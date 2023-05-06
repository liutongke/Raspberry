import wlan
from machine import Pin
import network
import socket
import time

ip = '192.168.1.105'
port = 8001
bufsize = 1024
ttl = 86400


def send_udp_client_data(send_data):
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_client.sendto(send_data, (ip, port))
    socket_client.close()
