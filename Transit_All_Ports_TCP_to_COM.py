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

    RunUp_ports_bool = {}
    RunUp_ports_name = {}

    SerialPort_dict = {}

    setup_command = False

    Baudrate = 0
    ip_address = 'localhost'
    ip_port_all_dict = {}
    ip_port = 0

    answer = {}

    def __init__(self, data: str = '33333'):

        self.SerialPort_dict = {}
        self.setup_command = False

        # Первое что делаем - парсим наши переменные
        self._definition_settings()
        # Второе что делаем - СМОТРИМ наши КОМ ПОРТЫ
        self._definition_COM_Ports()

        # Теперь переводим нашу войну и мир - Сначала в строку
        if type(data) != bytes:
            data = str(data)
            # и теперь в байты
            print('Информация для отправки - строка : ', data)
            data = data.encode()
        # Получаем данные для отправки
        print('Информация для отправки - байты :', data)
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


        # Получаем серйиный порт
        SerialPort = self.SerialPort_dict[COM_port_name]

        data = b''
        while True:

            # Ожидаем запуска команды
            if self.setup_command:

                print('Начинаем чтение ' + str(COM_port_name) + '\n')
                # Работаем пока включена передача
                while self.setup_command:
                    # print("read")
                    chack = SerialPort.readall()
                    # chack = SerialPort.read(size=size_data)
                    # чистим буффер
                    SerialPort.reset_output_buffer()
                    # chack = SerialPort.readline()
                    data = data + chack
                    # print(data)

                break
        # SerialPort.Close()
    #     print('СОМ ПОРТ ЗАКРЫЛИ')
        print('Прочитали данные :', data)
        print("Размер Полученных данных : ", getsizeof(data))

        # print('ПРОЧИТАЛИ',data, type(data))
        self.answer[COM_port_name] = data

    def Setup(self, COM: str = 'COM1'):
        """
        Метод Запуска - Через него запускаем все наши данные
        :param COM: COM порт на котором ожидаем (НОМЕР БЕЗЕТСЯ С НУМЕРАЦИИ НА ЖЕЛЕЗКЕ)
        :return:
        """

        self.SerialPort_dict = {}
        self.setup_command = False

        # делаем проверку на коректность заданных портов
        assert COM in ['COM1', 'COM2', 'COM3', 'COM4'], '\n Неправильно задан COM порт'

        # ТЕПЕРЬ - Получаем порт
        # Итак - Если порт существует - продолжаем
        assert self.RunUp_ports_bool[COM] is True, '\n COM порт не найден'
        # print(self.RunUp_ports_bool[COM])
        # print(self.RunUp_ports_name[COM])
        # print(self.ip_port_all_dict[COM])
        self.ip_port = self.ip_port_all_dict[COM]

        # Теперь запускаем наш TCP server
        # TCPsend = threading.Thread(target=self._Setup_send_data_TCP)
        # TCPsend.start()
        # /////////////////////////////////////////////////////////////////////////////////////////

        # /////////////////////////////////////////////////////////////////////////////////////////
        # открываем все ком порты

        COMPortsOpen = {}
        for port in self.RunUp_ports_name:
            COM_port = str(self.RunUp_ports_name[port])
            # print(COM_port)
            COMPortsOpen[port] = threading.Thread(target=self._setup_and_open_serial_port, args=(COM_port,))
            COMPortsOpen[port].start()

        for port in COMPortsOpen:
            COMPortsOpen[port].join()

        time.sleep(5)

        # Теперь начинаем чтение
        COMPortsResult = {}

        for port in self.RunUp_ports_name:
            COM_port = str(self.RunUp_ports_name[port])
            # print(COM_port)
            COMPortsResult[port] = threading.Thread(target=self._Read_to_com_port, args=(COM_port,))
            COMPortsResult[port].start()

        # Теперь запускаем наш TCP server
        TCPsend = threading.Thread(target=self._Setup_send_data_TCP)
        TCPsend.start()

        time.sleep(1)

        # запускаем
        self.setup_command = True

        TCPsend.join()

        # Останавливаем
        self.setup_command = False

        for thread in COMPortsResult:
            COMPortsResult[thread].join()
        # /////////////////////////////////////////////////////////////////////////////////////////
        print('ОТВЕТ : ', self.answer)

        result = ''
        for comport in self.answer:
            result = result + '\n ' + str(comport) + ' : ' + str(self.answer[comport])

        # А теперь сверяем -
        assert self.data == self.answer[
            self.RunUp_ports_name[COM]], '\n Получили не на тот порт что ожидали. Ожидали на ' + str(
            self.RunUp_ports_name[COM]) + ' Что получили - ' + str(result)


# for x in range(5):
#     TCPtoCOM().Setup(COM='COM'+ str(1 + x))
#
#     TCPtoCOM().Setup(COM='COM' + str(1 + x))

# try:
#     TCPtoCOM().Setup(COM='COM1')
#     print('++++++++++++++++++')
#     time.sleep(2)
# except :
#     print('----------------')
# time.sleep(2)
# try:
#     TCPtoCOM().Setup(COM='COM2')
#     print('++++++++++++++++++')
#     time.sleep(2)
# except :
#     print('----------------')
# time.sleep(2)
# try:
#     TCPtoCOM().Setup(COM='COM3')
#     print('++++++++++++++++++')
#     time.sleep(2)
# except :
#     print('----------------')
# time.sleep(2)
# try:
#     TCPtoCOM().Setup(COM='COM4')
#     print('++++++++++++++++++')
#     time.sleep(2)
# except :
#     print('----------------')

# data = 'lololol'
#
# # print(data)
# # TCPtoCOM(data=data).Setup(COM='COM2')
#
# TCPtoCOM(data=data).Setup(COM='COM2')
# # TCPtoCOM().Setup(COM='COM4')
