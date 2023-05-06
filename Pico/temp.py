import machine
import utime

sensor_temp = machine.ADC(4)  # Pico的温度传感器
conversion_factor = 3.3 / (65535)

while True:
    reading = sensor_temp.read_u16() * conversion_factor

    # 0.706V的时候是27度， 每增加0.001721V，温度下降1度
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    utime.sleep(2)
