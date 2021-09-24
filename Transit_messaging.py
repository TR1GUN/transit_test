# здесь Расположим наши основные классы работы с транзитом
import time
from Service.Setup import Setup
import threading


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#            Класс для работы - Отправляем Эмулируем обмен сообщениями между УСПД в транзите и счетчиком
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

class TransitMessaging(Setup):
    """
    В Этом классе эмулируется поведение УСПД в режиме транзита
    """

    # Запрос счетчику
    message_to_meter = "message_to_meter_"
    # Ответ счетчика
    message_from_meter = "message_from_meter_"

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
# /////////////////////////////////////////////////////////////////////////////////////////


# /////////////////////////////////////////////////////////////////////////////////////////


    def _Session(self):
        """
        Сама сессия обмена инфой
        идет по принципу : Сообщения Транзитом TCP->COM-COM->TCP
        :return:
        """

        # Начинаем чтение TCP
        IP_PortResult = {}
        for port in self.ip_port_all_dict:
            ip_port = int(self.ip_port_all_dict[port])
            IP_PortResult[port] = threading.Thread(target=self._Received_data_TCP, args=(ip_port,))
            IP_PortResult[port].start()

        time.sleep(1)
        # Теперь запускаем наш COM - отправляем Инфу
        TCPsend = threading.Thread(target=self._Setup_send_data_COM)
        TCPsend.start()

        time.sleep(1)

        # запускаем
        self.setup_command = True

        TCPsend.join()

        # При завершении отправки - Закрываем потоки
        for thread in IP_PortResult:
            IP_PortResult[thread].join()

        # ---------------------------------------------------------------------------------
        # # ---> ТЕПЕРЬ ПРОВЕРЯЕМ ЧТО ВСЕ ХОРОШО ПОЛУЧИЛИ
        # ---------------------------------------------------------------------------------
        print(self.answer)
        result = ''
        for comport in self.answer:
            result = result + '\n ' + str(comport) + ' : ' + str(self.answer[comport])
        #
        # # А теперь сверяем -
        assert self.data == self.answer[self.ip_port_all_dict[COM]], '\n Получили не на тот порт что ожидали. ' + \
                                                                     'Ожидали на ' + str(self.RunUp_ports_name[COM]) + \
                                                                     ' Что получили - ' + str(result)

        # ---------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------
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

    def Setup(self, COM: str = 'COM1', count_messages:int = 10):
        """
        Метод Запуска - Через него запускаем все наше добро
        :param count_messages: Количество циклов обмена сообщений по типу Вопрос-Ответ
        :param COM: COM-порт на УСПД через который будет идти обмен
        :return:
        """
        # Еще ничего не запускали
        self.setup_command = False
        self.Server_dict = {}


        assert COM in ['COM1', 'COM2', 'COM3', 'COM4'], '\n Неправильно задан COM порт'

        # ТЕПЕРЬ - Получаем порт
        # Итак - Если порт существует - продолжаем
        assert self.RunUp_ports_bool[COM] is True, ' \n COM порт не найден'

        # ip_port = self.ip_port_all_dict[COM]
        self.COM_port = self.RunUp_ports_name[COM]

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



        ---------------------------------------------------------------------------------

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

        print('ОТВЕТ : ', self.answer)
        result = ''
        for comport in self.answer:
            result = result + '\n ' + str(comport) + ' : ' + str(self.answer[comport])

        # А теперь сверяем -
        assert self.data == self.answer[
            self.RunUp_ports_name[COM]], '\n Получили не на тот порт что ожидали. Ожидали на ' + str(
            self.RunUp_ports_name[COM]) + ' Что получили - ' + str(result)


# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////