package utils

import (
	"io"
	"log"
	"os"
	"os/exec"
)

func StreamToVideo() {
	// 输入二进制流数据的管道
	inputPipeReader, inputPipeWriter := io.Pipe()
	defer inputPipeReader.Close()
	defer inputPipeWriter.Close()

	// 输出视频文件路径
	outputFilePath := "output.mp4"

	// 构建 ffmpeg 命令
	cmd := exec.Command("ffmpeg", "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", "640x480", "-i", "pipe:0", outputFilePath)

	// 将输入管道连接到 ffmpeg 命令的标准输入
	cmd.Stdin = inputPipeReader

	// 启动 ffmpeg 命令
	err := cmd.Start()
	if err != nil {
		log.Fatal(err)
	}

	// 模拟持续不断输入的二进制流数据
	// 在实际使用中，你需要根据数据来源不断地将二进制流写入输入管道
	go func() {
		inputFile, err := os.Open("input.bin")
		if err != nil {
			log.Fatal(err)
		}
		defer inputFile.Close()

		_, err = io.Copy(inputPipeWriter, inputFile)
		if err != nil {
			log.Fatal(err)
		}

		// 关闭输入管道以通知 ffmpeg 命令输入结束
		inputPipeWriter.Close()
	}()

	// 等待 ffmpeg 命令完成
	err = cmd.Wait()
	if err != nil {
		log.Fatal(err)
	}

	log.Println("视频转换完成！")
}
