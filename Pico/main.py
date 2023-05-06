import ssd1306py as lcd
import font
import time


def main():
    lcd.init_i2c(5, 4, 128, 64, 0)
    lcd.set_font(font.font16, 16)
    lcd.text('05-06', 0, 0, 16)
    lcd.text_cn("三月十七", 45, 0, 16)
    lcd.text_cn("周", 0, 16, 16)
    lcd.text_cn("日", 0, 32, 16)

    # 时
    lcd.text('18', 16, 16, 32)
    # 秒
    lcd.text('5', 48, 16, 16)
    lcd.text('9', 48, 32, 16)
    # 分
    lcd.text('03', 56, 16, 32)
    lcd.text_cn('上海多云台风℃', 0, 48, 16)
    # lcd.text('25', 64, 48, 16)
    # lcd.text_cn('实时上', 0, 0, 16)
    # lcd.text("333333:", 32, 0, 16)
    lcd.show()


'''
    # 时
    lcd.text('18', 16, 16, 32)
'''


def hour():
    t = time.localtime(time.time())
    lcd.text(str(t[3]), 16, 16, 32)


'''
    # 分
    lcd.text('03', 56, 16, 32)
'''


def minute():
    t = time.localtime(time.time())
    lcd.text(str(t[4]), 56, 16, 32)


'''
    # 秒
    lcd.text('5', 48, 16, 16)
    lcd.text('9', 48, 32, 16)
'''


def second():
    t = time.localtime(time.time())
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


if __name__ == '__main__':
    # week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    # print(week_list[datetime.date(2022, 2, 22).weekday()])
    main()
    while True:
        second()
        hour()
        minute()
        time.sleep(0.5)
