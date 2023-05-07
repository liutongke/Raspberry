#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: tm.py
@time: 2023/5/7 13:00
@version：Python 3.11.2
@title: 设置时区
Usage (assuming a network connection):
from getNow import getNow
print(getNow(UTC_OFFSET=-5))
(2022, 12, 12, 10, 34, 34, 0, 346)
https://github.com/orgs/micropython/discussions/9545
"""

import time
import ntptime

try:
    ntptime.settime()
except:
    raise Exception("npttime.settime() failed. No network connection.")


def getNow(UTC_OFFSET=-5):
    return time.gmtime(time.time() + UTC_OFFSET * 3600)
