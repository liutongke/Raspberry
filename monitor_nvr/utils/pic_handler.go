package utils

import (
	"bytes"
	"fmt"
	"io"
	"os/exec"
	"strconv"
)

type Ch struct {
	DeviceId string
	Data     []byte
	Break    bool
}

func RtmpSteamPush(ch chan *Ch, cam Cam) {
	// 创建FFmpeg命令
	ffmpegCmd := exec.Command("ffmpeg",
		"-y",
		"-f", "image2pipe",
		"-c:v", "mjpeg",
		"-r", strconv.Itoa(cam.Fps), // 设置帧率
		"-i", "-",
		"-s", fmt.Sprintf("%dx%d", cam.Width, cam.Height),
		//"-s", "800x600",
		"-b:v", "2M",
		"-g", "5",
		"-bf", "0",
		"-c:v", "libx264",
		"-pix_fmt", "yuv420p",
		"-preset", "ultrafast",
		"-f", "flv",
		cam.RtmpUrl,
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
			if v.Break { //结束
				goto stopFfmpeg
			}
			//fmt.Println("pic_handler: ", v.DeviceId)
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
			//fmt.Printf("DeviceId:%s time:%s \n", v.DeviceId, GetNowStr())

			// 等待一段时间，模拟帧率
			//time.Sleep(time.Second / 10)
		}
	}

stopFfmpeg:
	// 关闭FFmpeg的标准输入管道，等待推流操作完成
	pipeIn.Close()
	err = ffmpegCmd.Wait()
	if err != nil {
		fmt.Println("Error waiting for FFmpeg:", err)
		return
	}

	fmt.Println("Image frames streamed successfully.")
}
