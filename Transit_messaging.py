# здесь Расположим наши основные классы работы с транзитом
import time
from Service.Setup import Setup
import threading


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#            Класс для работы - Отправляем Эмулируем обмен сообщениями между УСПД в транзите и счетчиком
#                         В ЭТОМ КЛАССЕ - Слушаем Определенный порт -

# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

class TransitMessaging(Setup):
    """
    В Этом классе эмулируется поведение УСПД в режиме транзита - Слушаем Определенный порт

    """

    # Запрос счетчику
    message_to_meter = "message_to_meter_"
    # Ответ счетчика
    message_from_meter = "message_from_meter_"
    # Индекс обмена
    message_index = 0

    def __init__(self,
                 # Сообщение Которое идет из COM
                 message_from_meter: str = "message_from_meter_",
                 # Сообщение Которое идет в COM
                 message_to_meter: str = "message_to_meter_"):
        """
         В Этом классе эмулируется поведение УСПД в режиме транзита - Слушаем все ПОРТЫ

        :param message_from_meter: Сообщение Которое идет из COM
        :param message_to_meter: Сообщение Которое идет в COM
        """

    # Сама сессия обмена инфой  идет по принципу : Сообщения Транзитом TCP->COM-COM->TCP
    def Setup(self, COM: str = 'COM1', count_messages: int = 10):
        """
        Метод Запуска - Через него запускаем все наше добро
        Сама сессия обмена инфой  идет по принципу : Сообщения Транзитом TCP->COM-COM->TCP

        :param count_messages: Количество циклов обмена сообщений по типу Вопрос-Ответ
        :param COM: COM-порт на УСПД через который будет идти обмен
        :return:
        """

        from Transit_COM_to_TCP import COMtoTCP
        from Transit_TCP_to_COM import TCPtoCOM

        count_messages = int(count_messages)
        # Инициализируем нашу сессию
        for self.message_index in range(count_messages):
            # подготавливаем сообщения
            message_from_meter = self.message_from_meter + str(self.message_index)
            message_to_meter = self.message_to_meter + str(self.message_index)

            Message_to_meter = TCPtoCOM(data=message_to_meter).Setup(COM=str(COM))

            Message_from_meter = COMtoTCP(data=message_from_meter).Setup(COM=str(COM))

# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                                           Тестовые запуски
#
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

# TransitMessaging(message_from_meter='message_from_meter', message_to_meter='message_to_meter').Setup(COM="COM1", count_messages=10)