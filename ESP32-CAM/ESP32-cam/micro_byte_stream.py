#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: micro_byte_stream.py
@time: 2023/5/19 17:22
@version：Python 3.11.2
@title: 
"""
import machine


def get_device_info():
    machine_unique_id = machine.unique_id()  # 获取设备唯一标识符
    device_id = ''.join(['{:02x}'.format(byte) for byte in machine_unique_id])  # 转换为十六进制字符串
    return device_id, len(device_id)


def encode_payload(payload):
    device_id, device_id_len = get_device_info()
    device_id_len_byte_data = device_id_len.to_bytes(4, 'big')  # 将整数转换为字节流
    device_id_byte_data = bytes(device_id, 'utf-8')  # 将字符串转换为字节流
    payload_byte_data = bytes(payload, 'utf-8')  # 将字符串转换为字节流

    merged_data_stream = bytearray(device_id_len_byte_data) + bytearray(device_id_byte_data) + bytearray(
        payload_byte_data)  # 合并字节流
    return merged_data_stream

# device_id = machine.unique_id()  # 获取设备唯一标识符
# device_id_str = ''.join(['{:02x}'.format(byte) for byte in device_id])  # 转换为十六进制字符串
#
# print(device_id_str)  # 打印设备唯一标识符字符串
#
# device_id = 'esp32-cam'
# device_id_len = len(device_id)
# payload = 'Ae98r5ylpGLsMa1g'
#
# device_id_len_byte_data = device_id_len.to_bytes(4, 'big')  # 将整数转换为字节流
# device_id_byte_data = bytes(device_id, 'utf-8')  # 将字符串转换为字节流
# payload_byte_data = bytes(payload, 'utf-8')  # 将字符串转换为字节流
#
# merged_data = bytearray(device_id_len_byte_data) + bytearray(device_id_byte_data) + bytearray(
#     payload_byte_data)  # 合并字节流
# print("合并后数据流", merged_data)
#
# device_id_len_sliced_data = merged_data[0:4]  # 截取字节流的一部分
#
# device_id_len = int.from_bytes(device_id_len_sliced_data, 'big')  # 将字节流转换为整数
# print(device_id_len)
# device_id_sliced_data = merged_data[4:device_id_len]  # 截取字节流的一部分
# print(device_id_sliced_data.decode('utf-8'))
#
# payload = merged_data[4 + device_id_len:]
# print(payload)
