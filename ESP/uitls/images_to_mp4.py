#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: images_to_mp4.py
@time: 2023/5/20 17:00
@version：Python 3.11.2
@title: 
"""
import subprocess


def images_to_mp4(images_folder, output_file, fps):
    ffmpeg_command = [
        'ffmpeg',
        '-framerate', str(fps),
        '-i', f'{images_folder}/%d.jpg',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_file
    ]

    subprocess.run(ffmpeg_command)


# 图片文件夹路径
images_folder = 'C:\\Users\keke\dev\Raspberry-Pi\ESP\\a0b765593494'
# 输出MP4文件路径
output_file = 'images_to_video.mp4'
# 帧率（可根据需要进行修改）
fps = 6

# 将图片合成为MP4视频
images_to_mp4(images_folder, output_file, fps)
