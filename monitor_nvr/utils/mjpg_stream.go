package utils

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"net/http"
	"os"
)

// mjpg流媒体服务器
func (h *Hub) streamHandler(context *gin.Context) {
	// 设置响应头
	context.Writer.Header().Set("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")

	// 无限循环，持续发送图像流
	for {
		select {
		case v := <-h.MjpgStream:
			imageData := v.Data
			// 读取图像数据
			//imageData, err := readImage()
			//if err != nil {
			//	fmt.Println("Failed to read image:", err)
			//	return
			//}

			// 写入分隔符和图像数据
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

			// 暂停一段时间
			//time.Sleep(100 * time.Millisecond)
		}

	}
}

// 读取图像数据（示例函数，需要根据实际情况实现）
func readImage() ([]byte, error) {
	// 从文件系统中打开图像文件
	file, err := os.Open("test3.jpg")
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
