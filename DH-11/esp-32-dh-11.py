import dht
import machine

d = dht.DHT11(machine.Pin(13))   # data3 pin13
d.measure()
print(d.temperature())
print(d.humidity())
