#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: sg90180.py
@time: 2023/4/20 12:21
@version：Python 3.11.2
@title: sg90 180°舵机
"""
import RPi.GPIO as gpio
import time
import HCSR04

GPIO_SG = 18
gpio.setmode(gpio.BCM)
gpio.setup(GPIO_SG, gpio.OUT)
SG90_PWM = gpio.PWM(GPIO_SG, 50)
SG90_PWM.start(0)


def sg90_turn(data):
    if isinstance(data, str):  # 判断数据类型
        if data.upper() == 'STOP':
            SG90_PWM.ChangeDutyCycle(0)  # 更新占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值
        else:
            print('输入有误')
    elif isinstance(data, int) or isinstance(data, float):  # 判断数据类型
        SG90_PWM.ChangeDutyCycle(2.5 + data * 10 / 180)


def incr():
    for i in range(0, 190, 10):
        sg90_turn(i)
        print("Measured Distance = {:.2f} cm".format(HCSR04.launch()))
        time.sleep(0.5)


def decr():
    for i in range(180, -10, -10):
        sg90_turn(i)
        print("Measured Distance = {:.2f} cm".format(HCSR04.launch()))
        time.sleep(0.5)


def clear():
    SG90_PWM.stop()  # 关闭该引脚的 PWM
    gpio.cleanup()  # 清理 在退出时使用
# if __name__ == '__main__':
#     sg90_turn(0)
#     print("归零")
#     time.sleep(1)
#     incr()
#     decr()
#
#     sg90_turn('stop')
#     time.sleep(1)
#
#     SG90_PWM.stop()  # 关闭该引脚的 PWM
#     gpio.cleanup()  # 清理 在退出时使用
#     print("bye bye")
