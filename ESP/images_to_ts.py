#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: images_to_ts.py
@time: 2023/5/20 17:34
@version：Python 3.11.2
@title: 
"""
import subprocess


def images_to_ts(images_folder, output_file, fps=25):
    # 构建 FFmpeg 命令
    ffmpeg_command = [
        'ffmpeg',
        '-framerate', str(fps),
        '-i', f'{images_folder}/%d.jpg',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        '-f', 'mpegts',
        output_file
    ]

    # 执行 FFmpeg 命令
    subprocess.run(ffmpeg_command)


# 输入的图片文件名模式（例如，img-%d.jpg 表示以 img- 为前缀，后面是递增的数字）
# images_folder = 'C:\\Users\keke\dev\Raspberry-Pi\ESP\\a0b765593494'
# # 输出的 TS 文件名
# output_file = 'output.ts'
# # 视频的帧率（可根据需要进行修改，默认为25）
# fps = 6
#
# # 将图片转换为 TS 格式的视频
# images_to_ts(images_folder, output_file, fps)
