# 点灯
from machine import Pin
from utime import sleep


class Led:
    def blingbling(self):
        pin = Pin("WL_GPIO0", Pin.OUT)
        led = 0
        while led <= 2:
            pin.toggle()
            sleep(0.5)
            led += 1
        pin.low()
