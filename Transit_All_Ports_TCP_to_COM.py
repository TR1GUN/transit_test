# здесь Расположим наши основные классы работы с транзитом
import time
import threading
from Transit_TCP_to_COM import TCPtoCOM

# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                             Класс для работы - Отправляем на TCP читаем COM
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


class AllTCPtoCOM(TCPtoCOM):
    """
    Это основной класс запуска для способа транзита ТСР на СОМ
    """

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

        # Получаем рабочий TСP порт с которым работаем
        self.ip_port = self.ip_port_all_dict[COM]

        # открываем все ком порты
        COMPortsOpen = {}
        for port in self.RunUp_ports_name:
            COM_port = str(self.RunUp_ports_name[port])
            # print(COM_port)
            COMPortsOpen[port] = threading.Thread(target=self._setup_and_open_serial_port, args=(COM_port,))
            COMPortsOpen[port].start()

        for port in COMPortsOpen:
            COMPortsOpen[port].join()

        time.sleep(1)

        # Теперь начинаем чтение COM портов
        COMPortsResult = {}
        for port in self.RunUp_ports_name:
            COM_port = str(self.RunUp_ports_name[port])
            # print(COM_port)
            COMPortsResult[port] = threading.Thread(target=self._Read_to_com_port, args=(COM_port,))
            COMPortsResult[port].start()

        # Теперь запускаем наш TCP server
        TCPsend = threading.Thread(target=self._Setup_send_data_TCP)
        TCPsend.start()
        # time.sleep(1)
        # запускаем
        self.setup_command = True
        # Когда отправили мержим ветку
        TCPsend.join()
        # Останавливаем
        self.setup_command = False
        # Останавливаем поток чтения
        for thread in COMPortsResult:
            COMPortsResult[thread].join()
        # /////////////////////////////////////////////////////////////////////////////////////////
        # print('ОТВЕТ : ', self.answer)
        # Вспомогательный функционал для того чтоб посмотреть все что пришло - сделанно топорно - но все же
        result = ''
        for comport in self.answer:
            result = result + '\n ' + str(comport) + ' : ' + str(self.answer[comport])
        # /////////////////////////////////////////////////////////////////////////////////////////
        # # А теперь сверяем -
        self.CheckUp(COM=COM)

        # # А теперь сверяем -
        # assert self.data == self.answer[
        #     self.RunUp_ports_name[COM]], '\n Получили не на тот порт что ожидали. Ожидали на ' + str(
        #     self.RunUp_ports_name[COM]) + ' Что получили - ' + str(result)

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
#                                    Тестовые запуски
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

# data = 'lololol'
#
# # print(data)
# # TCPtoCOM(data=data).Setup(COM='COM2')
# #
# AllTCPtoCOM(data=data).Setup(COM='COM2')
# # # TCPtoCOM().Setup(COM='COM4')
