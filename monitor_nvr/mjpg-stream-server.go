package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

func main() {
	// 设置HTTP路由
	http.HandleFunc("/stream", streamHandler)

	// 启动HTTP服务器
	err := http.ListenAndServe(":9091", nil)
	if err != nil {
		fmt.Println("Failed to start server:", err)
		return
	}
}

func streamHandler(w http.ResponseWriter, req *http.Request) {
	// 设置响应头
	w.Header().Set("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")

	// 无限循环，持续发送图像流
	for {
		// 读取图像数据
		imageData, err := readImage()
		if err != nil {
			fmt.Println("Failed to read image:", err)
			return
		}

		// 写入分隔符和图像数据
		fmt.Fprintf(w, "--boundarydonotcross\r\n")
		fmt.Fprintf(w, "Content-Type: image/jpeg\r\n")
		fmt.Fprintf(w, "Content-Length: %d\r\n\r\n", len(imageData))
		w.Write(imageData)

		// 强制刷新缓冲区，将数据发送到客户端
		flusher, ok := w.(http.Flusher)
		if !ok {
			fmt.Println("Flusher not supported")
			return
		}
		flusher.Flush()

		// 暂停一段时间
		time.Sleep(100 * time.Millisecond)
	}
}

// 读取图像数据（示例函数，需要根据实际情况实现）
func readImage() ([]byte, error) {
	// 从文件系统中打开图像文件
	file, err := os.Open("test.jpg")
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// 读取图像数据到字节切片
	imageData, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, err
	}

	return imageData, nil
}
