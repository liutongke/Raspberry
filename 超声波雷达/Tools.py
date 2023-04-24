#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: Tools.py
@time: 2023/4/23 20:38
@version：Python 3.11.2
@title: 
"""
import json


def json_decode(json_dict_):
    return json.loads(json_dict_)


def json_encode(dict_):
    return json.dumps(dict_, indent=2, sort_keys=True, ensure_ascii=False)


# 角度换算
# plt.polar 0°到180° <=====> 0-1
def angle_conversion(angle):
    return (angle / 18) * 0.1
    # return format((angle / 18) * 0.1, ".2f")


def float_str(distance):
    # print("Measured Distance = {:.2f} cm".format(HCSR04.launch()))
    return distance
    # return format(distance, ".2f")
