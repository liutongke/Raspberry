from utime import sleep
from machine import Pin
import utime

try:
    TTP223_PIN = 16
    GPIO_PIN = Pin(TTP223_PIN, Pin.IN)

    led = Pin('WL_GPIO0', Pin.OUT)  # 板载LED连到WL_GPIO0
    led.value(0)

    print("start touch")
    while True:
        touch = GPIO_PIN.value()
        if touch == 1:
            led.toggle()
            print('Touch ON')
        sleep(1)

except KeyboardInterrupt:
    print('bye')
