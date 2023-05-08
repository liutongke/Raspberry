import urequests as requests
import json

import Tools
import config
import ntptime
import time
import utime
import time
import utime
import machine
from ntptime import settime
import os
import oled
import tm


def json_decode(json_dict_):
    return json.loads(json_dict_)


def json_encode(dict_):
    return json.dumps(dict_, )


# 获取当前ip地址
def get_ip():
    return "114.83.85.103"
    # response = requests.get(url='https://api64.ipify.org?format=json').json()
    # return response["ip"]


# ip定位 https://lbs.amap.com/api/webservice/guide/api/ipconfig


def get_location():
    ip = get_ip()

    key = config.gaode_key()
    local_url = f"https://restapi.amap.com/v3/ip?ip={ip}&key={key}"

    return requests.get(url=local_url).json()


# 获取城市编码


def get_city_code():
    return get_location()["adcode"]


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

'''
{
    "code": 0,
    "message": "Success",
    "data": {
        "animalsYear": "兔",
        "weekday": "星期一",
        "lunarYear": "癸卯年",
        "lunar": "三月十九",
        "year-month": "2023-5",
        "date": "2023-5-8",
        "suit": "结婚.出行.搬家.合婚订婚.搬新房",
        "avoid": "动土.安葬.破土",
        "holiday": "",
        "desc": ""
    }
}

https://www.kancloud.cn/topthink-doc/think-api/1861639
获取万年历，每天免费100次调用
'''


def get_wannianli():
    # file_name = '%s_wanninali.txt' % tm.dateId()
    file_name = 'wanninali.txt'

    d = json_decode(Tools.read_file(file_name))
    if 'endTm' in d and d['endTm'] > time.time():
        return d['data']

    data = get_request_wannianli()
    dict_ = {
        'endTm': tm.getTm() + 3600,
        'data': data,
        'tm': tm.tmStr()
    }

    Tools.write_file(file_name, Tools.json_encode(dict_))

    return data


def get_request_wannianli():
    # data = {
    #     "animalsYear": "兔",
    #     "weekday": "星期一",
    #     "lunarYear": "癸卯年",
    #     "lunar": "三月十九",
    #     "year-month": "2023-5",
    #     "date": "2023-5-8",
    #     "suit": "结婚.出行.搬家.合婚订婚.搬新房",
    #     "avoid": "动土.安葬.破土",
    #     "holiday": "",
    #     "desc": ""
    # }
    # print("get_request_wannianli request")
    # return data
    dateId = tm.dateId()

    weather_url = f"https://api.topthink.com/calendar/day?appCode={config.get_topthink_api_key()}&date={dateId}"

    response = requests.get(url=weather_url).json()

    return response['data']


def get_base_weather(extensions_type=0):
    file_name = 'weather.txt'

    d = json_decode(Tools.read_file(file_name))
    if 'endTm' in d and d['endTm'] > time.time():
        return d['data']

    data = get_weather(0)
    dict_ = {
        'endTm': tm.getTm() + 3600,
        'data': data,
        'tm': tm.tmStr()
    }

    Tools.write_file(file_name, Tools.json_encode(dict_))

    return data


def get_weather(extensions_type=0):
    # return {
    #     "province":
    #         "上海",
    #     "city":
    #         "青浦区",
    #     "adcode":
    #         "310118",
    #     "weather":
    #         "阴",
    #     "temperature":
    #         "14",
    #     "winddirection":
    #         "北",
    #     "windpower":
    #         "≤3",
    #     "humidity":
    #         "95",
    #     "reporttime":
    #         "2023-05-07 21:33:52",
    #     "temperature_float":
    #         "14.0",
    #     "humidity_float":
    #         "95.0"
    # }
    extensions = "all" if extensions_type == 1 else "base"
    weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={config.gaode_key()}&city={get_city_code()}&extensions={extensions}"

    response = requests.get(url=weather_url).json()

    return response['lives'][0]


def get_all_weather(extensions_type=1):
    pass
    # extensions = "all" if extensions_type == 1 else "base"
    # url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={config.gaode_key()}&city={get_city_code()}&extensions={extensions}"

    # payload = {}
    # headers = {}

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)


def write_file(file_path, file_data):
    file = open(file_path, "w")
    file.write(file_data)
    file.close()


def read_file(file_path):
    try:
        f = open(file_path, 'r')  # 打开文件
        data = f.read()  # 读取文件内容
        f.close()  # 确保文件被关闭
        return data
    except:
        return "{}"


'''
定时器
second 定时秒，单位毫秒1000毫秒
fun 执行的函数
https://www.micropython.org.cn/forum/viewtopic.php?f=10&t=1775
'''
