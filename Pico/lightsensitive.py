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
    adc_light = machine.ADC(machine.Pin(26))
    res = adc_light.read_u16()
    res = ((res >> 8) & 0xff) | (res << 8) & 0xff00
    res = round(res / (2 * 1.2), 2)
    result = "光照强度: " + str(res) + "lux"
    return result
