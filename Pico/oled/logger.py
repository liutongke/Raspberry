#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uio
import utime

# 定义日志文件路径
log_file_path = "./log.txt"


def save_log(message):
    result = get_current_datetime() + " - " + message
    # 打开日志文件，使用追加模式（"a"）
    with uio.open(log_file_path, "a") as file:
        # 写入日志内容
        file.write(result + "\n")


def get_current_datetime():
    # 获取当前时间的元组形式
    current_time = utime.localtime()

    # 提取年、月、日、时、分、秒
    year = current_time[0]
    month = current_time[1]
    day = current_time[2]
    hour = current_time[3]
    minute = current_time[4]
    second = current_time[5]

    # 格式化日期和时间字符串
    date_str = "{:04d}-{:02d}-{:02d}".format(year, month, day)
    time_str = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)

    # 拼接日期和时间
    datetime_str = date_str + " " + time_str

    return datetime_str
