#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: t.py
@time: 2023/5/24 4:26
@version：Python 3.11.2
@title: 
"""
import multiprocessing
import subprocess as sp


def worker(shared_dict):
    process = shared_dict['process']
    process.communicate(input=b"Hello, subprocess!")


if __name__ == '__main__':
    # 创建共享对象管理器
    manager = multiprocessing.Manager()

    # 创建共享字典，并存储 subprocess.Popen 对象
    shared_dict = manager.dict()
    shared_dict['process'] = sp.Popen(['echo', 'Hello, World!'], stdin=sp.PIPE, stdout=sp.PIPE)

    # 创建子进程，传递共享字典
    process = multiprocessing.Process(target=worker, args=(shared_dict,))
    process.start()

    # 等待子进程完成
    process.join()
