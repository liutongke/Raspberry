#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: add_frame.py
@time: 2023/5/20 17:27
@version：Python 3.11.2
@title: 
"""
import subprocess


def interpolate_frames(input_file, output_file, target_fps):
    # 构建 FFmpeg 命令
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', f'minterpolate=fps={target_fps}:mi_mode=mci',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        output_file
    ]

    # 执行 FFmpeg 命令
    subprocess.run(ffmpeg_command)


# 输入的6帧视频文件
input_file = 'images_to_video.mp4'
# 输出的30帧视频文件
output_file = 'images_to_video_output.mp4'
# 目标帧率
target_fps = 30

# 将6帧视频加帧到30帧率
interpolate_frames(input_file, output_file, target_fps)
