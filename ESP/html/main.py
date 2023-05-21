# update=1
# 1更新0不更新 boot.py加载时候更新，MicroPython启动顺序boot.py->main.py
import socket
import network
import camera
import time
import config

# # 连接wifi
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# if not wlan.isconnected():
#     print('connecting to network...')
#     wlan.connect(config.get_wlan_ssid(), config.get_wlan_passwd())
#
#     while not wlan.isconnected():
#         pass
# print('网络配置:', wlan.ifconfig())

# 摄像头初始化
try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)

camera.flip(1)  # 上翻下翻
camera.mirror(1)  # 左/右
camera.framesize(camera.FRAME_SVGA)  # 分辨率
# 选项如下：
# FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
# FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
# FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
# FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
# FRAME_P_FHD FRAME_QSXGA
# 有关详细信息，请查看此链接：https://bit.ly/2YOzizz

camera.speffect(camera.EFFECT_NONE)  # 特效
# 选项如下：
# 效果\无（默认）效果\负效果\ BW效果\红色效果\绿色效果\蓝色效果\复古效果
# EFFECT_NONE (default) EFFECT_NEG \EFFECT_BW\ EFFECT_RED\ EFFECT_GREEN\ EFFECT_BLUE\ EFFECT_RETRO

# 白平衡
# camera.whitebalance(camera.WB_HOME)
# 选项如下：
# WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

# 饱和
camera.saturation(0)
# -2,2（默认为0）. -2灰度
# -2,2 (default 0). -2 grayscale

# 亮度
camera.brightness(0)
# -2,2（默认为0）. 2亮度
# -2,2 (default 0). 2 brightness

# 对比度
camera.contrast(0)
# -2,2（默认为0）.2高对比度
# -2,2 (default 0). 2 highcontrast

# 质量
camera.quality(10)
# 10-63数字越小质量越高

# socket UDP 的创建
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


def get_device_info():
    device_id = config.get_device_id()
    return device_id, len(device_id)


def encode_payload(payload):
    device_id, device_id_len = get_device_info()
    device_id_len_byte_data = device_id_len.to_bytes(4, 'big')  # 将整数转换为字节流
    device_id_byte_data = bytes(device_id, 'utf-8')  # 将字符串转换为字节流
    payload_byte_data = bytes(payload, 'utf-8')  # 将字符串转换为字节流

    merged_data_stream = bytearray(device_id_len_byte_data) + bytearray(device_id_byte_data) + bytearray(
        payload_byte_data)  # 合并字节流
    return merged_data_stream


try:
    while True:
        buf = camera.capture()  # 获取图像数据
        s.sendto(encode_payload(buf),
                 ("192.168.1.106", 9090))  # 向服务器发送图像数据
        time.sleep(0.1)
except:
    pass
finally:
    camera.deinit()
