#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: SendToEmailLocalIp.py
@time: 2023/4/15 22:10
@version：Python 3.11.2
@title: 
"""
import socket
import smtplib
# 发送字符串的邮件
from email.mime.text import MIMEText
import time

time.sleep(10)
dataId = time.strftime("%Y-%m-%d %H:%M:%S")


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


myAddrIp = get_host_ip()  # 获取本机ip

if myAddrIp:
    mail_host = "smtp.163.com"  # SMTP服务器地址
    mail_sender = ""  # 账号
    mail_passwd = ""  # 密码

    # 构造邮件内容
    msg = MIMEText(myAddrIp, 'plain', 'utf-8')
    msg["Subject"] = "树莓派的ip地址: " + myAddrIp + " 日期: " + dataId
    msg["From"] = mail_sender  # 发送人
    to_receiver = ['']  # 收件人邮箱,多个人就是要list
    cc_reciver = ['']  # 抄送邮箱,可以不写
    receiver = cc_reciver + to_receiver
    msg["To"] = ";".join(receiver)  # 接收人  但是这个不区分收件人和抄送，不过也无关痛痒

    # 发送邮件
    s = smtplib.SMTP()  # 实例化对象
    s.connect(mail_host)  # 连接163邮箱服务器，端口号为465,注意，这里不需要写端口号，有些需要写端口，需要写的话就直接写数字
    s.login(mail_sender, mail_passwd)  # 登录邮箱
    s.sendmail(mail_sender, receiver, msg.as_string())
    s.quit()
