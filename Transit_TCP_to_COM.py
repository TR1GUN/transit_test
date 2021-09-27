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

    SerialPort_dict = {}

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
        # server.Received_Data()
        server.Close_socket()

        time.sleep(10)
        # запускаем
        self.setup_command = False

    def _Setup_received_data_COM(self, COM_port_name: str):
        """
        Здесь слушаем COM порт

        Запускается в отдельном потоке

        :return:
        """

        from Service.Connect_To_RS import ConnectToSerialPort

        Baudrate = int(self.Baudrate)

        SerialPort = ConnectToSerialPort(Port_Name=COM_port_name, Baudrate_Port=Baudrate)

        # Теперь начинаем прослушку - Только псоле тогок ак отправили что то
        # print('ПОРТ ОТКРЫЛИ')
        while True:
            if self.setup_command:
                SerialPort_data = SerialPort.Read()
                break
        # print(SerialPort_data)
        # И закрываем
        SerialPort.Close()
        print('ПОРТ ЗАКРЫЛИ')
        self.answer[COM_port_name] = SerialPort_data

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
        from sys import getsizeof
        # from datetime import datetime
        #
        #
        # # Узнаем размер пакета
        # size_data = getsizeof(self.data)
        # print('РАЗЩМЕР ЧТЕНИЯ ', size_data)
        # if size_data < 1:
        #     size_data = 1

        # Получаем серйиный порт
        SerialPort = self.SerialPort_dict[COM_port_name]

        # timeout = SerialPort.timeout
        # print(timeout)
        # if timeout is None:
        #     timeout = 1

        # data = b''
        # while True:
        #     # Ожидаем запуска команды
        #     if self.setup_command:
        #
        #         while True:
        #             print(SerialPort.in_waiting)
        #             chank = SerialPort.read(SerialPort.in_waiting)
        #             # чистим буффер
        #             # SerialPort.reset_output_buffer()
        #             data = data + chank
        #             print(data)
        # if SerialPort.in_waiting > 0 :
        #     chank = SerialPort.readall()
        #     # чистим буффер
        #     SerialPort.reset_output_buffer()
        #     data = data + chank
        #     print(data)

        # //-----------------------------------------------------------------------------------
        # //------------------Работает---------------------------------------------------------
        # // -----------------------------------------------------------------------------------

        data = b''
        while True:

            # Ожидаем запуска команды
            if self.setup_command:

                print('читаем ')
                # Работаем пока включена передача
                while self.setup_command:
                    chack = SerialPort.readall()
                    # chack = SerialPort.read(size=size_data)
                    # чистим буффер
                    SerialPort.reset_output_buffer()
                    # chack = SerialPort.readline()
                    data = data + chack
                    print(data)

                break

        print('data', getsizeof(data), data)
        # // -----------------------------------------------------------------------------------
        #
        # # Теперь дочитывааем
        # while True:
        #     chack = SerialPort.readall()
        #     SerialPort.reset_output_buffer()
        #     # chack = SerialPort.read(size=1)
        #     print('Дочитали', chack)
        #     data = data + chack
        #
        #     if chack == b'':
        #         break
        # # и дочитываем минуту
        # start = datetime.now()
        # print('------------')
        # print(start)
        # while True:
        #     chack = SerialPort.readall()
        #     data = data + chack
        #     start = start - datetime.now()
        #     if (int(start) - int(datetime.now())) > 60:
        #         break

        print('ПРОЧИТАЛИ', data, type(data))
        self.answer[COM_port_name] = data

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


        self.ip_port = self.ip_port_all_dict[COM]

        # Теперь запускаем наш TCP server
        # TCPsend = threading.Thread(target=self._Setup_send_data_TCP)
        # TCPsend.start()
        # /////////////////////////////////////////////////////////////////////////////////////////

        # /////////////////////////////////////////////////////////////////////////////////////////
        # открываем все ком порты

        COMPortsResult = {}

        for port in self.RunUp_ports_name:
            COM_port = str(self.RunUp_ports_name[port])
            print(COM_port)
            COMPortsResult[port] = threading.Thread(target=self._setup_and_open_serial_port, args=(COM_port,))
            COMPortsResult[port].start()

        for port in COMPortsResult:
            COMPortsResult[port].join()

        time.sleep(5)

        # Теперь начинаем чтение
        COMPortsResult = {}

        for port in self.RunUp_ports_name:
            COM_port = str(self.RunUp_ports_name[port])
            print(COM_port)
            COMPortsResult[port] = threading.Thread(target=self._Read_to_com_port, args=(COM_port,))
            COMPortsResult[port].start()

        # Теперь запускаем наш TCP server
        TCPsend = threading.Thread(target=self._Setup_send_data_TCP)
        TCPsend.start()

        time.sleep(1)

        # запускаем

        self.setup_command = True

        TCPsend.join()

        for thread in COMPortsResult:
            COMPortsResult[thread].join()
        # /////////////////////////////////////////////////////////////////////////////////////////
        print(self.answer)

        result = ''

        for comport in self.answer:
            result = result + '\n ' + str(comport) + ' : ' + str(self.answer[comport])

        # А теперь сверяем -
        assert self.data == self.answer[
            self.RunUp_ports_name[COM]], '\n Получили не на тот порт что ожидали. Ожидали на ' + str(
            self.RunUp_ports_name[COM]) + ' Что получили - ' + str(result)


data = 'lololol'

# print(data)
TCPtoCOM(data=data).Setup(COM='COM4')

# TCPtoCOM().Setup(COM='COM4')
# TCPtoCOM().Setup(COM='COM4')
