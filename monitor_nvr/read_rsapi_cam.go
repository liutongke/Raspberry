package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/hybridgroup/mjpeg"
)

func main() {
	// 创建一个 MJPEG 流
	stream := mjpeg.NewStream()

	// 启动一个 Goroutine 来读取摄像头视频流
	go func() {
		for {
			// 打开摄像头设备
			cam, err := os.Open("/dev/video0")
			if err != nil {
				log.Fatal(err)
			}
			defer cam.Close()

			// 从摄像头设备中读取数据并写入 MJPEG 流
			for {
				buf := make([]byte, 4096)
				n, err := cam.Read(buf)
				if err != nil {
					if err == io.EOF {
						// 设备流结束，重新打开摄像头
						break
					}
					log.Fatal(err)
				}
				// 将数据写入 MJPEG 流
				stream.UpdateJPEG(buf[:n])
				time.Sleep(30 * time.Millisecond)
			}
		}
	}()

	// 设置 HTTP 处理函数，将 MJPEG 流输出为 HTTP 响应
	http.Handle("/", stream)
	fmt.Println("start")
	log.Fatal(http.ListenAndServe(":7999", nil))
}
