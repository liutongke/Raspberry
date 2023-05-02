#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: RaspiInfo.py
@time: 2023/4/28 11:48
@version：Python 3.11.2
@title: 
"""
import DH11
import os
import sys
import time
from pathlib import Path
from datetime import datetime
import socket

import psutil

if os.name != 'posix':
    sys.exit(f'{os.name} platform is not supported')

from luma.core.render import canvas
from PIL import ImageFont


class RaspiInfo:
    def __int__(self):
        pass

    def GetRaspiInfo(self):
        tmp = []

        tmp.append(self.get_host_ip())
        tmp.append(self.GetCpuTemp())
        tmp.append(self.CpuUsage())
        tmp.append(self.MemUsage())
        tmp.append(self.DiskUsage('/'))

        return tmp

    def get_host_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return "ip地址:%s" % ip

    def GetCpuTemp(self):
        file = open("/sys/class/thermal/thermal_zone0/temp")
        temp = float(file.read()) / 1000
        file.close()
        return "CPU温度:%.1f ℃" % temp

    def CpuUsage(self):
        # load average, uptime
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        av1, av2, av3 = os.getloadavg()
        return "Ld:%.1f %.1f %.1f Up: %s" \
            % (av1, av2, av3, str(uptime).split('.')[0])

    def MemUsage(self):
        usage = psutil.virtual_memory()
        return "Mem: %s %.0f%%" \
            % (self.bytes2human(usage.used), 100 - usage.percent)

    def DiskUsage(self, dir):
        usage = psutil.disk_usage(dir)
        return "SD:  %s %.0f%%" \
            % (self.bytes2human(usage.used), usage.percent)

    def bytes2human(self, n):
        """
        >>> bytes2human(10000)
        '9K'
        >>> bytes2human(100001221)
        '95M'
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = int(float(n) / prefix[s])
                return '%s%s' % (value, s)
        return f"{n}B"
