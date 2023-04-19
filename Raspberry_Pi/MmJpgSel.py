#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" 
@author:keke 
@file: MmJpgSel.py 
@time: 2018/05/16 
"""
import os
import requests
from bs4 import BeautifulSoup
import pymysql
import urllib.request
from selenium import webdriver
import time


class MmJpgSel(object):
    def __init__(self):
        pass

    # 打开全部
    def onclikAll(self):
        browser = webdriver.Chrome('D:\Python\chromedriver.exe')
        # 打开首页
        browser.get('http://www.mmjpg.com/tag/xiaoqingxin')
        time.sleep(5)
        browser.get('http://www.mmjpg.com/mm/1346')
        # 浏览器最大化
        # browser.maximize_window()

        # 设置浏览器的高度为800像素，宽度为480像素
        # browser.set_window_size(480, 800)

        # # 查找出对应的元素进行点击
        browser.find_element_by_xpath("//em[@class='ch all']").click()
        time.sleep(5)
        browser.back()
        time.sleep(5)
        print('加载完了')
        exit()


obj = MmJpgSel()
obj.onclikAll()
