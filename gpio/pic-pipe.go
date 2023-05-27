package main

import (
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"time"
)

func main() {
	imageFolder := "./images"
	rtmpURL := "rtmp://192.168.1.107:1935/live/go1"

	// 获取图片文件列表
	imageFiles, err := getImageFiles(imageFolder)
	if err != nil {
		fmt.Println("Error getting image files:", err)
		return
	}

	// 创建FFmpeg命令
	ffmpegCmd := exec.Command("ffmpeg",
		"-y",
		"-f", "image2pipe",
		"-c:v", "mjpeg",
		"-r", "10", // 设置帧率
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
	for _, imageFile := range imageFiles {
		// 打开图片文件
		file, err := os.Open(imageFile)
		if err != nil {
			fmt.Println("Error opening image file:", err)
			continue
		}

		// 将图片数据写入FFmpeg的标准输入管道
		_, err = io.Copy(pipeIn, file)
		file.Close()
		if err != nil {
			fmt.Println("Error writing image data to FFmpeg:", err)
			continue
		}

		// 等待一段时间，模拟帧率
		time.Sleep(time.Second / 10)
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

// 获取指定文件夹下的图片文件列表
func getImageFiles(folderPath string) ([]string, error) {
	var imageFiles []string

	// 遍历文件夹中的文件
	err := filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
		// 如果是文件且是图片文件，则将其添加到列表中
		if !info.IsDir() && isImageFile(path) {
			imageFiles = append(imageFiles, path)
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	return imageFiles, nil
}

// 检查文件是否为图片文件
func isImageFile(filePath string) bool {
	extension := filepath.Ext(filePath)
	switch extension {
	case ".jpg", ".jpeg", ".png", ".gif":
		return true
	}
	return false
}
