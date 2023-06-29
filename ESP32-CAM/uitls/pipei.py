#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: pipei.py
@time: 2023/5/20 22:44
@version：Python 3.11.2
@title: 
"""
import subprocess
import json


def get_video_info(filename):
    # 运行 ffprobe 获取视频信息
    command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', filename]
    output = subprocess.check_output(command).decode('utf-8')

    # 解析 ffprobe 输出的 JSON 数据
    data = json.loads(output)

    return data


def get_keyframe_positions(video_info):
    keyframe_positions = []
    for stream in video_info['streams']:
        if stream['codec_type'] == 'video':
            keyframe_positions.extend(stream.get('key_frame_pos', []))

    return keyframe_positions


def are_videos_continuous(video1, video2):
    video1_info = get_video_info(video1)
    video2_info = get_video_info(video2)

    # 检查编码参数是否一致
    if video1_info['format']['format_name'] != video2_info['format']['format_name']:
        return False

    # 检查分辨率是否一致
    if video1_info['streams'][0]['width'] != video2_info['streams'][0]['width'] or \
            video1_info['streams'][0]['height'] != video2_info['streams'][0]['height']:
        return False

    # 检查帧率是否一致
    if video1_info['streams'][0]['r_frame_rate'] != video2_info['streams'][0]['r_frame_rate']:
        return False

    # 获取关键帧位置
    video1_keyframes = get_keyframe_positions(video1_info)
    video2_keyframes = get_keyframe_positions(video2_info)

    # 检查关键帧位置是否连续
    if abs(max(video1_keyframes) - min(video2_keyframes)) > 1:
        return False

    return True


# 两个 TS 视频文件路径
video1_path = 'images0.ts'
video2_path = 'images1.ts'

# 判断两个视频是否连续播放
if are_videos_continuous(video1_path, video2_path):
    print("视频可以连续播放")
else:
    print("视频u不可以连续播放")
