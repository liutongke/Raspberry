#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: MPU-6050.py
@time: 2023/4/27 13:34
@version：Python 3.11.2
@title: MPU-6050 https://www.52pojie.cn/thread-998097-1-1.html
"""
import smbus
import math
import time

# 电源管理寄存器地址
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


# 从一个给定的寄存器中读取一个单字（16bits）并将其转换为二进制补码
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


# 得到了每个 三维空间中重力对传感器施加的值，通过这个值我们可以计算出x轴和y轴的旋转值
def dist(a, b):
    return math.sqrt((a * a) + (b * b))
    # math.sqrt(x) 方法返回数字x的平方根。


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    # math.atan2(y, x) 返回给定的 X 及 Y 坐标值的反正切值。
    return -math.degrees(radians)
    # math.degrees(x) 将弧度x转换为角度。


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68  # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
    time.sleep(0.1)
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print(' ')
    print("-----------------------陀螺仪数据-----------------------")
    print("x轴陀螺仪计算值 : ", gyro_xout, " 每秒的旋转度数: ", (gyro_xout / 131))  # 倍率：±250°/s
    print("y轴陀螺仪计算值 : ", gyro_yout, " 每秒的旋转度数: ", (gyro_yout / 131))
    print("z轴陀螺仪计算值 : ", gyro_zout, " 每秒的旋转度数: ", (gyro_zout / 131))

    # 读取x、y、z的加速计算值，MPU6050传感器有许多寄存器，他们具有不同的功能，用于减速数据的寄存器是0x3b、0x3d、0x3f)
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    # 需要应用到原始加速度计值的默认转换值是16384
    accel_xout_scaled = accel_xout / 16384.0  # 倍率：±2g
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    print("-----------------------加速度数据-----------------------")
    print("x轴加速度计数值: ", accel_xout, " 每秒的旋转度数: ", accel_xout_scaled)
    print("y轴加速度计数值: ", accel_yout, " 每秒的旋转度数: ", accel_yout_scaled)
    print("z轴加速度计数值: ", accel_zout, " 每秒的旋转度数: ", accel_zout_scaled)
    print("-----------------------旋转度数据-----------------------")
    print("x轴旋转度数: ", get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    print("y轴旋转度数: ", get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))

    time.sleep(1)
