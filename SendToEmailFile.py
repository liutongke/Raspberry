#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: SendToEmailFile.py
@time: 2023/4/15 21:47
@version：Python 3.11.2
"""

import smtplib
# 需要 MIMEMultipart 类
from email.mime.multipart import MIMEMultipart
# 发送字符串的邮件
from email.mime.text import MIMEText

# 设置服务器所需信息
fromEmailAddr = ''  # 邮件发送方邮箱地址
password = ''  # 密码(部分邮箱为授权码)
toEmailAddrs = ['']  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
Subject = 'test title'  # 邮件标题
Content = 'test content'  # 邮箱内容
FilePath = 'test.txt'  # 附件地址
# 设置email信息
# ---------------------------发送带附件邮件-----------------------------
# 邮件内容设置
message = MIMEMultipart()
# 邮件主题
message['Subject'] = Subject
# 发送方信息
message['From'] = fromEmailAddr
# 接受方信息
message['To'] = toEmailAddrs[0]
# 邮件正文内容
message.attach(MIMEText(Content, 'plain', 'utf-8'))

# 构造附件
att1 = MIMEText(open(FilePath, 'rb').read(), 'base64', 'utf-8')
att1['Content-type'] = 'application/octet-stream'
att1['Content-Disposition'] = 'attachment; filename="test.txt"'
message.attach(att1)
# ---------------------------------------------------------------------

# 登录并发送邮件
try:
    server = smtplib.SMTP('smtp.163.com')  # 163邮箱服务器地址，端口默认为25
    server.login(fromEmailAddr, password)
    server.sendmail(fromEmailAddr, toEmailAddrs, message.as_string())
    print('success')
    server.quit()
except smtplib.SMTPException as e:
    print("error:", e)
