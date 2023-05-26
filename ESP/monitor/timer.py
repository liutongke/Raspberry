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


def job():
    # 在这里编写你要执行的任务代码
    print("执行定时任务")
    images_to_video('/var/www/html/monitor/a0b765593494', '/var/www/html/monitor/output.mp4', 6)


# 定义整点执行任务的函数
def run_task():
    # 获取当前时间
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(current_time)
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
    # 使用 schedule 模块来设置每分钟执行一次 run_task() 函数
    schedule.every(1).minutes.do(run_task)

    # 无限循环执行任务
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    import os

    # 使用 os.getcwd() 获取当前目录
    current_directory = os.getcwd()
    device_id = "123"
    path = f'{device_id}/{tools.get_prev_hour_id()}/'
    os.makedirs(path)
    # 打印当前目录
    print("当前目录：", path, current_directory)

    import os

    file_path = "/html/monitor/1.jpg"



    # 打印目录路径
    print("目录路径：", directory_path)
