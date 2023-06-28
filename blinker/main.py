#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time

from blinker import Device, ButtonWidget, RangeWidget

import config
import control
import lux
import sys_info
import temp_hum

device = Device(config.device_id)

btn_reboot = device.addWidget(ButtonWidget('btn-reboot'))
btn_shutdown = device.addWidget(ButtonWidget('btn-shutdown'))
ran_control = device.addWidget(RangeWidget('ran-val'))

deviceName = ""


async def btn_reboot_callback(msg):
    print("--------------btn_reboot_callback-----------------")
    print("btn_reboot_callback: {0}".format(msg))
    print(msg)


async def btn_shutdown_callback(msg):
    print("-------------btn_reboot_callback------------------")
    print("btn_shutdown_callback: {0}".format(msg))
    print(msg)


async def ran_control_callback(msg):
    print("-------------ran_control_callback------------------")
    var = msg["ran-val"]
    if var == 50:
        print("shutdown")
        control.shutdown_raspberry_pi()
    elif var == 100:
        print("The user initiates a restart request")
        control.reboot_raspberry_pi()
    print("Range received: {0}".format(msg))


async def heartbeat_func(msg):
    # print("Heartbeat func received: {0}".format(msg))
    # 文本组件
    pass


async def ready_func():
    # 获取设备配置信息
    global deviceName
    device_info = vars(device.config)
    print(device_info)
    deviceName = device_info["uuid"]
    # print("deviceName:", device_info["uuid"])
    data = {}
    while True:
        temp_hum_info = temp_hum.get_environment()
        if temp_hum_info["temp"] == 0 or temp_hum_info["humi"] == 0:
            await device.sendMessage(data, deviceName)
        else:
            cpu_use_info = sys_info.get_cpu_use()
            memory_info = sys_info.get_memory()

            msg = {
                "temp": {"tex": "室温", "val": temp_hum_info["temp"]},
                "humi": {"tex": "湿度", "val": temp_hum_info["humi"]},
                "cpu-temp": {"tex": "cpu温度", "val": sys_info.get_cpu_temp()},
                "cpu_percent": {"tex": "cpu使用率", "val": cpu_use_info["cpu_percent"]},
                "cpu_count": {"tex": "cpu核心数", "val": cpu_use_info["cpu_count"]},
                "total_memory": {"tex": "总内存", "val": memory_info["total_memory"]},
                "available_memory": {"tex": "可用内存", "val": memory_info["available_memory"]},
                "used_memory": {"tex": "已用内存", "val": memory_info["used_memory"]},
                "memory_percent": {"tex": "内存使用率", "val": memory_info["memory_percent"]},
                "available_space": {"tex": "可用磁盘", "val": sys_info.get_available_space()},
                "lux": {"tex": "光线强度", "val": lux.read_light_intensity()},
            }
            data = msg
            await device.sendMessage(msg, deviceName)
        time.sleep(5)


btn_reboot.func = btn_reboot_callback
btn_shutdown.func = btn_shutdown_callback
ran_control.func = ran_control_callback
device.heartbeat_callable = heartbeat_func
device.ready_callable = ready_func

if __name__ == '__main__':
    asyncio.run(device.run())  # 运行设备程序
