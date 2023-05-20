#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: mp4_to_m3u8.py
@time: 2023/5/20 17:04
@version：Python 3.11.2
@title: 
"""
import subprocess
import os


def split_mp4_to_ts(input_file, output_folder, segment_duration):
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-f', 'segment',
        '-segment_time', str(segment_duration),
        '-segment_format', 'mpegts',
        f'{output_folder}/segment_%d.ts'
    ]

    subprocess.run(ffmpeg_command)


def generate_m3u8_file(output_folder, segment_duration):
    m3u8_file = f'{output_folder}/playlist.m3u8'

    with open(m3u8_file, 'w') as f:
        f.write('#EXTM3U\n')
        f.write(f'#EXT-X-VERSION:3\n')
        f.write(f'#EXT-X-TARGETDURATION:{segment_duration + 1}\n')
        f.write(f'#EXT-X-MEDIA-SEQUENCE:0\n')

        for file_name in sorted(os.listdir(output_folder)):
            if file_name.endswith('.ts'):
                f.write(f'#EXTINF:{segment_duration},\n')
                f.write(f'{file_name}\n')

        f.write('#EXT-X-ENDLIST\n')


# 输入MP4文件路径
input_file = './test.mp4'
# 输出TS分段文件存储文件夹路径
output_folder = 'C:\\Users\keke\dev\Raspberry-Pi\ESP\\ts'
# 分段时长（单位：秒）
segment_duration = 10

# 将MP4视频切分为TS分段
split_mp4_to_ts(input_file, output_folder, segment_duration)

# 生成M3U8文件
generate_m3u8_file(output_folder, segment_duration)
