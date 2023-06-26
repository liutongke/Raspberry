package main

import (
	"fmt"
	"io"
	"os"
	"os/exec"
)

func main() {
	cmd := exec.Command("libcamera-vid", "--level", "4.2", "--framerate", "30", "--width", "1280", "--height", "720", "-o", "-", "-t", "0", "--denoise", "auto", "-n")

	// 创建管道连接命令的标准输出
	stdoutPipe, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("Error creating stdout pipe:", err)
		return
	}

	// 启动命令
	err = cmd.Start()
	if err != nil {
		fmt.Println("Error starting command:", err)
		return
	}

	// 创建输出文件
	outputFile, err := os.Create("output.h264")
	if err != nil {
		fmt.Println("Error creating output file:", err)
		return
	}
	defer outputFile.Close()

	// 将管道输出写入文件
	_, err = io.Copy(outputFile, stdoutPipe)
	if err != nil {
		fmt.Println("Error writing to output file:", err)
		return
	}

	// 等待命令完成
	err = cmd.Wait()
	if err != nil {
		fmt.Println("Command finished with error:", err)
	}
}
