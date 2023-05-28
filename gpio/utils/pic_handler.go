package utils

import (
	"bytes"
	"fmt"
	"io"
	"os/exec"
)

type Ch struct {
	DeviceId string
	Data     []byte
}

func RtmpSteamPush(ch chan Ch) {
	rtmpURL := "rtmp://192.168.1.107:1935/live/go1"

	// 创建FFmpeg命令
	ffmpegCmd := exec.Command("ffmpeg",
		"-y",
		"-f", "image2pipe",
		"-c:v", "mjpeg",
		"-r", "6", // 设置帧率
		"-i", "-",
		//"-s", fmt.Sprintf("%dx%d", 800, 600),
		"-s", "800x600",
		"-b:v", "2M",
		"-g", "5",
		"-bf", "0",
		"-c:v", "libx264",
		"-pix_fmt", "yuv420p",
		"-preset", "ultrafast",
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
			b, err := MakeWaterMarkerTobyte(v.Data, GetNowStr())
			if err != nil {
				fmt.Printf("MakeWaterMarkerTobyte err:%s", err.Error())
			}
			_, err = io.Copy(pipeIn, bytes.NewReader(b))
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
	//pipeIn.Close()
	//err = ffmpegCmd.Wait()
	//if err != nil {
	//	fmt.Println("Error waiting for FFmpeg:", err)
	//	return
	//}
	//
	//fmt.Println("Image frames streamed successfully.")
}
