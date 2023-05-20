import network
from utime import sleep
import led
import config
import ntptime


# 无线网连接
class Wlan:
    ip = ''

    def connect_wifi(self):
        print(config.get_wlan_ssid(),
              config.get_wlan_passwd())

        self.wlan = network.WLAN(network.STA_IF)  # 设为STA模式
        self.wlan.active(True)  # 启用网络
        self.wlan.connect(config.get_wlan_ssid(),
                          config.get_wlan_passwd())  # 连接网络AP
        while not self.wlan.isconnected():
            print("等待连接...")
            sleep(2)

        if self.wlan.isconnected():
            led.Led().blingbling()
        print('IP: ', self.wlan.ifconfig()[0])  # 显示Pico W开发板IP地址
        # print("wifi", self.wlan.isconnected())
        ntptime.host = 'ntp1.aliyun.com'
        ntptime.settime()
        # self.ap_open()
        return True

    # 开启热点
    def ap_open(self, ssid='Pico-w', password='123456789'):
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=ssid, password=password)
        ap.active(True)
