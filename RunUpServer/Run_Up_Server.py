# ЗДЕСЬ расположим классы для работы с поднятием сервера с нужными портами в рамках сетинга


class GETSettingsUSPD:
    """
    Класс для получения данных запущенных серверов с USPD
    """
    http = 'http://'
    servers_settings = '/settings/servers/tcp'
    ip_port = '192.168.202.22'

    def __init__(self, ip_port: str):
        # собираем адрес запрсов
        self.ip_port = str(ip_port)

    def Get_Settings(self):
        # собираем адрес запросов
        url_get_uspd_Settings = self.http + self.ip_port + self.servers_settings
        import requests
        # Отправляем запрос
        uspd_Settings = requests.get(url_get_uspd_Settings)

        # Возвращаем данные
        return uspd_Settings.json()


class PUTSettingsUSPD:
    """
    Класс для отправки данных запущенных серверов с USPD
    """
    http = 'http://'
    servers_settings = '/settings/servers/tcp'
    ip_port = '192.168.202.22'
    data = {}

    def __init__(self, ip_port: str, data: dict):
        self.ip_port = str(ip_port)
        self.data = dict(data)

    def Put_Settings(self):
        # собираем адрес запросов
        url_get_uspd_Settings = self.http + self.ip_port + self.servers_settings
        import requests
        # Отправляем запрос
        # print(url_get_uspd_Settings)

        uspd_Settings_result = requests.put(url_get_uspd_Settings, json=self.data)

        # Возвращаем данные
        return uspd_Settings_result.status_code


class DefinitionOfRunUpServer:
    """
    Здесь парсим наш JSON ответа и определяем какие именно сервера подняты

    """

    RTU = False
    Transit_Iface1 = False
    Transit_Iface2 = False
    Transit_Iface3 = False
    Transit_Iface4 = False

    def __init__(self, Settings: dict):

        # Получаем наши настройки
        Settings = Settings.get('Settings')

        # Это должен быть список
        if Settings is not None:
            # если не ноль , то тогда перебираем элементы списка
            for setting in Settings:
                if setting.get('type') is not None:
                    self.setting_dict.get(setting.get('type'))(self, setting)

                    # value = True

    def _Transit_Iface1(self, setting):

        """# Переопределяем Iface1"""
        self.Transit_Iface1 = DefinitionOnPortServer(type=setting.get('type'), port=setting.get('port')).Port

    def _Transit_Iface2(self, setting):

        """# Переопределяем Iface2"""
        self.Transit_Iface2 = DefinitionOnPortServer(type=setting.get('type'), port=setting.get('port')).Port

    def _Transit_Iface3(self, setting):

        """# Переопределяем Iface3"""
        self.Transit_Iface3 = DefinitionOnPortServer(type=setting.get('type'), port=setting.get('port')).Port

    def _Transit_Iface4(self, setting):

        """# Переопределяем Iface4"""
        self.Transit_Iface4 = DefinitionOnPortServer(type=setting.get('type'), port=setting.get('port')).Port

    def _RTU(self, setting):

        """# Переопределяем rtu327"""
        self.RTU = DefinitionOnPortServer(type=setting.get('type'), port=setting.get('port')).Port

    setting_dict = \
        {
            'iface1': _Transit_Iface1,
            'iface2': _Transit_Iface2,
            'iface3': _Transit_Iface3,
            'iface4': _Transit_Iface4,
            'rtu327': _RTU,
        }


class DefinitionOnPortServer:
    """
    Здесь проверяем Соответствие портов
    """

    Port = False

    def __init__(self, type: str, port: str):
        from Service_constant import port_for_server_to_constant

        needed_port = port_for_server_to_constant.get(type)
        if needed_port is not None:
            if needed_port == port:
                self.Port = True


class FormElementJSON:
    """
    Здесь формируем наш элемент JSON
    """
    type_key = None

    def __init__(self, type_key: str):
        self.type_key = type_key

    def Get(self):
        from Service_constant import port_for_server_to_constant
        element = {'type': str(self.type_key), 'port': str(port_for_server_to_constant.get(self.type_key))}

        return element


class RunUpServer:
    """
    Класс поднятия сервера

    что делает - смотрит какие сервера подняты - с НУЖНЫМ Портом , и взависимости от того , какие подняты или нет - Подымает
    """
    import Service_constant
    ip_port = Service_constant.ip_port
    result = False

    def __init__(self,
                 rtu327: bool = False,
                 iface1: bool = True,
                 iface2: bool = True,
                 iface3: bool = True,
                 iface4: bool = True):

        # Пункт первый - Смотрим что у нас поднято
        # отправляем запрос
        ip_port = self.ip_port

        Settings = GETSettingsUSPD(ip_port=ip_port).Get_Settings()
        # Смотрим что поднято
        RunUp = DefinitionOfRunUpServer(Settings)

        Transit_Iface1 = RunUp.Transit_Iface1
        Transit_Iface2 = RunUp.Transit_Iface2
        Transit_Iface3 = RunUp.Transit_Iface3
        Transit_Iface4 = RunUp.Transit_Iface4
        RTU = RunUp.RTU

        # МЫ НИЧЕГО НЕ ПЕРЕЗАПИСЫВААЕМ ЕСЛИ ПОРТЫ УЖЕ НОРМАЛЬНО РАБОТАЮТ
        if (rtu327 == RTU) and (Transit_Iface1 == iface1) and (Transit_Iface2 == iface2) and (
                Transit_Iface3 == iface3) and (Transit_Iface4 == iface4):
            pass
        # ИНАЧЕ ПЕРЕЗАПИСЫВАЕМ
        else:
            Settings_list = []
            # ТЕПЕРЬ ЕСЛИ НАДО ЧТО ТО ПОДНЯТЬ
            if rtu327:
                Settings_list.append(self._form_JSON_element('rtu327'))

            if iface1:
                Settings_list.append(self._form_JSON_element('iface1'))

            if iface2:
                Settings_list.append(self._form_JSON_element('iface2'))

            if iface3:
                Settings_list.append(self._form_JSON_element('iface3'))

            if iface4:
                Settings_list.append(self._form_JSON_element('iface4'))

            # И после этого собираем наш основной JSON
            JSON = {'Settings': Settings_list}
            # отправлляем его
            result = PUTSettingsUSPD(ip_port=ip_port, data=JSON).Put_Settings()

            # ТЕПЕРЬ - Проверяем что мы подняли все то что надо

            Settings = GETSettingsUSPD(ip_port=ip_port).Get_Settings()

            if Settings == result:
                self.result = True

    def _form_JSON_element(self, type_key: str):
        """
        Метод для формирвоания строки поднятия

        :param RunUp: булевый маркер что это уже поднято
        :param type_key: сам ключ по котормоу будеит все формироваться
        :return: Возвращает Элемент , если надо
        """

        return FormElementJSON(type_key=type_key).Get()

    def Get_result(self):

        return self.result


