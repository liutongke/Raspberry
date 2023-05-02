#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: TTP223.py
@time: 2023/4/24 19:44
@version：Python 3.11.2
@title: 
"""
import time

import RPi.GPIO as GPIO

TouchPin = 21


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TouchPin, GPIO.IN)


def loop():
    while True:
        if GPIO.input(TouchPin) == 1:
            print('Touch ON')
        time.sleep(0.1)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
