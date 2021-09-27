# здесь Расположим наши основные классы работы с транзитом
import time
from Service.Setup import Setup
import threading


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                             Класс для работы - Отправляем на TCP читаем COM
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


class TCPtoCOM(Setup):
    """
    Это основной класс запуска для способа транзита ТСР на СОМ
    """
    data = b'\x33\x33\x33\x33\x33'

    # Поднятые сервера
    RunUp_ports_bool = {}
    # ИМЕНА поднятых серверов
    RunUp_ports_name = {}

    # Маркер запущенной команды - нужна чтоб избежать гонки потоков
    setup_command = False
    # Открытые COM порты
    SerialPort_dict = {}

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

    def __init__(self, data: str = '33333'):

        """

        :param data:Сюда надо вставить данные для транзита

        """

        self.SerialPort_dict = {}
        self.setup_command = False

        # self.data = data
        # Первое что деалем - парсим наши переменные
        self._definition_settings()
        # Второе что делаем - СМОТРИМ наши КОМ ПОРТЫ
        self._definition_COM_Ports()

        # Теперь переводим нашу войну и мир - Сначала в строку
        if type(data) != bytes:
            # и теперь в байты
            data = str(data).encode()
            # print('Go bytes',data)
        self.data = data

    def _Setup_send_data_TCP(self):
        """
        Здесь запускаем данные по TCP IP по определенному порту

        Запускается в отдельном потоке

        :return:
        """

        from Service.Connect_To_Server import ConnectToSocket

        send_data = self.data
        ip_address = str(self.ip_address)
        ip_port = int(self.ip_port)

        server = ConnectToSocket(address=(ip_address, ip_port))

        # Не пускаем команду пока не разрешим
        while True:
            if self.setup_command:
                # Теперь пускаем команду
                server.Send_Data(data=send_data)
                break
        # И закрываем соединение
        server.Close_socket()

        # запускаем
        self.setup_command = False

    def _setup_and_open_serial_port(self, COM_port_name: str):

        """
        Этот метод ОТКРЫВАЕТ нужный серийный порт - ЭТО ОЧЕНЬ ВАЖНО

        :return:
        """

        from Service.Connect_To_RS import ConnectToSerialPort

        Baudrate = int(self.Baudrate)

        self.SerialPort_dict[COM_port_name] = ConnectToSerialPort(Port_Name=COM_port_name,
                                                                  Baudrate_Port=Baudrate).get_serial_port()

    def _Read_to_com_port(self, COM_port_name: str):

        """
        Здесь реализуем чтение с нашего СОМ порта

        """
        # from sys import getsizeof

        # Получаем серйиный порт
        SerialPort = self.SerialPort_dict[COM_port_name]

        data = b''
        while True:

            # Ожидаем запуска команды
            if self.setup_command:
                # Ставим таймаут
                timeout = 3.0
                SerialPort.timeout = float(timeout)
                # Работаем пока включена передача
                while self.setup_command:
                    try:
                        chack = SerialPort.readall()
                        # chack = SerialPort.read(size=size_data)
                        # чистим буффер
                        SerialPort.reset_output_buffer()
                        # chack = SerialPort.readline()
                        data = data + chack
                    # ЕСЛИ ошибка - ВЫВОДИМ ЕЕ
                    except Exception as e:
                        print('Ошибка при чтении с COM порта ', str(e))
                        break
                break

        # print('data', getsizeof(data), data)

        print(str(COM_port_name) + ' - ПРОЧИТАЛИ : ', data, type(data))
        self.answer[COM_port_name] = data

    # /////////////////////////////////////////////////////////////////////////////////////////
    #                         Главная Функция сравнения
    # /////////////////////////////////////////////////////////////////////////////////////////
    def CheckUp(self, COM):

        """
        Главный  метод сравнения
        """

        # Порт что ожидали
        COM_port = str(self.RunUp_ports_name.get(COM))
        result = self.answer[COM_port]

        # print('self.data', self.data)
        # print('result', result)

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

        # Обнуляем наши переменные - Словарь COM портов что читают
        # И маркер начала запуска
        self.SerialPort_dict = {}
        self.setup_command = False

        # Проверяем что правильно задали ком порт
        assert COM in ['COM1', 'COM2', 'COM3', 'COM4'], '\n Неправильно задан COM порт'

        # ТЕПЕРЬ - Получаем порт
        # Итак - Если порт существует - продолжаем
        assert self.RunUp_ports_bool[COM] is True, '\n COM порт не найден'

        # Получаем нужный нам TCP порт
        self.ip_port = int(self.ip_port_all_dict.get(COM))
        # открываем ком порт

        # Создаем словарь
        COMPortsResult = {}
        # Получаем наш COM порт
        COM_port = str(self.RunUp_ports_name.get(COM))
        # Открываем серийный порт
        COMPortsResult[self.ip_port] = threading.Thread(target=self._setup_and_open_serial_port, args=(COM_port,))
        COMPortsResult[self.ip_port].start()
        # time.sleep(1)
        COMPortsResult[self.ip_port].join()

        # Теперь начинаем чтение
        COMPortsResult = {}
        #
        COMPortsResult[self.ip_port] = threading.Thread(target=self._Read_to_com_port, args=(COM_port,))
        COMPortsResult[self.ip_port].start()

        # Теперь запускаем наш TCP server
        TCPsend = threading.Thread(target=self._Setup_send_data_TCP)
        TCPsend.start()

        # # запускаем
        self.setup_command = True

        TCPsend.join()
        COMPortsResult[self.ip_port].join()
        # # /////////////////////////////////////////////////////////////////////////////////////////

        self.CheckUp(COM=COM)


# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
#                                    Тестовые запуски
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
#
# data = 'llololollololollololollololollololollololollololollololollololollololollololollololollololollololollolololololol'
#
# # print(data)
# TCPtoCOM(data=data).Setup(COM='COM4')

# TCPtoCOM().Setup(COM='COM4')
# TCPtoCOM().Setup(COM='COM4')
