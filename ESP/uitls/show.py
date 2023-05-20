#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: show.py
@time: 2023/5/20 20:38
@version：Python 3.11.2
@title: 
"""
import os
import subprocess

# 文件夹路径
folder_path = 'images0/'

# 时间戳文件路径
timestamps_file = 'timestamps0.txt'

# 输出的 TS 视频文件路径
output_file = 'images0.ts'

# 读取时间戳信息
with open(timestamps_file, 'r') as file:
    timestamps = [line.strip() for line in file]

# 遍历文件夹下的图片文件
image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
input_files = [os.path.join(folder_path, f) for f in image_files]
print(image_files, len(image_files))
print(timestamps, len(timestamps))
# 构建 FFmpeg 命令
ffmpeg_cmd = [
    'ffmpeg',
    '-framerate', '10',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'pipe:',
    '-vf', f"setpts='{'|'.join(timestamps)}'",
    '-c:v', 'libx264',
    '-crf', '23',
    '-pix_fmt', 'yuv420p',
    output_file
]

# 执行 FFmpeg 命令
ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

# 将图片文件内容写入 FFmpeg 进程的标准输入
for input_file in input_files:
    with open(input_file, 'rb') as file:
        ffmpeg_process.stdin.write(file.read())

# 关闭 FFmpeg 进程的标准输入，等待命令执行完成
ffmpeg_process.stdin.close()
ffmpeg_process.wait()

print('TS 视频生成完成。')
