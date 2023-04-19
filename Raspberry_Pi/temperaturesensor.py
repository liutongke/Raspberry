#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

list = []
while True:
    # 打开温度传感器文件
    file = open("/sys/bus/w1/devices/28-0317237d11ff/w1_slave")
    # 读取文件所有内容
    text = file.read()
    # 关闭文件
    file.close()
    # 用换行符分割字符串成数组，并取第二行
    secondline = text.split("\n")[1]
    # 用空格分割字符串成数组，并取最后一个，即t=23000
    temperaturedata = secondline.split(" ")[9]
    # 取t=后面的数值，并转换为浮点型
    temperature = float(temperaturedata[2:])
    # 转换单位为摄氏度
    temperature = temperature / 1000
    # 打印值
    list.append(temperature)
    print(list)
    print(temperature)
    time.sleep(30)
