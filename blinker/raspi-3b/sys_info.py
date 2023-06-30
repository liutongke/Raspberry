#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

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


# 调用函数获取磁盘信息
def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = []

    for partition in partitions:
        partition_info = {}
        partition_info['Device'] = partition.device
        partition_info['Mount Point'] = partition.mountpoint
        partition_info['File System Type'] = partition.fstype
        disk_usage = psutil.disk_usage(partition.mountpoint)
        partition_info['Total Size'] = disk_usage.total // (1024 * 1024)  # 转换为MB
        partition_info['Used Size'] = disk_usage.used // (1024 * 1024)  # 转换为MB
        partition_info['Free Space'] = disk_usage.free // (1024 * 1024)  # 转换为MB
        disk_info.append(partition_info)

    return disk_info


# 调用函数获取磁盘信息
# disk_info = get_disk_info()

# 打印磁盘信息
# for disk in disk_info:
#     print('设备:', disk['Device'])
#     print('挂载点:', disk['Mount Point'])
#     print('文件系统类型:', disk['File System Type'])
#     print('总大小:', disk['Total Size'], 'MB')
#     print('已使用大小:', disk['Used Size'], 'MB')
#     print('可用空间:', disk['Free Space'], 'MB')
#     print('---------------------------')


# 调用函数获取磁盘总可用空间
def get_total_available_info():
    partitions = psutil.disk_partitions()
    total_available_space = 0

    for partition in partitions:
        disk_usage = psutil.disk_usage(partition.mountpoint)
        total_available_space += disk_usage.total // (1024 * 1024 * 1024)  # 累加每个分区的总可用空间（以GB为单位）

    return total_available_space


# 格式化输出磁盘总可用空间
# print('Total Available Space: {:.2f} GB'.format(get_total_available_info()))


# 调用函数获取 /dev/root 目录的可用空间
def get_available_space():
    disk_usage = psutil.disk_usage('/')
    available_space_gb = disk_usage.free / (1024 ** 3)  # 将字节转换为GB
    return available_space_gb


# 格式化输出可用空间
# print('Available Space: {:.2f} GB'.format(get_available_space()))


# 获取摇杆x轴与y轴的数据计算脚本
def joystick1_callback(xAxis, yAxis):
    angle = (xAxis * 90) / 128
    return angle


# 调用函数获取当前CPU频率
def get_cpu_frequency():
    try:
        with open('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq', 'r') as f:
            frequency = int(f.read().strip()) / 1000  # 将频率转换为MHz
            return frequency
    except FileNotFoundError:
        return None


# 调用函数获取当前CPU频率
# cpu_frequency = get_cpu_frequency()
# if cpu_frequency is not None:
#     print(f"当前CPU频率: {cpu_frequency} MHz")
# else:
#     print("无法获取CPU频率信息")


# 调用函数获取当前工作频率
def get_cpu_frequency():
    try:
        output = subprocess.check_output("vcgencmd measure_clock arm", shell=True)
        output = output.decode("utf-8").strip()
        frequency = int(output.split("=")[1]) / 1000000  # 将频率转换为MHz
        return frequency
    except subprocess.CalledProcessError:
        return None

# 调用函数获取当前工作频率
# cpu_frequency = get_cpu_frequency()
# if cpu_frequency is not None:
#     print(f"当前工作频率: {cpu_frequency} MHz")
# else:
#     print("无法获取工作频率信息")
