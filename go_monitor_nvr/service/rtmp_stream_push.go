package service

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"monitor/nvr/config"
	"monitor/nvr/utils"
	"os/exec"
	"strconv"
)

type RtmpStreamPushCh struct {
	DeviceId string
	Data     []byte
	Break    bool
	Idx      int64
}

// RtmpStreamPush 将处理完后的图片推流到rtmp服务器
func RtmpStreamPush(RtmpStreamPushCh chan *RtmpStreamPushCh, cam config.Cam, h *Hub) {
	args := []string{
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
	}
	// 创建FFmpeg命令
	ffmpegCmd := exec.Command("ffmpeg", args...)

	// 获取FFmpeg命令的标准输入管道
	pipeIn, err := ffmpegCmd.StdinPipe()
	if err != nil {
		log.Fatalf("Error getting FFmpeg stdin pipe: %v", err)
		return
	}

	// 启动FFmpeg进程
	err = ffmpegCmd.Start()
	if err != nil {
		log.Fatalf("Error starting FFmpeg: %v", err)
		return
	}

	utils.EchoSuccess(fmt.Sprintf("The rtmp streaming server started successfully and rtmp url:%s", cam.RtmpUrl))

	pipWriteErrNum := 0
	// 逐个推送图片帧
	for {
		select {
		case v := <-RtmpStreamPushCh:
			if v.Break { //结束
				goto stopFfmpeg
			}
			b := v.Data
			// 将图片数据写入FFmpeg的标准输入管道
			//b, err := AddWatermarkPic(v.Data, GetNowStr())
			//if err != nil {
			//	log.Printf("MakeWaterMarkerTobyte err:%s \n", err)
			//} else {
			//fmt.Println(b)
			_, err = io.Copy(pipeIn, bytes.NewReader(b))
			if err != nil {
				log.Printf("Error writing image data to FFmpeg: %v", err)

				if pipWriteErrNum >= 200 {
					//推流服务器出现错误、或者ffmpeg写入管道出现问题
					log.Println("Retry limit reached,stop push streamed")
					goto stopFfmpeg
				}

				pipWriteErrNum++
			}

			if config.SavePic() { //将数据流保存为图片
				pool.SendToWork(&SendData{
					DeviceId: v.DeviceId,
					Data:     b,
					Idx:      v.Idx,
				})
			}
		}
		//}
	}

stopFfmpeg:
	// 关闭FFmpeg的标准输入管道，等待推流操作完成
	pipeIn.Close()
	log.Println("frames streamed complete,stop ffmpeg Service")
	h.Heart <- 1
}
