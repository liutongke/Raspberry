import machine


# try:
#     adc_light = machine.ADC(machine.Pin(26))
#     while True:
#         light = adc_light.read_u16()
#         print(light)
#         utime.sleep(1)
# except KeyboardInterrupt:
#     print('bye')

# 获取光线强度


def get_light():
    adc_light = machine.ADC(machine.Pin(26))
    light = adc_light.read_u16()
    return light


def get_lux():
    light = get_light()
    # 根据传感器规格和转换公式进行转换
    voltage = light * 3.3 / 65535  # 假设使用3.3V供电电压
    lux = some_conversion_function(voltage)  # 使用适当的转换函数进行转换

    return lux
