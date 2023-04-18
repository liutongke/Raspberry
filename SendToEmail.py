#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: SendToEmail.py
@time: 2023/4/15 21:41
@version：Python 3.11.2
"""
import smtplib
# 发送字符串的邮件
from email.mime.text import MIMEText

mail_host = "smtp.163.com"  # SMTP服务器地址
mail_sender = ""  # 账号
mail_passwd = ""  # 密码

# 构造邮件内容
msg = MIMEText("这里是邮件正文内容", 'plain', 'utf-8')
msg["Subject"] = "这里是邮件主题"
msg["From"] = mail_sender  # 发送人
to_receiver = ['']  # 收件人邮箱,多个人就是要list
cc_reciver = ['']  # 抄送邮箱
receiver = cc_reciver + to_receiver
msg["To"] = ";".join(receiver)  # 接收人  但是这个不区分收件人和抄送，不过也无关痛痒

# 发送邮件
s = smtplib.SMTP()  # 实例化对象
s.connect(mail_host)  # 连接163邮箱服务器，端口号为465,注意，这里不需要写端口号，有些需要写端口，需要写的话就直接写数字
s.login(mail_sender, mail_passwd)  # 登录邮箱
s.sendmail(mail_sender, receiver, msg.as_string())
s.quit()
