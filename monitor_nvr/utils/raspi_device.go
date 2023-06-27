package utils

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os/exec"
)

func StartRaspiCam() chan *RaspiMjpeg {
	RaspiMjpgStream = make(chan *RaspiMjpeg, 1000)
	go InitCmd(RaspiMjpgStream)
	return RaspiMjpgStream
}

// https://www.raspberrypi.com/documentation/computers/camera_software.html#common-command-line-options
func InitCmd(ch chan *RaspiMjpeg) {
	log.Println("开始")
	// 执行 libcamera-vid 命令，并通过管道获取输出流
	args := []string{
		"-t", "0",
		"--codec",
		"mjpeg",
		"--quality", "90", //设置 JPEG 质量。100 表示最高质量，50 表示默认值。仅在以 MJPEG 格式保存时适用，100的画面会有撕裂
		"-b", "50000", //增加码率
		"-o", "-",
		"--width", "1280",
		"--height", "720",
		"--framerate", "30",
		"--denoise", "cdn_hq", //降噪模式
	}
	cmd := exec.Command("libcamera-vid", args...)

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
	scanner.Buffer(make([]byte, 1024*350), bufio.MaxScanTokenSize) //增加扫描器的缓冲区大小
	scanner.Split(libcameraScanNalSeparator)

	// 逐个读取分割后的数据片段
	for scanner.Scan() {
		imageData := scanner.Bytes()
		imageData = append(imageData, 255, 217) //补充添加MJPEG图片结束符

		//pic, err := AddWatermarkPic(imageData, GetNowStr())
		//if err != nil {
		//	return
		//}
		ch <- &RaspiMjpeg{
			Data: imageData,
		}

		// 保存帧为图像文件
		//filename := fmt.Sprintf("frame%d.jpg", frameCount)
		//err := ioutil.WriteFile(filename, imageData, 0644)
		//if err != nil {
		//	log.Fatal(err)
		//}
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
func libcameraScanNalSeparator(data []byte, atEOF bool) (advance int, token []byte, err error) {
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
