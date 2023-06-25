package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os/exec"
)

func main() {
	log.Println("开始")
	// 执行 libcamera-vid 命令，并通过管道获取输出流
	cmd := exec.Command("libcamera-vid", "-t", "5000", "--codec", "mjpeg", "-o", "-")
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

	mains(stdoutPipe)

	// 等待命令执行完成
	err = cmd.Wait()
	if err != nil {
		log.Fatal(err)
	}
	log.Println("视频保存完成")
}

func mains(stdoutPipe io.ReadCloser) {
	// 假设dataStream是输入的MJPEG数据流
	//var dataStream []byte

	// 使用bufio.NewReader创建一个带缓冲的Reader
	reader := bufio.NewReader(stdoutPipe)

	frameCount := 0

	// 循环读取数据流并处理帧
	for {
		// 读取一行数据，直到遇到'\n'为止
		line, err := reader.ReadBytes('\n')
		if err != nil {
			if err == io.EOF {
				// 数据流已结束
				break
			}
			log.Fatal(err)
		}

		// 搜索以0xFFD8开头的帧
		startIndex := bytes.Index(line, []byte{0xFF, 0xD8})
		if startIndex != -1 {
			// 找到帧的起始位置

			// 继续读取数据，直到遇到以0xFFD9结尾的帧
			frameData := make([]byte, 0)
			frameData = append(frameData, line[startIndex:]...)

			for {
				line, err = reader.ReadBytes('\n')
				if err != nil {
					if err == io.EOF {
						// 数据流已结束
						break
					}
					log.Fatal(err)
				}

				endIndex := bytes.Index(line, []byte{0xFF, 0xD9})
				if endIndex != -1 {
					// 找到帧的结束位置
					frameData = append(frameData, line[:endIndex+2]...)
					break
				}

				// 继续读取数据并添加到帧数据中
				frameData = append(frameData, line...)
			}

			// 处理帧数据
			// 保存帧为图像文件
			filename := fmt.Sprintf("frame%d.jpg", frameCount)
			err := ioutil.WriteFile(filename, frameData, 0644)
			if err != nil {
				log.Fatal(err)
			}
			frameCount++
		}
	}

	log.Printf("总共读取到%d帧", frameCount)
}

//在MJPEG视频格式中，每个帧之间是通过特定的分隔符来进行分隔的。这个分隔符通常由两个字节组成，即`0xFF`和`0xD8`，它们对应的是十进制的255和216。这个分隔符也被称为帧起始标记（Start of Frame marker）或帧头（Frame Header）。
//
//在MJPEG视频流中，每个帧都以帧起始标记（`0xFFD8`）开始，然后紧接着是帧的数据内容。帧的结束位置可以通过扫描帧数据来确定。帧的结束标记也是由两个字节组成，即`0xFF`和`0xD9`，对应的是十进制的255和217。这个结束标记被称为帧结束标记（End of Frame marker）或帧尾（Frame Tail）。
//
//因此，在MJPEG视频流中，每个帧的分隔符是以`0xFFD8`作为起始标记和`0xFFD9`作为结束标记。这样可以识别每个帧并进行分割和处理。
