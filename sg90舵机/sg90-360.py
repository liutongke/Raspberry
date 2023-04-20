#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: sg90-360.py
@time: 2023/4/20 16:02
@version：Python 3.11.2
@title: sg90 360°舵机
"""
import RPi.GPIO as gpio
import time

GPIO_SG = 18
gpio.setmode(gpio.BCM)
gpio.setup(GPIO_SG, gpio.OUT)
SG90_PWM = gpio.PWM(GPIO_SG, 50)
SG90_PWM.start(0)


# 停止
def stop():
    SG90_PWM.ChangeDutyCycle(0)


# 反转
def reversal(data):
    SG90_PWM.ChangeDutyCycle(2.5 + 7.5 + data / 100)


# 正转
def forward(data):
    SG90_PWM.ChangeDutyCycle(2.5 + data / 100)


# 在0.5ms~1.5ms期间：舵机正转，时间越短，转速越快（尽量不接近1.5ms，否则有可能不转）
# 在1.5ms（1.6ms、1.4ms等）:停止转动，即速度为0
# 在1.5ms~2.5ms:舵机反转，时间越长，转速越快（尽量接近1.5ms与2.5ms，否则有可能不转）


if __name__ == '__main__':
    reversal(10)
    time.sleep(0.5)
    print("反转结束")
    stop()
    time.sleep(3)

    forward(10)
    time.sleep(0.5)
    print("正转结束")
    stop()

    SG90_PWM.stop()  # 关闭该引脚的 PWM
    gpio.cleanup()  # 清理 在退出时使用
    print("bye bye")
