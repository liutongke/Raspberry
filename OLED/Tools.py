#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: Tools.py
@time: 2023/5/2 21:27
@version：Python 3.11.2
@title: 
"""
import requests
import json
import config


def json_decode(json_dict_):
    return json.loads(json_dict_)


def json_encode(dict_):
    return json.dumps(dict_, )


# 获取当前ip地址
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


# 获取预报天气
def get_all_weather(extensions_type=1):
    extensions = "all" if extensions_type == 1 else "base"
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={config.gaode_key()}&city={get_city_code()}&extensions={extensions}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# {
#     "status": "1",
#     "count": "1",
#     "info": "OK",
#     "infocode": "10000",
#     "lives": [
#         {
#             "province": "上海",
#             "city": "上海市",
#             "adcode": "310000",
#             "weather": "多云",
#             "temperature": "20",
#             "winddirection": "东",
#             "windpower": "≤3",
#             "humidity": "72",
#             "reporttime": "2023-05-02 22:03:40",
#             "temperature_float": "20.0",
#             "humidity_float": "72.0"
#         }
#     ]
# }
# 获取实况天气 https://lbs.amap.com/api/webservice/guide/api/weatherinfo
def get_base_weather(extensions_type=0):
    extensions = "all" if extensions_type == 1 else "base"
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={config.gaode_key()}&city={get_city_code()}&extensions={extensions}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json_decode(response.text)['lives'][0]


# ip定位 https://lbs.amap.com/api/webservice/guide/api/ipconfig
def get_location():
    ip = get_ip()
    key = config.gaode_key()
    url = f"https://restapi.amap.com/v3/ip?ip={ip}&key={key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json_decode(response.text)


# 获取城市编码
def get_city_code():
    return get_location()["adcode"]

# t = get_location()
# print(t)
# print(t["adcode"])
# print(get_base_weather())
