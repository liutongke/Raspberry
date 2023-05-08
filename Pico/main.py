import ssd1306py as lcd
import font
import time
import Tools
import wlan


def main():
    lcd.init_i2c(5, 4, 128, 64, 0)
    lcd.set_font(font.font16, 16)
    # lcd.text('05-06', 0, 0, 16)
    lcd.text_cn("十一月十七", 45, 0, 16)
    lcd.text_cn("周", 0, 16, 16)
    # lcd.text_cn("日", 0, 32, 16)

    # 时
    # lcd.text('18', 16, 16, 32)
    # 秒
    lcd.text('5', 48, 16, 16)
    lcd.text('9', 48, 32, 16)
    # 分
    lcd.text('03', 56, 16, 32)
    lcd.text_cn('一', 88, 16, 16)
    lcd.text_cn('二', 104, 16, 16)
    lcd.text_cn('三', 88, 32, 16)
    lcd.text_cn('四', 104, 32, 16)
    # lcd.text_cn('上海多云台风℃', 0, 48, 16)
    # lcd.text('25', 64, 48, 16)
    # lcd.text_cn('实时上', 0, 0, 16)
    # lcd.text("333333:", 32, 0, 16)
    lcd.show()


'''
天气
{
    "status": "1",
    "count": "1",
    "info": "OK",
    "infocode": "10000",
    "lives": [
        {
            "province": "上海",
            "city": "上海市",
            "adcode": "310000",
            "weather": "多云",
            "temperature": "20",
            "winddirection": "东",
            "windpower": "≤3",
            "humidity": "72",
            "reporttime": "2023-05-02 22:03:40",
            "temperature_float": "20.0",
            "humidity_float": "72.0"
        }
    ]
}
lcd.text_cn('上海多云台风℃', 0, 48, 16)
'''


def weather():
    weather_info = Tools.get_base_weather()
    Tools.write_file('weather_info.json', Tools.json_encode(weather_info))
    text = '%s%s' % (weather_info['city'],
                     weather_info['weather']
                     )

    lcd.text_cn(text, 0, 48, 16)

    city_len = 16 * len(text)
    tmp = str(weather_info['temperature'])
    lcd.text(tmp, city_len, 48, 16)
    tmp_len = 8 * len(tmp)
    lcd.text_cn('℃', city_len + tmp_len, 48, 16)


'''
    # 时
    lcd.text('18', 16, 16, 32)
'''


def hour():
    t = tm.getNow(8)
    # t = time.localtime(time.time())

    if len(str(t[3])) == 1:
        lcd.text('0', 16, 16, 32)
        lcd.text(str(t[3]), 32, 16, 32)
    else:
        lcd.text(str(t[3]), 16, 16, 32)


'''
    # 分
    lcd.text('03', 56, 16, 32)
'''


def minute():
    t = tm.getNow(8)
    # t = time.localtime(time.time())

    if len(str(t[4])) == 1:
        lcd.text('0', 56, 16, 32)
        lcd.text(str(t[4]), 72, 16, 32)
    else:
        lcd.text(str(t[4]), 56, 16, 32)


'''
    # lcd.text_cn("日", 0, 32, 16)
周一至周日的工作日是 0-6
'''


def week():
    t = tm.getNow(8)
    # t = time.localtime(time.time())
    weekday = {
        '0': '一',
        '1': '二',
        '2': '三',
        '3': '四',
        '4': '五',
        '5': '六',
        '6': '日',
    }
    # print(str(t[6]), t[6])
    lcd.text_cn(weekday[str(t[6])], 0, 32, 16)


'''
    # 秒
    lcd.text('5', 48, 16, 16)
    lcd.text('9', 48, 32, 16)
'''


def second():
    t = tm.getNow(8)
    # t = time.localtime(time.time())
    # print('年', t[0])
    # print('月', t[1])
    # print('日', t[2])
    # print('时', t[3])
    # print('分', t[4])
    # print('秒', t[5])
    # lcd.text('5', 48, 16, 16)
    # lcd.text('9', 48, 32, 16)
    if len(str(t[5])) == 1:
        lcd.text('0', 48, 16, 16)
        lcd.text(str(t[5]), 48, 32, 16)
    else:
        for index, ch in enumerate(str(t[5])):
            if index == 0:
                lcd.text(str(ch), 48, 16, 16)
            else:
                lcd.text(str(ch), 48, 32, 16)
    # lcd.text('0', 48, 16, 16)
    # lcd.text(str(t[5]), 48, 32, 16)
    lcd.show()


'''
lcd.text('05-06', 0, 0, 16)
日期
'''


def month():
    t = tm.getNow(8)
    # t = time.localtime(time.time())
    m = str(t[1])
    d = str(t[2])
    if len(m) == 1:
        m = "0%s" % m
    if len(d) == 1:
        d = "0%s" % d

    lcd.text("%s-%s" % (m, d), 0, 0, 16)


'''
{
    "result": [{
        "date": "2023-05-06",
        "lunar": "三月十七",
        "lunarYear": "兔年",
        "ganzhiYear": "癸卯年",
        "ganzhiMonth": "丁巳月",
        "ganzhiDay": "甲子日",
        "festival": [],
        "fitting": "嫁娶,纳采,祭祀,祈福,出行,动土,上梁,移徙,入宅,破土,安葬",
        "taboo": "祈福,斋醮",
        "solarTerm": "立夏",
        "stDays": "1",
        "nextSt": "小满",
        "nextstDays": "15",
        "moreDetail": {
            "zodiac": "兔",
            "constellation": "金牛座",
            "pzTaboo": "甲不开仓财物耗散，子不问卜自惹祸殃。",
            "foetus": "占门碓外东南",
            "elementYear": "金箔金",
            "elementMonth": "沙中土",
            "star": "心宿（心月狐）",
            "elementDay": "海中金",
            "chong": "马 （戊午）",
            "sha": "南",
            "obsidian": "先胜",
            "twelveGods": "危执位"
        }
    }]
}
# https://www.apispace.com/eolink/api/453456/introduction
'''


def wannianli():
    lcd.text_cn("十一月十七", 45, 0, 16)
    lcd.text_cn('立夏', 88, 16, 16)
    # lcd.text_cn('二', 104, 16, 16)
    lcd.text_cn('兔年', 88, 32, 16)
    # lcd.text_cn('四', 104, 32, 16)


# http://micropython.com.cn/en/latet/library/time.html
if __name__ == '__main__':
    if wlan.Wlan().connect_wifi():
        import tm

        main()
        while True:
            weather()
            second()
            hour()
            minute()
            week()
            month()
            wannianli()
            time.sleep(0.1)
