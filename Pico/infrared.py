# 红外线避障模块
from machine import Pin
from utime import sleep

GPIO_IN = Pin(16, Pin.IN)

try:
    while True:
        # 当模块检测到前方障碍物信号时，电路板上绿色指示灯点亮电平，同时OUT端口持续输出低电平信号
        if GPIO_IN.value() == 0:
            print("检测到障碍")
        else:
            print("无障碍")
        sleep(0.5)
except KeyboardInterrupt:
    print('bye')
