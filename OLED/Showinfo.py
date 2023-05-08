#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: Showinfo.py
@time: 2023/4/28 11:51
@version：Python 3.11.2
@title: 
"""
import DH11
import RaspiInfo
import time

# while True:
#     print(DH11.DH11().GetDH11Data())
#     print(RaspiInfo.RaspiInfo().GetCpuTemp())
#     time.sleep(10)
# !/usr/bin/python3
# -*- coding: utf-8 -*-
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
import socket
from PIL import ImageFont
from luma.core.virtual import viewport
import time
import random
from pathlib import Path
# from demo_opts import get_device
from luma.core.virtual import viewport
from PIL import Image
import RaspiInfo
import DH11
import GetLux
import Tools

txt = """
待到秋来九月八，
我花开后百花杀。
冲天香阵透长安，
满城尽带黄金甲。
------------
等到秋天九月重阳节来临的时候，
菊花盛开以后别的花就凋零了。
盛开的菊花香气弥漫整个长安，
遍地都是金黄如铠甲般的菊花。
"""


def text(data):
    # while True:
    # 调用显示函数
    with canvas(device) as draw:
        for i, line in enumerate(data):
            draw.text((0, (i * 16)), text=line, fill="white", font=font)
        # draw.rectangle(device.bounding_box, outline="white", fill="black")
        # draw.text((0, 0), RaspiInfo.RaspiInfo().get_host_ip(), fill="white", font=font)
        # dict_ = DH11.DH11().GetDH11Data()
        # temperature = "室温:%.1f ℃" % dict_['temperature']
        # humidity = "湿度:%.1f rh" % dict_['humidity']
        # draw.text((0, 15), temperature, fill="white", font=font)
        # draw.text((0, 30), humidity, fill="white", font=font)
        # draw.text((0, 45), GetLux.GetIlluminance(), fill="white", font=font)

        # tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #
        # draw.text((0, 15), tm, fill="white", font=font)


# 垂直滚动
def scroll_up(data):
    virtual = viewport(device, width=device.width, height=768)

    with canvas(virtual) as draw:
        # for i, line in enumerate(txt.split("\n")):
        #     draw.text((0, 20 + (i * 16)), text=line, fill="white", font=font)
        for i, line in enumerate(data):
            draw.text((0, 20 + (i * 16)), text=line, fill="white", font=font)
    sleep(2)

    for y in range(240):
        virtual.set_position((0, y))
        time.sleep(0.01)


# 翻页
def page(data):
    virtual = viewport(device, width=device.width, height=768)

    with canvas(virtual) as draw:
        # for i, line in enumerate(txt.split("\n")):
        #     draw.text((0, 20 + (i * 16)), text=line, fill="white", font=font)
        for i, line in enumerate(data):
            draw.text((0, 20 + (i * 16)), text=line, fill="white", font=font)
    sleep(2)

    for y in range(240):
        virtual.set_position((0, y))
        time.sleep(5)


def status():
    pass


if __name__ == "__main__":
    try:

        # 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
        device = ssd1306(i2c(port=1, address=0x3C))
        font = ImageFont.truetype('./fonts/msyh.ttc', 12)

        while True:
            # info = RaspiInfo.RaspiInfo().GetRaspiInfo()
            # scroll_up(info)
            # text()
            temp = []

            dict_ = DH11.DH11().GetDH11Data()
            temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            temp.append("室内温度:%.2f ℃" % dict_['temperature'])
            temp.append("室内湿度:%.2f RH" % dict_['humidity'])
            temp.append(GetLux.GetIlluminance())
            text(temp)
            sleep(5)

            text(RaspiInfo.RaspiInfo().GetRaspiInfo())
            sleep(5)

            base_city_weather = Tools.get_base_weather()
            text([
                "城市:%s" % base_city_weather['city'],
                "实时天气:%s" % base_city_weather['weather'],
                "实时气温:%s ℃" % base_city_weather['temperature_float'],
                "空气湿度:%s RH" % base_city_weather['humidity_float'],
            ])
            sleep(5)

            text([
                "风向:%s" % base_city_weather['winddirection'],
                "风力级别:%s" % base_city_weather['windpower'],
                "发布:%s" % base_city_weather['reporttime'],
                "ip地址:%s" % Tools.get_ip(),
            ])
            sleep(5)
    except KeyboardInterrupt:
        pass
