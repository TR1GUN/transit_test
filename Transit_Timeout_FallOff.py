import time
from Service.Setup import Setup
import threading


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                             Класс для работы - Отваливаемся по таймауту
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


class TimeoutFallOff(Setup):
    """
    Это основной класс запуска для отваливания по таймауту
    """
    data = b'\x33\x33\x33\x33\x33'

    RunUp_ports_bool = {}
    RunUp_ports_name = {}

    SerialPort_dict = {}

    Baudrate = 0
    ip_address = 'localhost'
    ip_port_all_dict = {}
    ip_port = 0

    COM_port = ''
    setup_command = False
    port_live = False
    answer = {}

    def __init__(self, data: str = '33333'):

        self.SerialPort_dict = {}

        self.setup_command = False
        self.port_live = False
        # Первое что деалем - парсим наши переменные
        self._definition_settings()
        # Второе что делаем - СМОТРИМ наши КОМ ПОРТЫ
        self._definition_COM_Ports()

        # Теперь переводим нашу войну и мир - Сначала в строку
        # if type(data) != bytes:
        #     data = str(data)
        #     # и теперь в байты
        #     data = data.encode()
        # self.data = data


    def _Setup_TCP(self, ip_port):
        """
        Здесь запускаем данные по TCP IP по определенному порту

        Запускается в отдельном потоке

        :return:
        """

        from Service.Connect_To_Server import ConnectToSocket

        import datetime

        start = datetime.datetime.now()

        ip_address = str(self.ip_address)
        # Запускаем порт
        server = ConnectToSocket(address=(ip_address, ip_port))
        time.sleep(150)

        falloff = server.PortStatus()
        print('--------falloff---------')
        print(falloff)
        self.port_live = True
        send_data = self.data

        # while True:
        #     if self.setup_command:
        #         server.Send_Data(data=send_data)
        #         break
        # # server.PortStatus()
        try:
            while True:
                if self.setup_command:
                    server.Send_Data(data=send_data)
                    print('Отправляем данные по порту что должен отвалиться')
                    break
        except:
            print('Порт отвалился по таймауту')
        falloff = server.PortStatus()
        print('--------falloff---------')
        print(falloff)
        print('ПОТОК', datetime.datetime.now() - start)

    def _Setup_send_data_COM(self):
        """
        Здесь слушаем COM порт

        Запускается в отдельном потоке

        :return:
        """
        # print('NAme port', COM_port_name)
        from Service.Connect_To_RS import ConnectToSerialPort

        send_data = self.data

        Baudrate = int(self.Baudrate)

        COM_port_name = str(self.COM_port)

        SerialPort = ConnectToSerialPort(Port_Name=COM_port_name, Baudrate_Port=Baudrate)

        # Теперь начинаем прослушку
        while True:
            if self.setup_command:
                #         SerialPort_data = SerialPort.Read()
                # Отправляем
                SerialPort.Write(data=send_data)
                break
        # И закрываем
        SerialPort.Close()

        # self.answer[COM_port_name] = SerialPort_data

    def _Setup_received_data_COM(self, COM_port_name: str):
        """
        Здесь слушаем COM порт

        Запускается в отдельном потоке

        :return:
        """
        # print('NAme port', COM_port_name)
        from Service.Connect_To_RS import ConnectToSerialPort

        Baudrate = int(self.Baudrate)

        SerialPort = ConnectToSerialPort(Port_Name=COM_port_name, Baudrate_Port=Baudrate)

        # Теперь начинаем прослушку
        while True:
            if self.setup_command:
                SerialPort_data = SerialPort.Read()
                break
        print('что прочитали ' + COM_port_name + str(SerialPort_data))
        # И закрываем
        SerialPort.Close()
        # print(COM_port_name)
        self.answer[COM_port_name] = SerialPort_data
        print(self.answer[COM_port_name])

    def _Setup_send_data_TCP(self, port):
        """
        Здесь запускаем данные по TCP IP по определенному порту

        Запускается в отдельном потоке

        :return:
        """

        from Service.Connect_To_Server import ConnectToSocket

        send_data = self.data
        ip_address = str(self.ip_address)
        ip_port = int(port)

        server = ConnectToSocket(address=(ip_address, ip_port))

        while True:
            if self.setup_command:
                server.Send_Data(data=send_data)
                break
        print('ОТПРАВИЛИ')
        # server.Received_Data()
        server.Close_socket()
        print('закрыли')

    # ---------------------------------------новые методы -----------------------------------------------

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
        #
        # """
        # Здесь реализуем чтение с нашего СОМ порта
        #
        # """
        # SerialPort = self.SerialPort_dict[COM_port_name]
        #
        # data = b''
        # while True:
        #     # Ожидаем запуска команды
        #     if self.setup_command:
        #         print('читаем ')
        #         # Работаем пока включена передача
        #         while self.setup_command:
        #             chack = SerialPort.readall()
        #             data = data + chack
        #             print(data)
        #         break
        #
        # print(data)
        # self.answer[COM_port_name] = data

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

        print('ПРОЧИТАЛИ', getsizeof(data), data, type(data))
        self.answer[COM_port_name] = data

    # // -----------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------

    def Setup(self, COM: str = 'COM1'):
        """
        Метод Запуска - ОЧЕНЬ ВАЖНО ЧТОБ ЭТО БЫЛО
        :param COM:
        :return:
        """
        self.SerialPort_dict = {}
        self.setup_command = False

        # Сначала проверяем что задачи правильны порт

        assert COM in ['COM1', 'COM2', 'COM3', 'COM4'], '\n Неправильно задан COM порт'

        # ТЕПЕРЬ - Получаем порт
        # Итак - Если порт существует - продолжаем
        assert self.RunUp_ports_bool[COM] is True, '\n COM порт не найден'

        ip_port = self.ip_port_all_dict[COM]
        IP_PortResult = {}

        import datetime
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

        # Теперь запускаем наш TCP server - Занимая все порты

        start = datetime.datetime.now()

        for port in self.ip_port_all_dict:
            ip_port = int(self.ip_port_all_dict[port])
            IP_PortResult[port] = threading.Thread(target=self._Setup_TCP, args=(ip_port,))
            IP_PortResult[port].start()

        self.setup_command = True

        time.sleep(120)

        # TCPsend = threading.Thread(target=self._Setup_send_data_TCP)
        # TCPsend.start()
        #
        # time.sleep(1)
        #
        # # запускаем
        #
        # self.setup_command = True
        #
        # TCPsend.join()
        #
        # for thread in COMPortsResult:
        #     COMPortsResult[thread].join()

        # ////////////////////////////////////////////////////////////////////////////////////////////////////

        # self.COM_port = self.RunUp_ports_name[COM]
        #
        # IP_PortResult = {}
        #
        # import datetime
        #
        # start = datetime.datetime.now()
        #
        # for port in self.ip_port_all_dict:
        #     ip_port = int(self.ip_port_all_dict[port])
        #     IP_PortResult[port] = threading.Thread(target=self._Setup_TCP, args=(ip_port,))
        #     IP_PortResult[port].start()
        #
        # time.sleep(120)
        #
        # # Теперь начинаем чтение
        # COMPortsResult = {}
        #
        # for port in self.RunUp_ports_name:
        #     COM_port = str(self.RunUp_ports_name[port])
        #     # print(COM_port)
        #     COMPortsResult[port] = threading.Thread(target=self._Setup_received_data_COM, args=(COM_port,))
        #     COMPortsResult[port].start()
        #
        # IP_PortResult_2 = {}
        # for port in self.ip_port_all_dict:
        #     ip_port = int(self.ip_port_all_dict[port])
        #     IP_PortResult_2[port] = threading.Thread(target=self._Setup_send_data_TCP, args=(ip_port,))
        #     IP_PortResult_2[port].start()
        #
        # self.setup_command = True
        # # time.sleep(60)
        #
        # print('три', self.answer)
        #
        # for thread in IP_PortResult_2:
        #     print('Закрываем')
        #     IP_PortResult_2[thread].join()
        # print('два', self.answer)
        #
        # for thread in COMPortsResult:
        #     COMPortsResult[thread].join()
        #
        # print('Раз', self.answer)
        # self.setup_command = False
        #
        # while True:
        #     if self.port_live:
        #         COMPortsResult = {}
        #
        #         for port in self.RunUp_ports_name:
        #             COM_port = str(self.RunUp_ports_name[port])
        #             # print(COM_port)
        #             COMPortsResult[port] = threading.Thread(target=self._Setup_received_data_COM, args=(COM_port,))
        #             COMPortsResult[port].start()
        #
        #         break
        # self.setup_command = True

        # /////////////////////////////////////////////////////////////////////////////////////////////////
        # # # # Теперь запускаем наш TCP server
        # TCPsend = threading.Thread(target=self._Setup_send_data_COM)
        # TCPsend.start()
        # #
        # # # Теперь начинаем чтение
        # IP_PortResult = {}
        #
        # for port in self.ip_port_all_dict:
        #     ip_port = int(self.ip_port_all_dict[port])
        #     # print(COM_port)
        #     IP_PortResult[port] = threading.Thread(target=self._Setup_received_data_TCP, args=(ip_port,))
        #     IP_PortResult[port].start()
        #
        # # Теперь это все соеденяем
        # TCPsend.join()
        #
        # for thread in IP_PortResult:
        #     IP_PortResult[thread].join()

        print(self.answer)
        #
        # result = ''
        #
        # for comport in self.answer:
        #     result = result + '\n ' + str(comport) + ' : ' + str(self.answer[comport])
        # #
        # # # А теперь сверяем -
        # assert self.data == self.answer[self.ip_port_all_dict[COM]], '\n Получили не на тот порт что ожидали. ' + \
        #                                                              'Ожидали на ' + str(self.RunUp_ports_name[COM]) + \
        #                                                               ' Что получили - ' + str(result)
        # print(datetime.datetime.now() - start)


# --------------------------------------------------------------------------------------------------------------------
TimeoutFallOff().Setup()
