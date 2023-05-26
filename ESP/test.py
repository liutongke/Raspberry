#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: test.py
@time: 2023/5/19 12:11
@version：Python 3.11.2
@title: 
"""
import fcntl
import threading
import time
from multiprocessing import Process, Queue


def get_tm_str():
    from datetime import datetime

    # 获取当前时间
    current_time = datetime.now()

    # 将时间转换为字符串
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # print("当前时间:", time_string)
    return time_string


def producer(queue):
    # while True:
    message = f"发送消息：{get_tm_str()}"
    queue.put(message)
    time.sleep(1)


def consumer(queue):
    while True:
        message = queue.get()
        print("接收到消息:", message)


if __name__ == "__main__":
    queue = Queue()
    producer_process = Process(target=producer, args=(queue,))
    consumer_process = Process(target=consumer, args=(queue,))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

exit()

lock_file = open("lock_file.lock", "w")  # 创建一个锁文件


def lock():
    fcntl.flock(lock_file, fcntl.LOCK_EX)  # 获取排它锁


def lock_flock():
    fcntl.flock(lock_file, fcntl.LOCK_UN)  # 释放锁


def lock_close():
    lock_file.close()  # 关闭锁文件


def print_numbers(n):
    print(f'{n}准备获得锁')
    lock()
    print(f'my {n}')
    time.sleep(10)
    lock_flock()


def print_letters(n):
    print(f'{n}准备获得锁')
    lock()
    print(f'my {n}')
    time.sleep(5)
    lock_flock()


# 创建线程对象
thread1 = threading.Thread(target=print_numbers, args=("thread1",))
thread2 = threading.Thread(target=print_letters, args=("thread2",))

# 启动线程
thread1.start()
thread2.start()

# 等待线程结束
thread1.join()
thread2.join()
print("All threads have finished execution.")

try:
    while True:
        pass
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("bye bye")
    lock_close()
