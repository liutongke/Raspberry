import network
import urequests

import config


def downloads():
    # 下载文件的URL
    url = "http://192.168.1.106:9900/main.py"

    # 发送GET请求并获取响应
    response = urequests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 读取文件内容
        file_content = response.content
        if chr(file_content[9]) == "1":
            # 将文件内容保存到本地文件
            with open("main.py", "wb") as file:
                file.write(file_content)
                print("文件下载完成")
        else:
            print("不需要更新")
    else:
        print("文件下载失败，状态码：", response.status_code)

    # 关闭响应连接
    response.close()


# 连接wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(config.get_wlan_ssid(), config.get_wlan_passwd())

    while not wlan.isconnected():
        pass
print('网络配置:', wlan.ifconfig())
downloads()  # 下载文件
