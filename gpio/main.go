package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"os/exec"
)

type Ch struct {
	DeviceId string
	Data     []byte
}

func decodePayload(byte_data []byte) (string, []byte) {
	// 将字节流转换为int32
	value := int32(binary.BigEndian.Uint32(byte_data[:4]))
	//fmt.Println(value) // 输出: 1
	device_id := string(byte_data[4 : 4+value])
	//fmt.Println(str)

	return device_id, byte_data[4+value:]
}

// UDP server端
func main() {
	ch := make(chan Ch, 1000)
	go rtmp_steam_push(ch)

	listen, err := net.ListenUDP("udp", &net.UDPAddr{
		IP:   net.IPv4(0, 0, 0, 0),
		Port: 9090,
	})
	if err != nil {
		fmt.Println("listen failed, err:", err)
		return
	}
	defer listen.Close()
	for {
		var data [65535]byte
		n, _, err := listen.ReadFromUDP(data[:]) // 接收数据
		if err != nil {
			fmt.Println("read udp failed, err:", err)
			continue
		}

		deviceId, byte_data := decodePayload(data[:n])
		ch <- Ch{
			DeviceId: deviceId,
			Data:     byte_data,
		}
		//fmt.Println(deviceId)
		//fmt.Printf("data:%v addr:%v count:%v\n", string(data[:n]), addr, n)
		//_, err = listen.WriteToUDP(data[:n], addr) // 发送数据
		//if err != nil {
		//	fmt.Println("write to udp failed, err:", err)
		//	continue
		//}
	}
}
func rtmp_steam_push(ch chan Ch) {
	rtmpURL := "rtmp://192.168.1.107:1935/live/go1"

	// 创建FFmpeg命令
	ffmpegCmd := exec.Command("ffmpeg",
		"-y",
		"-f", "image2pipe",
		"-c:v", "mjpeg",
		"-r", "6", // 设置帧率
		"-i", "-",
		"-c:v", "libx264",
		"-pix_fmt", "yuv420p",
		"-f", "flv",
		rtmpURL,
	)

	// 获取FFmpeg命令的标准输入管道
	pipeIn, err := ffmpegCmd.StdinPipe()
	if err != nil {
		fmt.Println("Error getting FFmpeg stdin pipe:", err)
		return
	}

	// 启动FFmpeg进程
	err = ffmpegCmd.Start()
	if err != nil {
		fmt.Println("Error starting FFmpeg:", err)
		return
	}

	// 逐个推送图片帧
	for {
		select {
		case v := <-ch:
			// 将图片数据写入FFmpeg的标准输入管道
			_, err = io.Copy(pipeIn, bytes.NewReader(v.Data))
			if err != nil {
				fmt.Println("Error writing image data to FFmpeg:", err)
				continue
			}
			fmt.Printf("DeviceId:%s time:%s \n", v.DeviceId, GetNowStr())
			// 等待一段时间，模拟帧率
			//time.Sleep(time.Second / 10)
		}
	}

	// 关闭FFmpeg的标准输入管道，等待推流操作完成
	pipeIn.Close()
	err = ffmpegCmd.Wait()
	if err != nil {
		fmt.Println("Error waiting for FFmpeg:", err)
		return
	}

	fmt.Println("Image frames streamed successfully.")
}
