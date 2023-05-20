#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: watermark.py
@time: 2023/5/18 3:19
@version：Python 3.11.2
@title: 
"""
import cv2
import numpy as np
import time

img = cv2.imread("1.jpg")  # 导入我们需要添加水印的图片
RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
blank_img = np.zeros(shape=(RGB_img.shape[0], RGB_img.shape[1], 3), dtype=np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
# 添加水印的文字内容 org：水印放置的横纵坐标，(x坐标，y坐标) width = 800
# height = 600
text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
cv2.putText(blank_img, text=text, org=(420, 580),
            fontFace=font, fontScale=1,
            color=(255, 0, 0), thickness=2, lineType=cv2.LINE_4)
blended = cv2.addWeighted(src1=RGB_img, alpha=0.7,
                          src2=blank_img, beta=1, gamma=2)

saveFile = 'water.jpg'
cv2.imwrite(saveFile, blended)  # 保存图像文件

# cv2.imshow('image', blended)
# cv2.waitKey(0)
