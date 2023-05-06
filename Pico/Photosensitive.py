import machine
import utime
# try:
#     adc_light = machine.ADC(machine.Pin(26))
#     while True:
#         light = adc_light.read_u16()
#         print(light)
#         utime.sleep(1)
# except KeyboardInterrupt:
#     print('bye')

# 获取光线强度


def getLight():
    adc_light = machine.ADC(machine.Pin(26))
    light = adc_light.read_u16()
    return light
