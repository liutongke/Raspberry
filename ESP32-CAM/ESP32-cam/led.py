#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: led.py
@time: 2023/5/15 19:33
@version：Python 3.11.2
@title: 
"""
from machine import Pin
import time

led = Pin(4, Pin.OUT)


def open_led():
    return led.value(1)


def close_led():
    return led.value(0)


open_led()
time.sleep(1)
close_led()
