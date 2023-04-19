#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import datetime
import picamera

# 红外、超声波壁障模块
# 如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息。你可以通过下列代码禁用警告
GPIO.setwarnings(False)
# 通过红外感应控制灯泡的亮灭
GPIO.setmode(GPIO.BCM)
# gpio针脚
# 电机驱动
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22
# 超声波针脚
TRIG = 23
ECHO = 24
# 红外线针脚
IN5 = 17
IN6 = 18
IN7 = 27
IN8 = 22


# 初始化函数
def init():
    # 超声波(echo输入信号，try输出信号)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    # 电机驱动程序(输出信号)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    # 红外感应(输入信号)
    GPIO.setup(IN5, GPIO.IN)
    GPIO.setup(IN6, GPIO.IN)
    GPIO.setup(IN7, GPIO.IN)
    GPIO.setup(IN8, GPIO.IN)


# 控制轮胎方向
def up():
    # 右侧车轮前进
    GPIO.output(IN1, GPIO.HIGH)
    # 左侧车轮前进
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def down():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    # 右侧车轮后退
    GPIO.output(IN3, GPIO.HIGH)
    # 左侧车轮后退
    GPIO.output(IN4, GPIO.HIGH)


def turn_left():
    # 右侧车轮前进
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def turn_right():
    GPIO.output(IN1, GPIO.LOW)
    # 左侧车轮前进
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def ranging():
    # 首先超声波模块进行测距，如果距离过短则停止
    # 发送 trig 信号  持续 10us 的方波脉冲
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # 等待低电平结束，然后记录时间。
    while (GPIO.input(ECHO) == 0):
        pass
    pulse_start = time.time()

    # 等待高电平结束，然后记录时间。
    while (GPIO.input(ECHO) == 1):
        pass
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    # 测得距离
    distance = round(distance, 2)
    return distance


init()
while True:
    # 左侧红外线接收器
    in_left = GPIO.input(IN5)
    # 右侧红外线接收器
    in_right = GPIO.input(IN6)
    # 未遇到障碍时直行
    up()
    if in_left == int(0):
        down()
        time.sleep(1)
        turn_right()
        time.sleep(1)
        n = n - 1
        continue

    if in_right == int(0):
        down()
        time.sleep(1)
        turn_left()
        time.sleep(1)
        n = n - 1
        continue

    if in_right == int(0) & in_left == int(0):
        down()
        time.sleep(1)
        turn_right()
        time.sleep(1)
        n = n - 1
        continue
    if distance < int(5):
        # 如果小于5厘米，调用程序后退
        pass
    else:
        pass
        # 这里对程序的红外感应器进行判断

# 清空GPIO接口配置信息
GPIO.cleanup()
