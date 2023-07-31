#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess


def main():
    # 获取当前目录路径
    current_dir = os.getcwd()
    print("Current directory path:", current_dir)

    # 构建镜像
    image_name = "nginx-rtmp-server:v1"
    subprocess.run(["docker", "build", "-t", image_name, "-f", "./Dockerfile", "."], check=True)

    # 运行容器
    subprocess.run([
        "docker", "run", "--name", "nginx-rtmp-v1", "-d", "-p", "9998:1935", "-p", "9999:80",
        "--restart", "always", "-v", f"{current_dir}/nginx.conf:/usr/local/nginx/conf/nginx.conf", image_name
    ], check=True)


if __name__ == "__main__":
    main()
