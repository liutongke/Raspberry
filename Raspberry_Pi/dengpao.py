# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息。你可以通过下列代码禁用警告
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# 设置pin14负责输出电压
GPIO.setup(26, GPIO.OUT)
# 监控距离感应器的状态
GPIO.setup(14, GPIO.IN)
# 循环十次结束闪烁
count = 5
while (count > 0):
    if (GPIO.input(14) == int(0)):
        # 设置闪烁的函数
        # 输出1
        GPIO.output(26, GPIO.HIGH)
        time.sleep(0.5)
        # 输出0
        GPIO.output(26, GPIO.LOW)
        time.sleep(0.5)
        print ('yes')
        count = count - 1
        # 循环结束设置长亮状态
        # GPIO.output(14, GPIO.HIGH)
    else:
        print ('no')
        time.sleep(1)
        count = count - 1
# 清除进程
GPIO.cleanup()
