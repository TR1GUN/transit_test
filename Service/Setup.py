# Здесь расположим класс для запуска нашего теста
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                                             КЛАСС ОПРЕДЕЛЕНИЯ ПОРТОВ
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


class DefinePortConnection:
    """
    В этом классе определяем какие у нас есть порты и делаем соответсвие

    """
    # у нас в 40 смарте есть только 4 порта RS - Делаем их
    Ports = {'COM1': None, 'COM2': None, 'COM3': None, 'COM4': None}
    list_all_ports = []
    RunUp_ports_bool = {}
    RunUp_ports_name = {}

    def __init__(self):
        # Первое что делаем - Определяем порты
        self._define_port_on_config_parser()
        self._getting_list_ports()
        self.RunUp_ports_bool = self._define_ports()
        self.RunUp_ports_name = self._accordance_port()

    def _getting_list_ports(self):
        """СНАЧАЛА получаем все порты что подключены"""
        from Service.Connect_To_RS import ConnectToSerialPort

        list_ports = ConnectToSerialPort.get_list_ports()

        for port in list_ports:
            self.list_all_ports.append(port.name)

    def _define_port_on_config_parser(self):
        """Здесь определяем порты что определены в конфиг парсере"""
        from Service.ConfigParser import com1, com2, com3, com4
        # берем нашу переменную и переопределяем ее
        self.Ports['COM1'] = com1
        self.Ports['COM2'] = com2
        self.Ports['COM3'] = com3
        self.Ports['COM4'] = com4

    def _define_ports(self):
        """
        САМ ОПРЕДЕЛИТЕЛЬ портов
        Если порта нет в живых - То возвращаем FASLE
        ЕСЛИ он присутствует то возвращаем в TRUE
        """

        Ports = {}
        for port in self.Ports:
            if self.Ports[port] in self.list_all_ports:
                Ports[port] = True
            else:
                Ports[port] = False

        return Ports

    def _accordance_port(self):
        """ Удаляем не поднятые порты  """

        Ports = self.Ports

        for port in self.RunUp_ports_bool:
            if not self.RunUp_ports_bool[port]:
                # Если этот порт не поднят - Удаляем его из общего списка
                Ports.pop(port)

        return Ports

    def Define(self):
        """Возвращаем список булевых маркеров поднятых портов"""

        return self.RunUp_ports_bool

    def Get_accordance_port(self):
        """Возвращаем имена поднятых портов"""

        return self.RunUp_ports_name


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                                             БАЗОВЫЙ КЛАСС ЗАПУСКА
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

class Setup:
    """
    Это основной класс запуска для способа транзита ТСР на СОМ
    """
    data = b'\x33\x33\x33\x33\x33'

    RunUp_ports_bool = {}
    RunUp_ports_name = {}

    Baudrate = 0
    ip_address = 'localhost'
    ip_port_all_dict = {}
    ip_port = 0

    def _definition_COM_Ports(self):
        """Здесь определяем Ком порты"""

        # from Service.Setup import DefinePortConnection

        define = DefinePortConnection()

        self.RunUp_ports_bool = define.RunUp_ports_bool

        self.RunUp_ports_name = define.RunUp_ports_name

    def _definition_settings(self):
        """
        В этой функции Определяем основные переменнные - ЭТО ВАЖНО

        Данный метод должен запускаться в конструкторе
        :return:
        """
        # ИМПОРТИРУЕМ НАШИ ПЕРЕМЕННЫЕ
        from Service.ConfigParser import baudrate, uspd_ip, iface1, iface2, iface3, iface4, com1, com2, com3, com4

        # Теперь - Определяем общие переменные

        # скорость порта
        self.Baudrate = int(baudrate)

        # ip адресс
        self.ip_address = uspd_ip

        # открытые сервера портов
        self.ip_port_all_dict = {
            'COM1': int(iface1),
            'COM2': int(iface2),
            'COM3': int(iface3),
            'COM4': int(iface4),
        }
