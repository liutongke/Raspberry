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
def radar(theta_arr, r):
    plt.clf()  # 清除上一幅图像
    plt.polar(np.array(theta_arr) * np.pi, r, marker='.', ms=2, mfc='r', mec='r',
              color='r', ls='-', lw=0.5)
    plt.ylim(0, 200)  # 设置极轴的上下限
    plt.pause(0.1)  # 暂停1秒
    plt.ioff()  # 关闭画图的窗口

# i = 1
# theta_ares = []
# rs = []
# while i:
#     theta_ares.append(i / 10)
#     rs.append(random.randint(50, 150))
#     radar(theta_ares, rs)
#     print(theta_ares)
#     i += 1
#     if i == 10:
#         i = 0
#         theta_ares = []
#         rs = []
#     if i == 20:
#         break
