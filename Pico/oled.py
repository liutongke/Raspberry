# http://micropython.circuitpython.com.cn/en/latet/esp8266/tutorial/ssd1306.html

# display.poweroff()     # power off the display, pixels persist in memory
# display.poweron()      # power on the display, pixels redrawn
# display.contrast(0)    # dim
# display.contrast(255)  # bright
# display.invert(1)      # display inverted
# display.invert(0)      # display normal
# display.rotate(True)   # rotate 180 degrees
# display.rotate(False)  # rotate 0 degrees
# display.show()         # write the contents of the FrameBuffer to display memory


# display.fill(0)                         # fill entire screen with colour=0
# display.pixel(0, 10)                    # get pixel at x=0, y=10
# display.pixel(0, 10, 1)                 # set pixel at x=0, y=10 to colour=1
# display.hline(0, 8, 4, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
# display.vline(0, 8, 4, 1)               # draw vertical line x=0, y=8, height=4, colour=1
# display.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63
# display.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 107,43, colour=1
# display.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 107,43, colour=1
# display.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1
# display.scroll(20, 0)                   # scroll 20 pixels to the right

# display.poweroff() # 关闭显示器，像素保留在内存中
# display.poweron() # 开启显示器，重绘像素
# display.contrast(0) # 暗淡
# display.contrast(255) # 明亮
# display.invert(1) # 反转显示
# display.invert(0) # 正常显示
# display.rotate(True) # 旋转 180 度
# display.rotate(False) # 旋转 0 度
# display.show() # 将FrameBuffer的内容写入显示内存


# display.fill(0) # 用 colour=0 填充整个屏幕
# display.pixel(0, 10) # 获取 x=0, y=10 处的像素
# display.pixel(0, 10, 1) # 将 x=0, y=10 处的像素设置为 colour=1
# display.hline(0, 8, 4, 1) # 画水平线 x=0, y=8, width=4, colour=1
# display.vline(0, 8, 4, 1) # 画垂直线 x=0, y=8, height=4, colour=1
# display.line(0, 0, 127, 63, 1) # 从 0,0 到 127,63 画一条线
# display.rect(10, 10, 107, 43, 1) # 绘制矩形轮廓 10,10 到 107,43, colour=1
# display.fill_rect(10, 10, 107, 43, 1) # 画一个实心矩形 10,10 到 107,43, colour=1
# display.text('Hello World', 0, 0, 1) # 在 x=0, y=0, colour=1 处绘制一些文本
# display.scroll(20, 0) # 向右滚动 20 像素

# 显示.填充(0)
# display.fill_rect(0, 0, 32, 32, 1)
# display.fill_rect(2, 2, 28, 28, 0)
# 显示.vline(9, 8, 22, 1)
# 显示.vline(16, 2, 22, 1)
# 显示.vline(23, 8, 22, 1)
# display.fill_rect(26, 24, 2, 4, 1)
# display.text('MicroPython', 40, 0, 1)
# display.text('SSD1306', 40, 12, 1)
# display.text('OLED 128x64', 40, 24, 1)

# display.fill(0)
# display.fill_rect(0, 0, 32, 32, 1)
# display.fill_rect(2, 2, 28, 28, 0)
# display.vline(9, 8, 22, 1)
# display.vline(16, 2, 22, 1)
# display.vline(23, 8, 22, 1)
# display.fill_rect(26, 24, 2, 4, 1)
# display.text('MicroPython', 40, 0, 1)
# display.text('SSD1306', 40, 12, 1)
# display.text('OLED 128x64', 40, 24, 1)