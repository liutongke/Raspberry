要从标准输出流中提取MJPEG图像帧，您可以使用适当的方法和库来解析MJPEG数据，并将每一帧保存为单独的图像文件。以下是一个示例Python代码，演示了如何从标准输出流中提取MJPEG图像帧：

```python
import sys
import struct

# 定义MJPEG起始标记和结束标记
SOI_MARKER = b'\xff\xd8'  # 图像帧起始标记
EOI_MARKER = b'\xff\xd9'  # 图像帧结束标记

frame_count = 0
frame_data = b''  # 存储当前图像帧的数据

# 从标准输入流读取数据并处理图像帧
while True:
    data = sys.stdin.buffer.read(1024)  # 从标准输入流中读取数据
    if not data:
        break

    frame_data += data

    # 检查是否找到图像帧起始标记和结束标记
    while True:
        start = frame_data.find(SOI_MARKER)
        end = frame_data.find(EOI_MARKER)

        if start != -1 and end != -1:
            # 提取图像帧数据
            frame = frame_data[start:end + 2]

            # 将图像帧保存为文件
            filename = f"frame{frame_count:05d}.jpg"
            with open(filename, 'wb') as f:
                f.write(frame)

            frame_count += 1
            frame_data = frame_data[end + 2:]
        else:
            break
```

您可以将上述代码保存为Python脚本（例如`extract_frames.py`），然后通过将`libcamera-vid`命令的输出流重定向到该脚本来提取MJPEG图像帧。以下是一个示例命令：

```shell
libcamera-vid -t 10000 --codec mjpeg --segment 1 -n -o - | python extract_frames.py
```

执行上述命令后，图像帧将被提取并保存为以`frameXXXXX.jpg`命名的文件，其中`XXXXX`是图像帧的顺序号。