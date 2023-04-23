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
