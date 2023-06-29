#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: video_info.py
@time: 2023/5/20 17:57
@version：Python 3.11.2
@title: 
"""
import subprocess
import json


def get_video_info(video_path):
    # 构建FFprobe命令
    ffprobe_command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        video_path
    ]

    # 执行FFprobe命令并捕获输出
    output = subprocess.check_output(ffprobe_command).decode('utf-8')

    # 解析输出为JSON格式
    info = json.loads(output)

    # 提取视频信息
    video_info = None
    for stream in info.get('streams', []):
        if stream.get('codec_type') == 'video':
            video_info = stream
            break

    return video_info


# 获取文件时长
def get_video_duration(video_path):
    video_info = get_video_info(video_path)
    return video_info.get('duration')
# # 视频文件路径
# video_path = 'images_to_video.mp4'
#
# # 获取视频信息
# video_info = get_video_info(video_path)
#
# # 打印视频信息
# width = video_info.get('width')
# height = video_info.get('height')
# duration = video_info.get('duration')
# codec_name = video_info.get('codec_name')
#
# print(video_info)
# print('视频信息：')
# print('分辨率：{}x{}'.format(width, height))
# print('时长：{}秒'.format(duration))
# print('编码格式：{}'.format(codec_name))
