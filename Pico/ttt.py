import socket
import socket_client
import wlan
import socket_server
import Tools
import lightsensitive
import network
import machine
import json

from machine import Pin
from utime import sleep


def led():
    pin = Pin("WL_GPIO0", Pin.OUT)
    ledi = 0
    while ledi <= 2:
        pin.toggle()
        sleep(0.5)
        ledi += 1
    pin.low()


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # 设为STA模式
    wlan.active(True)  # 启用网络
    wlan.connect(ssid, password)  # 连接网络AP
    while wlan.isconnected() == False:
        print("等待连接...")
        sleep(1)
    print('IP: ', wlan.ifconfig()[0])  # 显示Pico W开发板IP地址
    if wlan.isconnected():
        led()
    print("wifi", wlan.isconnected())
    return True


ip = '192.168.1.105'
port = 8001
bufsize = 1024
ttl = 86400


def send_udp_client_data(send_data):
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_client.sendto(send_data, (ip, port))
    socket_client.close()


def getLight():
    adc_light = machine.ADC(machine.Pin(26))
    light = adc_light.read_u16()
    return light


def json_decode(json_dict_):
    return json.loads(json_dict_)


def json_encode(dict_):
    return json.dumps(dict_, )


if connect_wifi("", ""):
    while True:
        led()
        send_udp_client_data(json_encode(
            {'light': getLight(), 'cmd': 'null'}))
        sleep(10)

# oled = Pin('WL_GPIO0', Pin.OUT)       # 板载LED连到WL_GPIO0
# oled.value(0)                         # 板载LED熄灭
# oled.toggle()
# time.sleep(1)

# if wlan.connect_wifi("", ""):
#     send_data = "65535"
#     socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     socket_client.sendto(send_data.encode('utf-8'), ('192.168.1.105', 8001))
# print(time.gmtime())
# print(time.time())
# light = lightsensitive.getLight()
# print(light)
# send_data = tools.json_encode({'t': time.localtime(), 'light': light})
# print(light)
# if wlan.connect_wifi('', ''):
# socket_client.send_upd_client_data(send_data)
# socket_server.start_udp_server()
# i = 0
# while True:
#     socket_client.send_udp_client_data(tools.json_encode(
#         {'light': lightsensitive.getLight(), 'cmd': 'null'}))
#     print(lightsensitive.getLight())
#     time.sleep(10)
