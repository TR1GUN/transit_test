# здесь конектимся к нашему серийному порту

import serial
from serial.tools import list_ports


class ConnectToSerialPort:
    """
    Это универсальеный класс конекта к Порту RS
    """
    SerialPort = None

    # В поля класса выносим все настройки порта - ЭТО ВАЖНО
    Name_port = 'COM1'
    baudrate = 9600
    timeout = 60.0
    # timeout = None
    bytesize = 8
    write_timeout = 30.0
    inter_byte_timeout = 2

    def __init__(self, Port_Name: str, Baudrate_Port: int = 9600):

        # Переопределяем переменные
        self.Name_port = Port_Name
        self.baudrate = Baudrate_Port

        # ТЕПЕРЬ ВЫЗЫВАЕМ ЕГО ИНИЦИАЛИЗАЦИЮ
        self._initialization_port()
        # И если нужно Открываем

    def _initialization_port(self):

        """
        пытаемся инициализировать наш КОМ ПОРТ
        :param Port_Name:
        """

        self.SerialPort = serial.Serial()
        #
        self.SerialPort.port = self.Name_port
        self.SerialPort.baudrate = self.baudrate
        self.SerialPort.timeout = self.timeout
        self.SerialPort.bytesize = self.bytesize
        self.SerialPort.write_timeout = self.write_timeout
        self.SerialPort.inter_byte_timeout = self.inter_byte_timeout
        # проверяем проверку четности
        # self.SerialPort.parity = SerialPort.PARITY_EVEN
        # self.SerialPort.parity = 'E'
        self._openCOMPort()

    def _openCOMPort(self):

        """
        открывтие порта

        :return:
        """
        # ЕСЛИ ПОРТ НЕ ОТКРЫТ то ОТКРЫВАЕМ ЕГО

        assert type(self.SerialPort) == serial.serialwin32.Serial, 'COM port не создавался'

        if not self.SerialPort.is_open:
            self.SerialPort.open()

    # ПОСКОЛЬКУ возникли проблемы с чтением - читаем разными способами
    def Read_to_timeout(self):
        """
        В этом методе пытаемся читать по таймауту
        :return:
        """

        from datetime import datetime
        timeout_start = datetime.now()
        # while True :

    def get_serial_port(self):

        """
        Этот метод возвращает Обьект серийного порта
        :return:
        """

        return self.SerialPort

    def Close(self):
        """Закрываем порт"""

        assert type(self.SerialPort) == serial.serialwin32.Serial, 'COM port не создавался'

        from time import sleep
        sleep(1)

        if self.SerialPort.is_open:
            self.SerialPort.close()

    def Write(self, data):
        """ЗДЕСЬ ЗАПИСЫВАЕМ Дaнные в порт"""

        self._openCOMPort()

        from time import sleep
        sleep(1)

        data = bytes(data)
        self.SerialPort.write(data)

    def Settings(self):
        """
        Здесь получаем настрйоки нащего ком порта

        :return: Возвращает None если порт не создан

        """

        settings = None

        if type(self.SerialPort) == serial.serialwin32.Serial:
            settings = self.SerialPort.get_settings()

        return settings

    @staticmethod
    def get_list_ports():
        """
        Так - Здесь статический метод - так до кучи
        Возвращает доступные порты
        """
        return list_ports.comports()
