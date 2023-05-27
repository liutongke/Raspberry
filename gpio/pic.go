package main

import (
	"log"
	"os/exec"
	"time"
)

func main() {
	imagePath := "./1.jpg"
	rtmpURL := "rtmp://192.168.1.107:1935/live/go"

	// 构建 FFmpeg 命令
	cmd := exec.Command("ffmpeg",
		"-re",        // 实时推流
		"-loop", "1", // 循环播放图片
		"-i", imagePath, // 输入图片路径
		"-vf", "format=yuv420p", // 视频格式转换
		"-c:v", "libx264", // 视频编码器
		"-preset", "veryfast", // 编码速度
		"-f", "flv", rtmpURL, // 输出为 FLV 格式，推流到 RTMP 服务器
	)

	// 开始推流
	err := cmd.Start()
	if err != nil {
		log.Fatalf("Failed to start FFmpeg: %v", err)
	}

	// 停止推流（示例中停止推流等待 10 秒）
	time.Sleep(1000 * time.Second)
	err = cmd.Process.Kill()
	if err != nil {
		log.Fatalf("Failed to stop FFmpeg: %v", err)
	}

	log.Println("Streaming stopped")
}
