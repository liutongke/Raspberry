#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: cpu_temp.py
@time: 2023/4/16 22:26
@version：Python 3.11.2
@title: 查看CPU温度
"""

import time

try:
    while True:
        # 打开文件
        file = open("/sys/class/thermal/thermal_zone0/temp")
        # 读取结果，并转换为浮点数
        temp = float(file.read()) / 1000
        # 关闭文件
        file.close()
        print("cpu温度:", temp)
        time.sleep(1)
    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("bye bye")
