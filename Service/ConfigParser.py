# Здесь расположим парсер наших конфигов

import configparser
import os
# ----------------------------------------------------------------------------
path ='/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
path ='/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
# settings = 'config.ini'
settings = '../config.ini'

# настройки берем из конфига
parser = configparser.ConfigParser()
parser.read(os.path.join(path, settings))
#
#
uspd_ip = parser['Config']['uspd_ip']

rtu327 = parser['Config']['rtu327']
iface1 = parser['Config']['iface1']
iface2 = parser['Config']['iface2']
iface3 = parser['Config']['iface3']
iface4 = parser['Config']['iface4']
com1 = parser['Config']['COM1']
com2 = parser['Config']['COM2']
com3 = parser['Config']['COM3']
com4 = parser['Config']['COM4']

baudrate = int(parser['Config']['baudrate'])

# print(uspd_ip, type(uspd_ip))
# print(rtu327, type(rtu327))
# print(iface1, type(iface1))
# print(iface2, type(iface2))
# print(iface3, type(iface3))
# print(iface4, type(iface4))
# print(com1, type(com1))
