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
import os


def sort_photos_by_filename(folder_path):
    # 获取文件夹中的所有照片文件
    photo_files = [
        file for file in os.listdir(folder_path)
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ]

    # 按照文件名递增排序
    sorted_files = sorted(photo_files, key=lambda x: int(os.path.splitext(x)[0]))

    return sorted_files


def images_to_ts(images_folder, output_path, fps=6):
    # 构建FFmpeg命令
    ffmpeg_command = [
        'ffmpeg',
        '-framerate', str(fps),
        '-i', f'{images_folder}/%d.jpg',  # 文件名顺序递增，出示范围0-4
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        '-f', 'mpegts',
        output_path
    ]

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
segments = []
n = 0
# 打印所有文件夹名字
for folder in folders:
    # 图片文件夹路径
    images_folder = f'C:\\Users\keke\dev\Raspberry-Pi\ESP\\test\\tests\\{folder}'
    # tm = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    # 输出TS文件路径
    output_path = 'jiankong%s.ts' % str(n)
    n += 1
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
        segments.append({'filename': output_path, 'duration': duration})
    else:
        print('无法获取视频信息。')


def generate_m3u8(file_path, segments, target_duration):
    with open(file_path, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXT-X-TARGETDURATION:{}\n".format(target_duration))
        f.write("#EXT-X-MEDIA-SEQUENCE:0\n")

        for i, segment in enumerate(segments):
            segment_filename = segment['filename']
            segment_duration = segment['duration']
            f.write("#EXTINF:{},\n".format(segment_duration))
            f.write("{}\n".format(segment_filename))

        f.write("#EXT-X-ENDLIST\n")


# 示例用法
# segments = [
#     {'filename': 'segment_0.ts', 'duration': 10.0},
#     {'filename': 'segment_1.ts', 'duration': 10.0},
#     {'filename': 'segment_2.ts', 'duration': 10.0}
# ]
target_duration = 55

generate_m3u8('jiankong.m3u8', segments, target_duration)
