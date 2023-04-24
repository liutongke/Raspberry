#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: leida.py
@time: 2023/4/22 1:36
@version：Python 3.11.2
@title: 
"""
# 导入第三方模块
import numpy as np
import matplotlib.pyplot as plt


# https://zhuanlan.zhihu.com/p/37104717
# https://blog.csdn.net/qq_43511299/article/details/113781883
def radar(theta_arr, r):
    plt.clf()  # 清除上一幅图像
    plt.polar(np.array(theta_arr) * np.pi, r, marker='.', ms=10, mfc='r', mec='r',
              color='r', ls='None', lw=0.5)
    plt.ylim(0, 100)  # 设置极轴的上下限
    plt.pause(0.1)  # 暂停1秒
    plt.ioff()  # 关闭画图的窗口

# def radar():
#     try:
#         i = 0
#         theta_arr = []
#         r = []
#         while True:
#
#             plt.clf()  # 清除上一幅图像
#             # theta_arr.append(random.random())
#             theta_arr.append(i / 10)
#             r.append(random.randint(50, 150))
#             # print(theta_arr, r)
#             theta = np.array(theta_arr)
#
#             # theta = np.array([random.random()])
#             # r = [random.randint(50, 150)]
#             plt.polar(theta * np.pi, r, marker='.', ms=2, mfc='r', mec='r',
#                       color='r', ls='-', lw=0.5)
#             plt.ylim(0, 200)  # 设置极轴的上下限
#             plt.pause(1)  # 暂停1秒
#             plt.ioff()  # 关闭画图的窗口
#
#             print(i)
#             i += 1
#             if i == 10:
#                 i = 0
#                 theta_arr = []
#                 r = []
#     except KeyboardInterrupt:
#         print("bye bye")
#         exit()
