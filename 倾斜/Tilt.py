#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: Tilt.py
@time: 2023/4/18 14:17
@version：Python 3.11.2
@title: 倾斜传感器模块
"""

# 导入GPIO控制薄块
import RPi.GPIO as GPIO

# 设置使用的引脚编码模式
GPIO.setmode(GPIO.BCM)
# 定义震动开关引脚 BCM
swi_shake = 18

# 进行开关引脚的初始化，设置为输入引脚，且默认为高电平
GPIO.setup(swi_shake, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 定义状态变化的回调函数
def switch_shake(channel):
    # 低电平为开关打开状态
    if not GPIO.input(channel):
        print("震动")


#  读取上升沿/下降沿
# GPIO.RISING 上升沿
# GPIO.FALLING 下降沿
# GPIO.BOTH 上升沿/下降沿
GPIO.add_event_detect(swi_shake, GPIO.FALLING, callback=switch_shake, bouncetime=200)

if __name__ == '__main__':
    try:
        while True:
            while True:
                pass
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("bye bye")
        GPIO.cleanup()
