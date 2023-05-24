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
