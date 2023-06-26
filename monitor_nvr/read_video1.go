package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/exec"
)

func main() {
	// 执行 libcamera-vid 命令，并通过管道获取输出流
	cmd := exec.Command("libcamera-vid", "-t", "10000", "--codec", "mjpeg", "-o", "-")
	stdoutPipe, err := cmd.StdoutPipe()
	if err != nil {
		log.Fatal(err)
	}
	defer stdoutPipe.Close()

	// 启动命令
	err = cmd.Start()
	if err != nil {
		log.Fatal(err)
	}

	// 创建用于保存图像的文件
	fileIndex := 1
	fileName := fmt.Sprintf("image%d.jpg", fileIndex)
	file, err := os.Create(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// 读取 MJPEG 流并保存图像
	scanner := bufio.NewScanner(stdoutPipe)
	for scanner.Scan() {
		line := scanner.Bytes()

		// 检查是否是分隔符（0xFF 0xD8）
		if len(line) >= 2 && line[0] == 0xFF && line[1] == 0xD8 {
			// 保存上一帧图像
			err := saveImage(file, fileName)
			if err != nil {
				log.Fatal(err)
			}

			// 创建新的文件保存下一帧图像
			fileIndex++
			fileName = fmt.Sprintf("image%d.jpg", fileIndex)
			file, err = os.Create(fileName)
			if err != nil {
				log.Fatal(err)
			}
			defer file.Close()
		}

		// 将数据写入当前图像文件
		_, err := file.Write(line)
		if err != nil {
			log.Fatal(err)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	// 等待命令执行完成
	err = cmd.Wait()
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Image saving completed.")
}

func saveImage(file *os.File, fileName string) error {
	err := file.Sync()
	if err != nil {
		return err
	}

	log.Printf("Image saved: %s\n", fileName)
	return nil
}
