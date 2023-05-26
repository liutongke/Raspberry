#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: tools.py
@time: 2023/5/23 21:05
@version：Python 3.11.2
@title: 
"""
import re
import datetime
import os


# true存在 false不存在
def dict_key_exist(key, _dict):
    return key in _dict
    # my_dict = {'key1': 1, 'key2': 2, 'key3': 3}
    # if 'key1' in my_dict:
    #     print("key1存在")
    # if 'key4' not in my_dict:
    #     print("key4不存在")


def dd():
    pass


def log(text):
    with open("./filename.txt", "a") as file:
        file.write(f"{text}\n")


def is_hex(s):
    pattern = r'^[0-9a-fA-F]+$'
    return bool(re.match(pattern, s))


def get_tm_str():
    from datetime import datetime

    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


# 获取当前小时id
def get_now_hour_id() -> str:
    # 获取当前时间
    current_time = datetime.datetime.now()

    # 获取当前小时
    current_hour = current_time.strftime("%Y%m%d%H")

    return current_hour


# 获取上一个小时的id
def get_prev_hour_id() -> str:
    # 获取当前时间
    current_time = datetime.datetime.now()

    # 获取上一个小时的时间
    previous_hour = current_time - datetime.timedelta(hours=1)

    # 输出上一个小时的时间
    # print(previous_hour)

    # 格式化上一个小时的时间
    formatted_time = previous_hour.strftime("%Y%m%d%H")

    # 输出格式化后的时间
    # print(formatted_time)
    return formatted_time


def get_dir_path(file_path: str) -> str:
    # 使用 os.path.dirname() 获取文件所在目录的路径
    directory_path = os.path.dirname(file_path)
    return directory_path


def mkdir(filename: str):
    if not os.path.exists(filename):  # 判断所在目录下是否有该文件名的文件夹
        os.mkdir(filename)  # 创建多级目录用mkdirs，单击目录mkdir


def mkdirs(path: str) -> bool:
    # 验证目录是否创建成功
    if not os.path.isdir(path):
        # 使用 os.makedirs() 创建多级目录
        os.makedirs(path)
    return True
