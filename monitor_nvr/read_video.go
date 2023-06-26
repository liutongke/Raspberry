package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os/exec"
)

func main() {
	log.Println("开始")
	// 执行 libcamera-vid 命令，并通过管道获取输出流
	//cmd := exec.Command("libcamera-vid", "-t", "5000", "--codec", "mjpeg", "-o", "-")
	cmd := exec.Command("libcamera-vid", "-t", "5000", "--codec", "mjpeg", "-o", "-", "--width", "800", "--height", "600")

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
	//"=================================="
	// 创建一个扫描器，并设置分割函数
	scanner := bufio.NewScanner(stdoutPipe)
	scanner.Split(scanNalSeparator)
	frameCount := 1

	// 逐个读取分割后的数据片段
	for scanner.Scan() {
		token := scanner.Bytes()
		//fmt.Printf("Token: %s\n", token)

		// 保存帧为图像文件
		filename := fmt.Sprintf("frame%d.jpg", frameCount)
		err := ioutil.WriteFile(filename, token, 0644)
		if err != nil {
			log.Fatal(err)
		}
		frameCount++
	}

	if scanner.Err() != nil {
		fmt.Printf("Error: %s\n", scanner.Err())
	}
	//"=================================="
	// 等待命令执行完成
	err = cmd.Wait()
	if err != nil {
		log.Fatal(err)
	}
	log.Println("视频保存完成")
}
func scanNalSeparator(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}

	if i := bytes.Index(data, []byte{0xFF, 0xD9}); i >= 0 {
		return i + len([]byte{0xFF, 0xD9}), data[0:i], nil
	}

	if atEOF {
		return len(data), data, nil
	}

	return 0, nil, nil
}

//在MJPEG视频格式中，每个帧之间是通过特定的分隔符来进行分隔的。这个分隔符通常由两个字节组成，即`0xFF`和`0xD8`，它们对应的是十进制的255和216。这个分隔符也被称为帧起始标记（Start of Frame marker）或帧头（Frame Header）。
//
//在MJPEG视频流中，每个帧都以帧起始标记（`0xFFD8`）开始，然后紧接着是帧的数据内容。帧的结束位置可以通过扫描帧数据来确定。帧的结束标记也是由两个字节组成，即`0xFF`和`0xD9`，对应的是十进制的255和217。这个结束标记被称为帧结束标记（End of Frame marker）或帧尾（Frame Tail）。
//
//因此，在MJPEG视频流中，每个帧的分隔符是以`0xFFD8`作为起始标记和`0xFFD9`作为结束标记。这样可以识别每个帧并进行分割和处理。
