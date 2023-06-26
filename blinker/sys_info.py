#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil


# 获取CPU温度
def get_cpu_temp() -> float:
    # 打开文件
    file = open("/sys/class/thermal/thermal_zone0/temp")
    # 读取结果，并转换为浮点数
    temp = float(file.read()) / 1000
    # 关闭文件
    file.close()
    # print("cpu温度:", temp)
    return temp


# 获取CPU详情
def get_cpu_use():
    # 获取 CPU 使用情况
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()

    # print("CPU 使用率: {:.2f}%".format(cpu_percent))
    # print("CPU 核心数: {}".format(cpu_count))
    return {
        "cpu_percent": cpu_percent,
        "cpu_count": cpu_count
    }


# 获取内存详情
def get_memory():
    # 获取内存使用情况
    memory = psutil.virtual_memory()

    total_memory = memory.total / (1024 * 1024)  # 总内存大小（MB）
    available_memory = memory.available / (1024 * 1024)  # 可用内存大小（MB）
    used_memory = memory.used / (1024 * 1024)  # 已使用内存大小（MB})
    memory_percent = memory.percent  # 内存使用率

    # print("总内存: {:.2f} MB".format(total_memory))
    # print("可用内存: {:.2f} MB".format(available_memory))
    # print("已使用内存: {:.2f} MB".format(used_memory))
    # print("内存使用率: {:.2f}%".format(memory_percent))
    return {
        "total_memory": total_memory,
        "available_memory": available_memory,
        "used_memory": used_memory,
        "memory_percent": memory_percent,
    }


# 获取摇杆x轴与y轴的数据计算脚本
def joystick1_callback(xAxis, yAxis):
    angle = (xAxis * 90) / 128
    return angle
