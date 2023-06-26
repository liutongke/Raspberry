package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os/exec"
)

type Mjpeg struct {
	data []byte
}

func main() {
	ch := make(chan *Mjpeg, 100)
	go startLibcamera(ch)
	r := gin.Default()
	r.GET("/ping", func(context *gin.Context) {
		// 设置响应头
		context.Writer.Header().Set("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")

		// 无限循环，持续发送图像流
		for {
			select {
			case v := <-ch:
				imageData := v.data
				imageData = append(imageData, 255, 217)
				fmt.Fprintf(context.Writer, "--boundarydonotcross\r\n")
				fmt.Fprintf(context.Writer, "Content-Type: image/jpeg\r\n")
				fmt.Fprintf(context.Writer, "Content-Length: %d\r\n\r\n", len(imageData))
				context.Writer.Write(imageData)

				// 强制刷新缓冲区，将数据发送到客户端
				flusher, ok := context.Writer.(http.Flusher)
				if !ok {
					fmt.Println("Flusher not supported")
					return
				}
				flusher.Flush()
			}

		}
	})

	log.Println("start http server prot:%d", 8888)
	http.ListenAndServe(":8888", r)
}

func startLibcamera(ch chan *Mjpeg) {
	log.Println("开始")
	// 执行 libcamera-vid 命令，并通过管道获取输出流
	//cmd := exec.Command("libcamera-vid", "-t", "5000", "--codec", "mjpeg", "-o", "-")
	cmd := exec.Command("libcamera-vid", "-t", "0", "--codec", "mjpeg", "--quality", "90", "--bitrate", "5000000", "-o", "-", "--width", "800", "--height", "600")

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
	scanner.Buffer(make([]byte, 1024*999), bufio.MaxScanTokenSize) //增加扫描器的缓冲区大小
	scanner.Split(libcameraScanNalSeparator)
	frameCount := 1

	// 逐个读取分割后的数据片段
	for scanner.Scan() {
		token := scanner.Bytes()
		ch <- &Mjpeg{
			data: token,
		}
		//fmt.Printf("Token: %s\n", token)

		// 保存帧为图像文件
		//filename := fmt.Sprintf("frame%d.jpg", frameCount)
		//err := ioutil.WriteFile(filename, token, 0644)
		//if err != nil {
		//	log.Fatal(err)
		//}
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
