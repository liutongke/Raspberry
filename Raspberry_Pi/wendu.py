# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# print('过一秒钟休眠')
# time.sleep(5)
# print('休眠了五秒钟')
# count = 0

while True:
    # while (count < 9):
    # -*- coding: utf-8 -*-  
    # 打开文件
    file = open("/sys/class/thermal/thermal_zone0/temp")
    # 读取结果，并转换为浮点数
    temp = float(file.read()) / 1000
    # 关闭文件
    file.close()
    if temp > float(50):
        # 大于这个温度电量灯泡

        # ss = '温度大于四十二度，当前温度' + str(temp)
        # print(ss)
        # print('温度大于四十二度，当前温度'temp)
        # 指定针脚使用方式
        GPIO.setmode(GPIO.BCM)
        # 禁用警告
        GPIO.setwarnings(False)

        R, G, B = 15, 18, 14

        # 指定引脚
        GPIO.setup(R, GPIO.OUT)
        GPIO.setup(G, GPIO.OUT)
        GPIO.setup(B, GPIO.OUT)

        pwmR = GPIO.PWM(R, 70)
        pwmG = GPIO.PWM(G, 70)
        pwmB = GPIO.PWM(B, 70)

        pwmR.start(0)
        pwmG.start(0)
        pwmB.start(0)

        try:

            t = 0.4
            while True:
                # 红色灯全亮，蓝灯，绿灯全暗（红色）
                pwmR.ChangeDutyCycle(0)
                pwmG.ChangeDutyCycle(100)
                pwmB.ChangeDutyCycle(100)
                time.sleep(t)

                # 绿色灯全亮，红灯，蓝灯全暗（绿色）
                pwmR.ChangeDutyCycle(100)
                pwmG.ChangeDutyCycle(0)
                pwmB.ChangeDutyCycle(100)
                time.sleep(t)

                # 蓝色灯全亮，红灯，绿灯全暗（蓝色）
                pwmR.ChangeDutyCycle(100)
                pwmG.ChangeDutyCycle(100)
                pwmB.ChangeDutyCycle(0)
                time.sleep(t)

                # 红灯，绿灯全亮，蓝灯全暗（黄色）
                pwmR.ChangeDutyCycle(0)
                pwmG.ChangeDutyCycle(0)
                pwmB.ChangeDutyCycle(100)
                time.sleep(t)

                # 红灯，蓝灯全亮，绿灯全暗（洋红色）
                pwmR.ChangeDutyCycle(0)
                pwmG.ChangeDutyCycle(100)
                pwmB.ChangeDutyCycle(0)
                time.sleep(t)

                # 绿灯，蓝灯全亮，红灯全暗（青色）
                pwmR.ChangeDutyCycle(100)
                pwmG.ChangeDutyCycle(0)
                pwmB.ChangeDutyCycle(0)
                time.sleep(t)

                # 红灯，绿灯，蓝灯全亮（白色）
                pwmR.ChangeDutyCycle(0)
                pwmG.ChangeDutyCycle(0)
                pwmB.ChangeDutyCycle(0)
                time.sleep(t)

                # 调整红绿蓝LED的各个颜色的亮度组合出各种颜色
                for r in xrange(0, 101, 20):
                    pwmR.ChangeDutyCycle(r)
                    for g in xrange(0, 101, 20):
                        pwmG.ChangeDutyCycle(g)
                        for b in xrange(0, 101, 20):
                            pwmB.ChangeDutyCycle(b)
                            time.sleep(0.01)

        except KeyboardInterrupt:
            pass

        pwmR.stop()
        pwmG.stop()
        pwmB.stop()

        RPi.GPIO.cleanup()
    else:
        # print('温度小于四十二度，当前温度'temp)
        # ss = '温度大于四十二度，当前温度' + str(temp)
        # print(ss)
        # 低于这个温度熄灭灯泡
        print('温度正常')
        # count = count + 1
        # print(count'循环结束')
