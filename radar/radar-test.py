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
import random
import matplotlib.pyplot as plt

# https://zhuanlan.zhihu.com/p/37104717
# https://blog.csdn.net/qq_43511299/article/details/113781883
# https://www.bilibili.com/bangumi/play/ep50790?spm_id_from=333.337.0.0&from_spmid=666.25.player.continue
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
#
#
# radar()

dict_ = {
    'r': [243.67, 63.16, 55.01, 55.85, 55.02, 54.98, 56.06, 57.77, 55.79, 59.98, 220.65, 54.96,
          57.67, 57.87, 87.86, 220.56, 57.62, 167.46, 56.51],
    'theta_arr': [1.0, 0.9444444444444445, 0.888888888888889, 0.8333333333333335, 0.7777777777777778, 0.7222222222222223, 0.6666666666666667, 0.6111111111111112, 0.5555555555555556, 0.5, 0.4444444444444445, 0.3888888888888889, 0.33333333333333337, 0.2777777777777778, 0.22222222222222224, 0.16666666666666669, 0.11111111111111112, 0.05555555555555556, 0.0]}

plt.clf()  # 清除上一幅图像
plt.polar(np.array(dict_['theta_arr']) * np.pi, dict_['r'], marker='.', ms=2, mfc='r', mec='r',
          color='r', ls='-', lw=0.5)
plt.ylim(0, 200)  # 设置极轴的上下限
plt.pause(10)  # 暂停1秒
plt.ioff()  # 关闭画图的窗口
# {'r': ['243.67', '63.16', '55.01', '55.85', '55.02', '54.98', '56.06', '57.77', '55.79', '59.98', '220.65', '54.96', '57.67', '57.87', '87.86', '220.56', '57.62', '167.46', '56.51'], 'theta_arr': [1.0, 0.9444444444444445, 0.888888888888889, 0.8333333333333335, 0.7777777777777778, 0.7222222222222223, 0.6666666666666667, 0.6111111111111112, 0.5555555555555556, 0.5, 0.4444444444444445, 0.3888888888888889, 0.33333333333333337, 0.2777777777777778, 0.22222222222222224, 0.16666666666666669, 0.11111111111111112, 0.05555555555555556, 0.0]}
