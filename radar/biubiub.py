#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: biubiub.py
@time: 2023/4/22 15:46
@version：Python 3.11.2
@title: 
"""
import numpy as np
import random
import matplotlib.pyplot as plt

# https://zhuanlan.zhihu.com/p/37104717
# https://blog.csdn.net/qq_43511299/article/details/113781883
# https://www.bilibili.com/bangumi/play/ep50790?spm_id_from=333.337.0.0&from_spmid=666.25.player.continue

try:
    i = 0
    theta_arr = []
    r = []
    while True:

        plt.clf()  # 清除上一幅图像
        # theta_arr.append(random.random())
        theta_arr.append(i / 100)
        r.append(random.randint(100, 200))
        # print(theta_arr, r)
        theta = np.array(theta_arr)

        # theta = np.array([random.random()])
        # r = [random.randint(50, 150)]
        plt.polar(theta * np.pi, r, marker='.', ms=2, mfc='r', mec='r',
                  color='r', ls='-', lw=0.5)
        plt.ylim(0, 200)  # 设置极轴的上下限
        plt.pause(0.1)  # 暂停1秒
        plt.ioff()  # 关闭画图的窗口

        print(i)
        i += 1
        if i == 100:
            i = 0
            theta_arr = []
            r = []
except KeyboardInterrupt:
    print("bye bye")
