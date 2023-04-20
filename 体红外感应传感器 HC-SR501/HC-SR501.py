#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: HC-SR501.py
@time: 2023/4/20 13:59
@version：Python 3.11.2
@title: 红外感应模块HC-SR501 https://www.jianshu.com/p/3f612cb6bf17
"""
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_HC_SR501 = 18
GPIO.setup(GPIO_HC_SR501, GPIO.IN)


def start():
    for i in range(1, 101):
        # 如果感应器针脚输出为True，则打印信息并执行蜂鸣器函数
        if GPIO.input(GPIO_HC_SR501):
            print("Someone disclosing!")

        else:
            print("No anybody!")
        time.sleep(2)


if __name__ == '__main__':
    try:
        start()
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("bye bye")
        GPIO.cleanup()
