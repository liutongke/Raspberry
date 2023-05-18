Device is busy or does not respond. Your options:

- wait until it completes current work;
- use Ctrl+C to interrupt current work;
- reset the device and try again;
- check connection properties;
- make sure the device has suitable MicroPython / CircuitPython / firmware;
- make sure the device is not in bootloader mode.

已上烧录后报错，烧录板始终io0接地，需要使用杜邦线面包板接线

MicroPython固定地址：https://github.com/lemariva/micropython-camera-driver

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230515170727.png)

摄像头初始化失败的话，可能插入电脑时候自动运行，删除`boot.py`、`main.py`文件后重新插拔