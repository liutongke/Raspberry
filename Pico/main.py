import oled
import tm
import wlan
import time
import Tools
from machine import Timer


def timer_weather_wannianli():
    oled.Oled().weather()
    oled.Oled().wannianli()
    print(tm.tmStr())


# http://micropython.com.cn/en/latet/library/time.html
if __name__ == '__main__':

    if wlan.Wlan().connect_wifi():
        oled.Oled().start()

        tms = Timer(-1)
        tms.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: timer_weather_wannianli())

        oled.Oled().minute()
        oled.Oled().hour()
        oled.Oled().week()
        oled.Oled().month()
        oled.Oled().weather()
        oled.Oled().wannianli()
        while True:
            oled.Oled().second()
            # oled.Oled().minute()
            # oled.Oled().hour()
            # oled.Oled().week()
            # oled.Oled().month()
            time.sleep(0.2)
