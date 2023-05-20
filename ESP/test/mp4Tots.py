#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: mp4Tots.py
@time: 2023/5/20 2:06
@version：Python 3.11.2
@title: 
"""
import subprocess
import json
import time
import os

def sort_files_by_number(files):
    def extract_number(filename):
        # 提取文件名中的数字部分
        basename = os.path.basename(filename)
        number = ''.join(filter(str.isdigit, basename))
        return int(number)

    # 使用自定义函数提取数字并进行比较排序
    sorted_files = sorted(files, key=extract_number)
    return sorted_files

# 设置文件夹路径
# folder_path = 'C:\\Users\keke\dev\Raspberry-Pi\ESP\\test\\1'
#
# # 获取文件夹中的所有文件
# files = os.listdir(folder_path)
#
# # 按照数字大小递增排序文件
# sorted_files = sort_files_by_number(files)
#
# # 打印排序后的文件名
# for file in sorted_files:
#     print(file)
# exit()


def images_to_ts(images_folder, output_path, fps=25):
    print(images_folder)
    # 按照数字大小递增排序文件
    sorted_files = sort_files_by_number(images_folder)

    ffmpeg_command = [
        'ffmpeg',
        '-framerate', str(fps),
        '-i', sorted_files[0],
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        '-f', 'mpegts',
        output_path
    ]  # 构建FFmpeg命令

    # 执行FFmpeg命令
    subprocess.run(ffmpeg_command)
    return get_video_info(output_path)


def get_video_info(video_file):
    ffprobe_cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', video_file]
    result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)

    output = result.stdout
    info = json.loads(output)

    # 提取视频信息
    video_info = None
    for stream in info.get('streams', []):
        if stream.get('codec_type') == 'video':
            video_info = stream
            break

    return video_info


def get_all_folders():
    current_dir = os.getcwd()  # 获取当前目录
    items = os.listdir(current_dir)  # 获取当前目录下的所有文件和文件夹
    folders = [item for item in items if os.path.isdir(os.path.join(current_dir, item))]  # 过滤出文件夹
    return folders


# 调用函数获取当前目录下的所有文件夹
folders = get_all_folders()

# 打印所有文件夹名字
for folder in folders:
    # 图片文件夹路径
    images_folder = f'C:\\Users\keke\dev\Raspberry-Pi\ESP\\test\\{folder}'
    # tm = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    # 输出TS文件路径
    output_path = 'output_%s.ts' % folder
    # 帧率（可根据需要进行修改，默认为25）
    fps = 6

    # 将图片合成TS文件
    video_info = images_to_ts(images_folder, output_path, fps)
    if video_info:
        width = video_info.get('width')
        height = video_info.get('height')
        duration = video_info.get('duration')
        codec_name = video_info.get('codec_name')

        print('视频信息：')
        print('分辨率：{}x{}'.format(width, height))
        print('时长：{}秒'.format(duration))
        print('编码格式：{}'.format(codec_name))
    else:
        print('无法获取视频信息。')

# def generate_m3u8(file_path, segments, target_duration):
#     with open(file_path, 'w') as f:
#         f.write("#EXTM3U\n")
#         f.write("#EXT-X-VERSION:3\n")
#         f.write("#EXT-X-TARGETDURATION:{}\n".format(target_duration))
#         f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
#
#         for i, segment in enumerate(segments):
#             segment_filename = segment['filename']
#             segment_duration = segment['duration']
#             f.write("#EXTINF:{},\n".format(segment_duration))
#             f.write("{}\n".format(segment_filename))
#
#         f.write("#EXT-X-ENDLIST\n")
#
#
# # 示例用法
# segments = [
#     {'filename': 'segment_0.ts', 'duration': 10.0},
#     {'filename': 'segment_1.ts', 'duration': 10.0},
#     {'filename': 'segment_2.ts', 'duration': 10.0}
# ]
# target_duration = 10
#
# generate_m3u8('playlist.m3u8', segments, target_duration)
