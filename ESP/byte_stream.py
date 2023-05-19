#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: test.py
@time: 2023/5/19 12:25
@version：Python 3.11.2
@title: 
"""
import io

device_id = 'RaspberryPi'
device_id_len = len(device_id)
payload = 'XCz9mryE0AckHBnP'

buffer = io.BytesIO()  # 创建一个内存中的字节流缓冲区
# 合并数据流
buffer.write(device_id_len.to_bytes(4, 'big'))
buffer.write(device_id.encode())
buffer.write(payload.encode())

# 获取合并后的数据流
merged_data_stream = buffer.getvalue()

# 可以在这里使用 merged_data_stream 进行后续操作
print("合并后数据流:", merged_data_stream)

# 设置截取范围
start_index = 0  # 起始索引（包含）
end_index = 4  # 结束索引（不包含）

# 截取数据流的一部分
buffer.seek(start_index)  # 设置读取的起始位置
device_id_len_data_stream = buffer.read(end_index - start_index)  # 读取指定范围的数据
print("设备名称长度：", int.from_bytes(device_id_len_data_stream, 'big'))

buffer.seek(end_index)
device_id_data_stream = buffer.read(int.from_bytes(device_id_len_data_stream, 'big'))  # 读取指定范围的数据
print("设备名称：", device_id_data_stream)

n = int.from_bytes(device_id_len_data_stream, 'big') + 4
buffer.seek(n)
payload_data_stream = buffer.read()  # 读取指定范围的数据
print("payload数据：", payload_data_stream)
# 关闭缓冲区
buffer.close()
