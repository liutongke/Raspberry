import urequests as requests
import json
import config


def json_decode(json_dict_):
    return json.loads(json_dict_)


def json_encode(dict_):
    return json.dumps(dict_,)


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


def get_base_weather(extensions_type=0):
    return {'winddirection': '\u5317', 'humidity_float': '90.0', 'city': '\u4e0a\u6d77\u5e02', 'humidity': '90', 'weather': '\u9634', 'reporttime': '2023-05-05 23:03:45', 'temperature': '222', 'temperature_float': '22.0', 'adcode': '310000', 'windpower': '\u22643', 'province': '\u4e0a\u6d77'}
    # extensions = "all" if extensions_type == 1 else "base"
    # weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={config.gaode_key()}&city={get_city_code()}&extensions={extensions}"

    # response = requests.get(url=weather_url).json()

    # return response['lives'][0]


def get_all_weather(extensions_type=1):
    pass
    # extensions = "all" if extensions_type == 1 else "base"
    # url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={config.gaode_key()}&city={get_city_code()}&extensions={extensions}"

    # payload = {}
    # headers = {}

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
