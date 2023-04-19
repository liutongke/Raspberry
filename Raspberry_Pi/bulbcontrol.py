# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息。你可以通过下列代码禁用警告
GPIO.setwarnings(False)
# 通过红外感应控制灯泡的亮灭
GPIO.setmode(GPIO.BCM)
# 设置pin14负责输出电压
GPIO.setup(18, GPIO.OUT)
# 设置pin14负责接收红外感应
GPIO.setup(14, GPIO.IN)
n = 5
while n > 0:
    if GPIO.input(14) == int(0):
        # 如果为真则亮灯
        # print('liang')
        GPIO.output(18, GPIO.HIGH)
        time.sleep(2)
        n = n - 1
        print('灯亮')
    else:
        # 如果为假则灭灯
        GPIO.output(18, GPIO.LOW)
        time.sleep(2)
        n = n - 1
        print('灯灭')
# 清除进程
GPIO.cleanup()
