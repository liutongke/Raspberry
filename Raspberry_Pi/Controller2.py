#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" 
@author:keke 
@file: Controller.py 
@time: 2019/04/27 
"""
# 》》》》》》》》》》》》》》》》》》》》超声波测距控制结束

import picamera
import RPi.GPIO as GPIO  # 引入RPi.GPIO库函数命名为GPIO
import time  # 引入计时time函数

# 》》》》》》》》》》》》》》》》》》》》红外传感器
# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BOARD)  # 将GPIO编程方式设置为BOARD模式
# 输出模式
IN5 = 40
GPIO.setup(IN5, GPIO.IN)  # 将GPIO引脚37设置为输入引脚

i = 0
while i < 10:
    InputRes = GPIO.input(IN5)
    print(InputRes)
    time.sleep(0.5)
    i = i + 1
# 》》》》》》》》》》》》》》》》》》》》红外传感器结束
exit()

# 》》》》》》》》》》》》》》》》》》》》超声波测距控制结束

import picamera
import RPi.GPIO as GPIO  # 引入RPi.GPIO库函数命名为GPIO
import time  # 引入计时time函数

# 》》》》》》》》》》》》》》》》》》》》LED灯控制
# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BOARD)  # 将GPIO编程方式设置为BOARD模式
# 输出模式
GPIO.setup(37, GPIO.OUT)  # 将GPIO引脚37设置为输出引脚
GPIO.setup(40, GPIO.OUT)  # 将GPIO引脚40设置为输出引脚

while True:  # 条件为真，下面程序一直循环执行
    GPIO.output(37, GPIO.HIGH)  # 将11引脚电压置高，点亮LED灯
    time.sleep(0.5)  # 延时1秒
    GPIO.output(37, GPIO.LOW)  # 将11引脚电压置低，熄灭LED灯
    time.sleep(0.5)
    GPIO.output(40, GPIO.HIGH)  # 将11引脚电压置高，点亮LED灯
    time.sleep(0.5)  # 延时1秒
    GPIO.output(40, GPIO.LOW)  # 将11引脚电压置低，熄灭LED灯
    time.sleep(0.5)
# 》》》》》》》》》》》》》》》》》》》》LED灯控制结束
exit()

# 导入 GPIO库
import RPi.GPIO as GPIO
import time

# 》》》》》》》》》》》》》》》》》》》》超声波测距控制开始
# 设置 GPIO 模式为 BCM
GPIO.setmode(GPIO.BCM)

# 定义 GPIO 引脚
GPIO_TRIGGER = 26
GPIO_ECHO = 21

# 设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # 发送高电平信号到 Trig 引脚
    GPIO.output(GPIO_TRIGGER, True)

    # 持续 10 us
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # 记录发送超声波的时刻1
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # 记录接收到返回超声波的时刻2
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # 计算超声波的往返时间 = 时刻2 - 时刻1
    time_elapsed = stop_time - start_time
    # 声波的速度为 343m/s， 转化为 34300cm/s。
    distance = (time_elapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print("Measured Distance = {:.2f} cm".format(dist))
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
exit()

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)
pwm_led = gpio.PWM(18, 500)
pwm_led.start(0)
print('pwm start')
try:
    while True:
        for i in range(0, 100):
            pwm_led.ChangeDutyCycle(i)
            time.sleep(0.05)
        for i in range(100, 0):
            pwm_led.ChangeDutyCycle(i)
            time.sleep(0.05)
except KeyboardInterrupt:
    pwm_led.stop()
    gpio.cleanup()
    print('pwm stop and gpio clean up by ctrl + c')
    exit()
# 初始化
camera = picamera.PiCamera()
sleep(3)
# 捕获图像
camera.capture('image123.jpg')
# 打开预览
# camera.start_preview()
# 垂直翻转
# camera.vflip = True
# 水平翻转
# camera.hflip = True
# 控制摄像头亮度
# camera.brightness = 60
# 控制摄像头录像
# camera.start_recording('video.mp4')
# 程序休眠，但摄像头继续工作
# sleep(5)
# 停止录像
# camera.stop_recording()
# 也可以这样用：预览摄像头在不同亮度下的变化情况。
# for i in range(100):
#     camera.brightness = i
#     sleep(0.1)
