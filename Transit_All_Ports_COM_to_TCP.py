# здесь Расположим наши основные классы работы с транзитом
import time
from Service.Setup import Setup
import threading
from Transit_COM_to_TCP import COMtoTCP

# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                             Класс для работы - Отправляем на COM  читаем TCP
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


class AllCOMtoTCP(COMtoTCP):
    """
    Это основной класс запуска для способа транзита ТСР на СОМ
    """



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

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
#                                    Тестовые запуски
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////



AllCOMtoTCP('gfdfdfdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddf').Setup(COM='COM2')
