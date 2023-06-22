import machine
import dht
import time
dht_pin = machine.Pin(2)  # 设置 GPIO 引脚号
dht_sensor = dht.DHT11(dht_pin)
while True:
    dht_sensor.measure()  # 测量温湿度
    temp_c = dht_sensor.temperature()  # 获取温度（摄氏度）
    humidity = dht_sensor.humidity()  # 获取湿度
    print("Temperature: {}°C".format(temp_c))
    print("Humidity: {}%".format(humidity))
    time.sleep(2)  # 延迟一段时间后再次读取
