#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess


# 关机
def shutdown_raspberry_pi():
    subprocess.run(["sudo", "shutdown", "-h", "now"])


# 重启
def reboot_raspberry_pi():
    subprocess.run(["sudo", "reboot"])
