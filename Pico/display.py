#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: main.py
@time: 2023/4/27 21:20
@version：Python 3.11.2
@title: 
"""
from machine import Pin
from utime import sleep
import network
import socket
import json
import time
import lightsensitive
import machine
import ssd1306
import wlan
import machine
import utime
import pcf8591
import Tools
import urequests as requests

fonts = {
    0xE59F8E: [0x20, 0x20, 0x20, 0x27, 0x24, 0xFC, 0x24, 0x27, 0x24, 0x24, 0x24, 0x3C, 0xE6, 0x49, 0x08, 0x10, 0x28,
               0x24, 0x20, 0xFE, 0x20, 0x20, 0x24, 0xA4, 0xA4, 0xA8, 0xA8, 0x90, 0x92, 0x2A, 0x46, 0x82],  # 城

    0xE5B882: [0x02, 0x01, 0x00, 0x7F, 0x01, 0x01, 0x01, 0x3F, 0x21, 0x21, 0x21, 0x21, 0x21, 0x21, 0x01, 0x01, 0x00,
               0x00, 0x00, 0xFC, 0x00, 0x00, 0x00, 0xF8, 0x08, 0x08, 0x08, 0x08, 0x28, 0x10, 0x00, 0x00],  # /*"市",1*/

    0xE5AE9E: [0x02, 0x01, 0x7F, 0x40, 0x88, 0x04, 0x04, 0x10, 0x08, 0x08, 0xFF, 0x01, 0x02, 0x04, 0x18, 0x60, 0x00,
               0x00, 0xFE, 0x02, 0x84, 0x80, 0x80, 0x80, 0x80, 0x80, 0xFE, 0x40, 0x20, 0x10, 0x08, 0x04],  # /*"实",2*/

    0xE697B6: [0x00, 0x00, 0x7C, 0x44, 0x45, 0x44, 0x44, 0x7C, 0x44, 0x44, 0x44, 0x44, 0x7C, 0x44, 0x00, 0x00, 0x08,
               0x08, 0x08, 0x08, 0xFE, 0x08, 0x08, 0x08, 0x88, 0x48, 0x48, 0x08, 0x08, 0x08, 0x28, 0x10],  # /*"时",3*/

    0xE5A4A9: [0x00, 0x3F, 0x01, 0x01, 0x01, 0x01, 0xFF, 0x01, 0x02, 0x02, 0x04, 0x04, 0x08, 0x10, 0x20, 0xC0, 0x00,
               0xF8, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x00, 0x80, 0x80, 0x40, 0x40, 0x20, 0x10, 0x08, 0x06],  # /*"天",4*/

    0xE6B094: [0x10, 0x10, 0x3F, 0x20, 0x4F, 0x80, 0x3F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
               0x00, 0xFC, 0x00, 0xF0, 0x00, 0xF0, 0x10, 0x10, 0x10, 0x10, 0x10, 0x0A, 0x0A, 0x06, 0x02],  # /*"气",5*/

    0xE6B8A9: [0x00, 0x23, 0x12, 0x12, 0x83, 0x42, 0x42, 0x13, 0x10, 0x27, 0xE4, 0x24, 0x24, 0x24, 0x2F, 0x00, 0x00,
               0xF8, 0x08, 0x08, 0xF8, 0x08, 0x08, 0xF8, 0x00, 0xFC, 0xA4, 0xA4, 0xA4, 0xA4, 0xFE, 0x00],  # /*"温",6*/

    0xE7A9BA: [0x02, 0x01, 0x7F, 0x40, 0x88, 0x10, 0x20, 0x00, 0x1F, 0x01, 0x01, 0x01, 0x01, 0x01, 0x7F, 0x00, 0x00,
               0x00, 0xFE, 0x02, 0x24, 0x10, 0x08, 0x00, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFC, 0x00],  # /*"空",7*/

    0xE6B9BF: [0x00, 0x27, 0x14, 0x14, 0x87, 0x44, 0x44, 0x17, 0x11, 0x21, 0xE9, 0x25, 0x23, 0x21, 0x2F, 0x00, 0x00,
               0xF8, 0x08, 0x08, 0xF8, 0x08, 0x08, 0xF8, 0x20, 0x20, 0x24, 0x28, 0x30, 0x20, 0xFE, 0x00],  # /*"湿",8*/

    0xE5BAA6: [0x01, 0x00, 0x3F, 0x22, 0x22, 0x3F, 0x22, 0x22, 0x23, 0x20, 0x2F, 0x24, 0x42, 0x41, 0x86, 0x38, 0x00,
               0x80, 0xFE, 0x20, 0x20, 0xFC, 0x20, 0x20, 0xE0, 0x00, 0xF0, 0x10, 0x20, 0xC0, 0x30, 0x0E],  # /*"度",9*/

    0xE9A38E: [0x00, 0x3F, 0x20, 0x20, 0x28, 0x24, 0x22, 0x22, 0x21, 0x21, 0x22, 0x22, 0x24, 0x48, 0x40, 0x80, 0x00,
               0xF0, 0x10, 0x10, 0x50, 0x50, 0x90, 0x90, 0x10, 0x10, 0x90, 0x92, 0x4A, 0x4A, 0x06, 0x02],  # /*"风",10*/

    0xE59091: [0x02, 0x04, 0x08, 0x7F, 0x40, 0x40, 0x47, 0x44, 0x44, 0x44, 0x44, 0x47, 0x44, 0x40, 0x40, 0x40, 0x00,
               0x00, 0x00, 0xFC, 0x04, 0x04, 0xC4, 0x44, 0x44, 0x44, 0x44, 0xC4, 0x44, 0x04, 0x14, 0x08],  # /*"向",11*/

    0xE58A9B: [0x02, 0x02, 0x02, 0x02, 0x7F, 0x02, 0x02, 0x02, 0x02, 0x04, 0x04, 0x08, 0x08, 0x10, 0x20, 0x40, 0x00,
               0x00, 0x00, 0x00, 0xF8, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x88, 0x50, 0x20],  # /*"力",12*/

    0xE7BAA7: [0x10, 0x13, 0x20, 0x20, 0x48, 0xF8, 0x10, 0x20, 0x41, 0xF9, 0x41, 0x01, 0x1A, 0xE2, 0x44, 0x01, 0x00,
               0xFC, 0x84, 0x88, 0x88, 0x90, 0x9C, 0x84, 0x44, 0x44, 0x28, 0x28, 0x10, 0x28, 0x44, 0x82],  # /*"级",13*/

    0xE588AB: [0x00, 0x7F, 0x41, 0x41, 0x41, 0x7F, 0x10, 0x10, 0xFF, 0x11, 0x11, 0x11, 0x21, 0x21, 0x4A, 0x84, 0x04,
               0x04, 0x04, 0x24, 0x24, 0x24, 0x24, 0x24, 0x24, 0x24, 0x24, 0x24, 0x04, 0x04, 0x14, 0x08],  # /*"别",14*/

    0xE58F91: [0x01, 0x11, 0x11, 0x22, 0x3F, 0x02, 0x04, 0x07, 0x0A, 0x09, 0x11, 0x10, 0x20, 0x40, 0x03, 0x1C, 0x00,
               0x10, 0x08, 0x00, 0xFC, 0x00, 0x00, 0xF8, 0x08, 0x08, 0x10, 0xA0, 0x40, 0xA0, 0x18, 0x06],  # /*"发",15*/

    0xE5B883: [0x02, 0x02, 0x02, 0xFF, 0x04, 0x09, 0x11, 0x3F, 0x51, 0x91, 0x11, 0x11, 0x11, 0x11, 0x01, 0x01, 0x00,
               0x00, 0x00, 0xFE, 0x00, 0x00, 0x00, 0xF8, 0x08, 0x08, 0x08, 0x08, 0x28, 0x10, 0x00, 0x00],  # /*"布",16*/

    0xE59CB0: [0x10, 0x10, 0x10, 0x11, 0x11, 0xFD, 0x11, 0x13, 0x11, 0x11, 0x11, 0x1D, 0xE1, 0x41, 0x00, 0x00, 0x20,
               0x20, 0x20, 0x20, 0x2C, 0x34, 0x64, 0xA4, 0x24, 0x34, 0x28, 0x22, 0x22, 0x02, 0xFE, 0x00],  # /*"地",17*/

    0xE59D80: [0x10, 0x10, 0x10, 0x11, 0x11, 0xFD, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1D, 0xE1, 0x41, 0x07, 0x00, 0x20,
               0x20, 0x20, 0x20, 0x20, 0x20, 0x3C, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xFE, 0x00],  # /*"址",18*/

    0xE5AEA4: [0x02, 0x01, 0x7F, 0x40, 0x80, 0x3F, 0x04, 0x08, 0x1F, 0x01, 0x01, 0x3F, 0x01, 0x01, 0xFF, 0x00, 0x00,
               0x00, 0xFE, 0x02, 0x04, 0xF8, 0x00, 0x20, 0xF0, 0x10, 0x00, 0xF8, 0x00, 0x00, 0xFE, 0x00],  # /*"室",19*/

    0xE58685: [0x01, 0x01, 0x01, 0x7F, 0x41, 0x41, 0x41, 0x42, 0x42, 0x44, 0x48, 0x50, 0x40, 0x40, 0x40, 0x40, 0x00,
               0x00, 0x00, 0xFC, 0x04, 0x04, 0x04, 0x84, 0x44, 0x24, 0x14, 0x14, 0x04, 0x04, 0x14, 0x08],  # /*"内",20*/

    0xE697A5: [0x00, 0x1F, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F, 0x10, 0x00,
               0xF0, 0x10, 0x10, 0x10, 0x10, 0x10, 0xF0, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0xF0, 0x10],  # /*"日",21*/

    0xE69C9F: [0x22, 0x22, 0x7F, 0x22, 0x22, 0x3E, 0x22, 0x22, 0x3E, 0x22, 0x22, 0xFF, 0x04, 0x22, 0x41, 0x82, 0x00,
               0x7C, 0x44, 0x44, 0x44, 0x7C, 0x44, 0x44, 0x44, 0x7C, 0x44, 0x44, 0x84, 0x84, 0x14, 0x08],  # /*"期",22*/

    0xE59CB0: [0x10, 0x10, 0x10, 0x11, 0x11, 0xFD, 0x11, 0x13, 0x11, 0x11, 0x11, 0x1D, 0xE1, 0x41, 0x00, 0x00, 0x20,
               0x20, 0x20, 0x20, 0x2C, 0x34, 0x64, 0xA4, 0x24, 0x34, 0x28, 0x22, 0x22, 0x02, 0xFE, 0x00],  # /*"地",23*/

    0xE782B9: [0x02, 0x02, 0x02, 0x03, 0x02, 0x02, 0x3F, 0x20, 0x20, 0x20, 0x3F, 0x00, 0x24, 0x22, 0x42, 0x80, 0x00,
               0x00, 0x00, 0xFC, 0x00, 0x00, 0xF0, 0x10, 0x10, 0x10, 0xF0, 0x00, 0x88, 0x44, 0x44, 0x04],  # /*"点",24*/
    0xEFBC9A: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x00, 0x30, 0x30, 0x00, 0x00, 0x00,
               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],  # /*"：",0*/
}

def chinese(ch_str, x_axis, y_axis):
    offset_ = 0
    y_axis = y_axis*8  # 中文高度一行占8个
    x_axis = (x_axis*16)  # 中文宽度占16个
    for k in ch_str:
        code = 0x00  # 将中文转成16进制编码
        data_code = k.encode("utf-8")
        code |= data_code[0] << 16
        code |= data_code[1] << 8
        code |= data_code[2]
        byte_data = fonts[code]
        for y in range(0, 16):
            a_ = bin(byte_data[y]).replace('0b', '')
            while len(a_) < 8:
                a_ = '0'+a_
            b_ = bin(byte_data[y+16]).replace('0b', '')
            while len(b_) < 8:
                b_ = '0'+b_
            for x in range(0, 8):
                display.pixel(x_axis+offset_+x, y+y_axis, int(a_[x]))
                display.pixel(x_axis+offset_+x+8, y+y_axis, int(b_[x]))
        offset_ += 16