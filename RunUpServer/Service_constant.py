# СЮДА ВЫНЕСИМ НАШИ КОНСТАНТЫ ЗНАЧЕНИЙ
from Service import ConfigParser

ip_port = str(ConfigParser.uspd_ip)

# ЗДЕСЬ СОДЕРЖИТЬСЯ наши значения портов по умолчанию
port_for_server_to_constant = \
    {
        'rtu327': str(ConfigParser.rtu327),
        'iface1': str(ConfigParser.iface1),
        'iface2': str(ConfigParser.iface2),
        'iface3': str(ConfigParser.iface3),
        'iface4': str(ConfigParser.iface4),
    }


