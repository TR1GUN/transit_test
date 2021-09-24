# здесь Расположим наши основные классы работы с транзитом
import time
from Service.Setup import Setup
import threading


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                             Класс для работы - Отправляем на COM  читаем TCP
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


class COMtoTCP(Setup):
    """
    Это основной класс запуска для способа транзита ТСР на СОМ
    """
    data = b'\x33\x33\x33\x33\x33'

    RunUp_ports_bool = {}
    RunUp_ports_name = {}

    setup_command = False
    Server_dict = {}

    Baudrate = 0
    ip_address = 'localhost'
    ip_port_all_dict = {}
    ip_port = 0

    COM_port = ''

    answer = {}

    def __init__(self, data: str = '33333'):

        # self.data = data
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

    def _Setup_received_data_TCP(self, ip_port):
        """
        Здесь запускаем данные по TCP IP по определенному порту

        Запускается в отдельном потоке

        :return:
        """

        from Service.Connect_To_Server import ConnectToSocket

        # send_data = self.data
        ip_address = str(self.ip_address)
        # ip_port = int(self.ip_port)

        server = ConnectToSocket(address=(ip_address, ip_port))

        # server.Send_Data(data=send_data)
        ReceivedPort_data = server.Received_Data()
        server.Close_socket()

        self.answer[ip_port] = ReceivedPort_data

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
                time.sleep(1)
                print('Отправляем')
                SerialPort.Write(data=send_data)
                break
        # И закрываем соединение
        SerialPort.Close()

        time.sleep(1)
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

                    try :
                        chack = Server.recv(1)

                        data = data + chack

                    except :
                        print('Не удалось считать')
                        break

                break
        self.answer[COM_port_name] = data

        Server.close()
    # -------------------

    def Setup(self, COM: str = 'COM1'):
        """
        Метод Запуска - ОЧЕНЬ ВАЖНО ЧТОБ ЭТО БЫЛО
        :param COM:
        :return:
        """
        self.setup_command = False
        self.Server_dict = {}


        assert COM in ['COM1', 'COM2', 'COM3', 'COM4'], '\n Неправильно задан COM порт'

        # ТЕПЕРЬ - Получаем порт
        # Итак - Если порт существует - продолжаем
        assert self.RunUp_ports_bool[COM] is True, '\n COM порт не найден'

        # ip_port = self.ip_port_all_dict[COM]
        self.COM_port = self.RunUp_ports_name[COM]

        # /////////////////////////////////////////////////////////////////////////////////////////

        # /////////////////////////////////////////////////////////////////////////////////////////
        # открываем все ком порты

        Server_run_up = {}

        for server in self.ip_port_all_dict:
            ip_port = int(self.ip_port_all_dict[server])
            # print(COM_port)
            Server_run_up[server] = threading.Thread(target=self._Setup_server_TCP, args=(ip_port,))
            Server_run_up[server].start()

        # ждем пока подымется все и вся
        for server in Server_run_up:
            Server_run_up[server].join()

        time.sleep(5)

        # Теперь начинаем чтение
        IP_PortResult = {}

        for port in self.ip_port_all_dict:
            ip_port = int(self.ip_port_all_dict[port])
            IP_PortResult[port] = threading.Thread(target=self._Received_data_TCP, args=(ip_port,))
            IP_PortResult[port].start()

        time.sleep(1)

        # Теперь запускаем наш COM
        TCPsend = threading.Thread(target=self._Setup_send_data_COM)
        TCPsend.start()

        time.sleep(1)

        # запускаем
        self.setup_command = True

        TCPsend.join()

        for thread in IP_PortResult:
            IP_PortResult[thread].join()
        # /////////////////////////////////////////////////////////////////////////////////////////
        print(self.answer)

        result = ''

        for comport in self.answer:
            result = result + '\n ' + str(comport) + ' : ' + str(self.answer[comport])
        #
        # # А теперь сверяем -
        assert self.data == self.answer[self.ip_port_all_dict[COM]], '\n Получили не на тот порт что ожидали. ' + \
                                                                     'Ожидали на ' + str(self.RunUp_ports_name[COM]) + \
                                                                     ' Что получили - ' + str(result)



COMtoTCP('gfdfdfdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddf').Setup(COM='COM3')