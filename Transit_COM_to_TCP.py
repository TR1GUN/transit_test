# здесь Расположим наши основные классы работы с транзитом
import time
from Service.Setup import Setup
import threading


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                             Класс для работы - Отправляем на COM  читаем TCP
#                             Здесь Производиться работа ТОЛЬКО С ОПРЕДЕЛЕННЫМ COM портом
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


class COMtoTCP(Setup):
    """

    Это основной класс запуска для способа транзита ТСР на СОМ
    Здесь Производиться работа ТОЛЬКО С ОПРЕДЕЛЕННЫМ COM портом

    """
    data = b'\x33\x33\x33\x33\x33'

    # Поднятые сервера
    RunUp_ports_bool = {}
    # ИМЕНА поднятых серверов
    RunUp_ports_name = {}

    # Маркер запущенной команды - нужна чтоб избежать гонки потоков
    setup_command = False
    # Запущенные сервера
    Server_dict = {}

    # Скорость COM порта
    Baudrate = 0
    # IP адресс сервера
    ip_address = 'localhost'
    # словарь всех запущенных портов
    ip_port_all_dict = {}
    # Наш IP порт что используем
    ip_port = 0
    # Наш COM порт что используем
    COM_port = ''

    # Словарь ответов из всех доступных портов
    answer = {}

    # Байтовый буфер, который захардкожен в модуле транзита
    byte_buffer = 4096

    # ОШИБКА СОКЕТА - превышен таймаут
    from Service.Service_constant import get_error_socket_timeout
    error_socket = get_error_socket_timeout()

    def __init__(self, data: str = '33333'):

        """

        :param data:Сюда надо вставить данные для транзита

        """

        self.setup_command = False
        self.Server_dict = {}
        # Первое что деалем - парсим наши переменные
        self._definition_settings()
        # Второе что делаем - СМОТРИМ наши КОМ ПОРТЫ
        self._definition_COM_Ports()

        # Теперь переводим нашу войну и мир - Сначала в строку
        if type(data) != bytes:
            data = str(data)
            # и теперь в байты
            data = data.encode()
        self.data = data

    def _Setup_send_data_COM(self):
        """
        Здесь слушаем COM порт
        Запускается в отдельном потоке

        :return:
        """

        from Service.Connect_To_RS import ConnectToSerialPort

        send_data = self.data

        Baudrate = int(self.Baudrate)

        COM_port_name = str(self.COM_port)

        # Открываем порт
        SerialPort = ConnectToSerialPort(Port_Name=COM_port_name, Baudrate_Port=Baudrate)

        # Не пускаем команду пока не разрешим
        while True:
            if self.setup_command:
                # Теперь пускаем команду
                # time.sleep(1)
                print('Отправляем')
                SerialPort.Write(data=send_data)
                break
        # И закрываем соединение
        SerialPort.Close()

        # time.sleep(1)
        # отпускаем обмен
        self.setup_command = False

    def _Setup_server_TCP(self, ip_port):
        """
        Здесь запускаем данные по TCP IP по определенному порту

        Запускается в отдельном потоке

        :return:
        """

        from Service.Connect_To_Server import ConnectToSocket

        ip_address = str(self.ip_address)

        self.Server_dict[ip_port] = ConnectToSocket(address=(ip_address, ip_port)).get_socket()

    def _Received_data_TCP(self, COM_port_name: str):

        """
        Здесь реализуем чтение с нашего СОМ порта

        """

        Server = self.Server_dict[COM_port_name]

        data = b''
        while True:
            # Ожидаем запуска команды
            if self.setup_command:
                print('читаем порт')
                # Работаем пока включена передача
                while self.setup_command:
                    timeout = 3.0

                    # Ставим таймаут- ЭТО ОЧЕНЬ ВАЖНО
                    Server.settimeout(float(timeout))
                    try:
                        # ЧИТАЕМ РОВНО СТОЛЬКО СКОЛЬКО ЕСТЬ в буфере
                        chack = Server.recv(self.byte_buffer)
                        # print(chack)
                        data = data + chack

                    # ТЕПЕПРЬ обрабатываем ошибки -
                    # ЕСЛИ ОТВАЛИЛИСЬ ПО ТАЙМАТУ _ ТО ВСЕ НОРМ И ОК

                    except self.error_socket:
                        print('Отвалились')
                        break
                    # ЕСЛИ ИНАЯ _ ВЫВОДИМ ЕЕ
                    except Exception as e:

                        print('Ошибка при чтении с сокета', e)
                        break
                break
        self.answer[COM_port_name] = data

        Server.close()

    # /////////////////////////////////////////////////////////////////////////////////////////
    #                         Главная Функция сравнения
    # /////////////////////////////////////////////////////////////////////////////////////////
    def CheckUp(self, COM):

        """
        Главный  метод сравнения
        """

        # Порт что ожидали
        ip_port = int(self.ip_port_all_dict.get(COM))
        result = self.answer[ip_port]

        print('self.data', self.data)
        print('result', result)

        assert self.data == result, '\n Получили не на тот порт что ожидали. ' + \
                                    'Что ожидали - ' + str(self.data) + \
                                    ' Что получили - ' + str(result)

    # /////////////////////////////////////////////////////////////////////////////////////////
    #                         Главная Функция Запуска
    # /////////////////////////////////////////////////////////////////////////////////////////
    def Setup(self, COM: str = 'COM1'):
        """
        Метод Запуска - ОЧЕНЬ ВАЖНО ЧТОБ ЭТО БЫЛО
        :param COM: Наш КОМ порт на железке через который гоняем тесты
        :return:
        """

        # Обнуляем наши переменные - Словарь серверов что читают
        # И маркер начала запуска
        self.setup_command = False
        self.Server_dict = {}

        # Проверяем что правильно задали ком порт
        assert COM in ['COM1', 'COM2', 'COM3', 'COM4'], '\n Неправильно задан COM порт'

        # ТЕПЕРЬ - Получаем порт
        # Итак - Если порт существует - продолжаем
        assert self.RunUp_ports_bool[COM] is True, '\n COM порт не найден'

        # Открываем Нужный нам порт
        self.COM_port = self.RunUp_ports_name[COM]

        # Подымаем нужный нам сервер
        Server_run_up = {}

        # Получаем наш ip порт
        ip_port = int(self.ip_port_all_dict.get(COM))

        Server_run_up[ip_port] = threading.Thread(target=self._Setup_server_TCP, args=(ip_port,))
        Server_run_up[ip_port].start()
        # # ждем пока подымется все и вся
        # time.sleep(1)
        Server_run_up[ip_port].join()

        # time.sleep(1)
        #
        # Теперь начинаем чтение
        IP_PortResult = {}

        # ТЕПЕРЬ ЗАПУСКАЕМ TCP
        IP_PortResult[ip_port] = threading.Thread(target=self._Received_data_TCP, args=(ip_port,))
        IP_PortResult[ip_port].start()

        # Теперь запускаем наш COM
        TCPsend = threading.Thread(target=self._Setup_send_data_COM)
        TCPsend.start()

        # time.sleep(1)

        # запускаем
        self.setup_command = True

        TCPsend.join()
        IP_PortResult[ip_port].join()
        # # /////////////////////////////////////////////////////////////////////////////////////////

        self.CheckUp(COM=COM)

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
#                                    Тестовые запуски
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////


COMtoTCP(
    'gfdfdfdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddf').Setup(
    COM='COM2')
