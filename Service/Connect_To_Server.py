# Здесь мы работаем с сокетом - ЭТО ВАЖНО
import socket


# print('ip_address', ip_address, type(ip_address))
# print('ip_address', ip_port, type(ip_port))

class ConnectToSocket:
    sock = None

    def __init__(self, address):

        # при инициализации класса запускам сам сокет , чо б нет
        self.answer = self._setup(address=address)
        self.address  = address

    def _setup(self, address):
        """
        Метод запуска сокета
        :param address: - Адрес сокета - Это очень важно
        :return:
        """

        # Создаем сокет
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = socket.socket()
        self.sock.settimeout(10)
        # Подключаемся по нужному адресу
        self.sock.connect(address)
        print('ЗАПУСТИЛИ ', address)

    def Send_Data(self, data):
        """
        Метод Для отправки каких либо данных -

        Проверку типов пока не ставим , зочем нам надо это
        :param data:
        :return:
        """
        from time import sleep

        sleep(1)
        print('ОТПРАВИЛИ ', data)
        self.sock.sendall(data)
        print('--->', self.sock.getpeername())

    def Received_Data(self):

        """
        Метод для проверки данных что мы отправляем - чо нам

        :return: И возвращаем что мы получиили
        """
        answer_bytes = b''
        while True:
            try:
                buffer = bytes
                buffer = self.sock.recv(1)
                # print(buffer)

                # print('buffer', buffer)
                answer_bytes = answer_bytes + buffer
            except:

                break
        return answer_bytes

    def Close_socket(self):

        """
        Метод дял закрытия сокета - это может быть важно
        :return:
        """

        self.sock.close()

    def get_socket(self):

        return self.sock

    def PortStatus(self):

        from time import sleep
        # while True :
            # print(self.sock.getpeername())
            # print(self.sock.getblocking())
            # print(self.sock.gettimeout())
            # print(self.sock.getsockname())
        print('--->', self.sock.getpeername())

        return self.sock.fileno()
            # sleep(60)
