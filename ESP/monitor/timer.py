#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: timer.py
@time: 2023/5/26 21:37
@version：Python 3.11.2
@title: 
"""
import schedule
import time
import subprocess
from natsort import natsorted
import os
import cv2
import datetime
import tools
import config


def job():
    # 在这里编写你要执行的任务代码
    print("执行定时任务")

    for device_id, value in config.cam_param().items():
        folder_path = f'{os.getcwd()}/images/{device_id}/{tools.get_prev_hour_id()}'
        # print(folder_path)
        # print(os.path.exists(folder_path))
        if os.path.exists(folder_path):
            mp4_path = f'video/{device_id}/{tools.get_prev_hour_id()}.mp4'
            if tools.mkdirs(tools.get_dir_path(mp4_path)):
                images_to_video(folder_path, mp4_path, 6)


# 定义整点执行任务的函数
def run_task():
    # 获取当前时间
    current_time = time.strftime("%H:%M", time.localtime())
    print(current_time)
    # 判断当前时间是否为整点，如果是，则执行任务,图片合成视频，每个小时执行一次即可
    if current_time.endswith(":01"):
        job()


def images_to_video(image_folder, output_file, fps=6):
    # 获取输入文件夹中的所有照片文件，并按照文件名排序
    image_files = natsorted([f for f in os.listdir(image_folder) if f.endswith(".jpg")])

    # 读取第一张图片，获取图片的宽度和高度
    first_image = cv2.imread(os.path.join(image_folder, image_files[0]))
    height, width, _ = first_image.shape

    # 创建视频写入器对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用指定的编解码器（此处为 MP4）
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # 遍历排序后的图片列表，将每张图片写入视频帧中
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        video_writer.write(image)

    # 释放视频写入器对象
    video_writer.release()


def main():
    print("启动定时任务")
    # 使用 schedule 模块来设置每分钟执行一次 run_task() 函数
    schedule.every(1).minutes.do(run_task)

    # 无限循环执行任务
    while True:
        schedule.run_pending()
        time.sleep(1)

# if __name__ == '__main__':
#     current_time = time.strftime("%H:%M", time.localtime())
#     print(current_time)
