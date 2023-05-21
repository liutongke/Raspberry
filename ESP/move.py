#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: move.py
@time: 2023/5/18 20:15
@version：Python 3.11.2
@title: 
"""

import cv2
import numpy as np

cap = cv2.VideoCapture("2023-05-18-19-26-10.mp4")  # 使用摄像头，参数为设备索引号；也可以指定视频文件路径
ret, frame = cap.read()  # 读取一帧图像
frame = cv2.resize(frame, None, fx=0.5, fy=0.5)  # 可选：调整图像大小
gray_background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
gray_background = cv2.GaussianBlur(gray_background, (21, 21), 0)  # 可选：应用高斯模糊

while True:
    ret, frame = cap.read()  # 读取一帧图像
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)  # 可选：调整图像大小
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)  # 可选：应用高斯模糊

    # 计算当前帧与背景帧的差异
    frame_delta = cv2.absdiff(gray_background, gray_frame)
    thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]

    # 执行形态学操作，去除噪声
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历检测到的轮廓
    for contour in contours:
        if cv2.contourArea(contour) < 1000:  # 可选：设置最小轮廓面积
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 显示当前帧
    cv2.imshow("Motion Detection", frame)

    # 处理键盘输入（按下'q'退出）
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理资源
cap.release()
cv2.destroyAllWindows()
