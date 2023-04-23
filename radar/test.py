#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: test.py
@time: 2023/4/20 22:44
@version：Python 3.11.2
@title: 
"""

import radar


# def xunhuan():
#     for i in range(0, 360, 10):
#         print(12.5 - 5 * i / 360, i)


def dump(data):
    print(data == 2244)
    if data == '2244':
        radar.radar()
    print("客户端发的信息" + data)


def xunhuan():
    for i in range(180, -10, -10):
        print(i)


if __name__ == '__main__':
    xunhuan()
