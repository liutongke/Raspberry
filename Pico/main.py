import ssd1306py as lcd
import font
lcd.init_i2c(5, 4, 128, 64, 0)


lcd.set_font(font.font16, 16)
lcd.text_cn('天气', 0, 0, 16)
lcd.show()
