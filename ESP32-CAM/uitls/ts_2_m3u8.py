#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: ts_2_m3u8.py
@time: 2023/5/20 19:46
@version：Python 3.11.2
@title: 
"""
import os
import video_info


def generate_m3u8(folder_path, output_file, segment_duration, sequence):
    with open(output_file, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write(f"#EXT-X-MEDIA-SEQUENCE:{sequence}\n")
        f.write("#EXT-X-TARGETDURATION:{:.1f}\n".format(segment_duration))

        # 遍历文件夹中的文件
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.ts'):
                    file_list.append(os.path.join(root, file_name))

        # 按文件名排序
        file_list.sort()

        segment_index = 0
        for file_path in file_list:
            segment_index += 1
            segment_url = os.path.basename(file_path)
            f.write(f"#EXTINF:{video_info.get_video_duration(file_path)},\n")
            f.write(segment_url + "\n")


# 指定文件夹路径、输出文件路径和分片时长
# folder_path = './'
# output_file = './output.m3u8'
# segment_duration = 16.0  # 分片时长（秒）
# sequence = 1  # 当前播放定位
# 生成规范的 M3U8 文件
# generate_m3u8('./', 'C:\\Users\\keke\\dev\\Raspberry-Pi\\ESP\\test\\video/output.m3u8', 16.0, sequence)
