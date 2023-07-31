#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

# 启动 srs4-cow 容器
subprocess.run(["docker", "run", "-itd", "--name", "srs4-cow", "registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4"],
               check=True)

# 从容器中复制配置文件到本地
subprocess.run(["docker", "cp", "srs4-cow:/usr/local/srs/conf", "./"], check=True)

# 复制 docker.conf 文件到 conf 目录中
conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf")
docker_conf = os.path.join(conf_path, "docker.conf")
if not os.path.exists(conf_path):
    os.mkdir(conf_path)
subprocess.run(["cp", "docker.conf", docker_conf], check=True)

# 构建镜像 srs4:v1
subprocess.run(["docker", "build", "-t", "srs4:v1", "."], check=True)

VIDEO_DIR = "video"
if not os.path.exists(VIDEO_DIR):
    os.mkdir(VIDEO_DIR)

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

# 运行 srs4-v1 容器
subprocess_args = [
    "docker", "run", "--name", "srs4-v1", "-itd",
    "-p", "1935:1935", "-p", "1985:1985", "-p", "8080:8080",
    "--restart", "always",
    "-v", f"{SCRIPT_PATH}/conf:/usr/local/srs/conf",
    "-v", f"{SCRIPT_PATH}/video:/usr/local/srs/video",
    "srs4:v1",
    "./objs/srs", "-c", "conf/docker.conf"
]
subprocess.run(subprocess_args, check=True)

# 停止并删除 srs4-cow 容器
subprocess.run(["docker", "stop", "srs4-cow"], check=True)
subprocess.run(["docker", "rm", "srs4-cow"], check=True)
