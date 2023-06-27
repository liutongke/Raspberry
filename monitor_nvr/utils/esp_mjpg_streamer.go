package utils

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

// mjpg流媒体服务器

func (h *Hub) EspMjpgStreamer(context *gin.Context) {
	// 设置响应头
	context.Writer.Header().Set("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")

	// 无限循环，持续发送图像流
	for {
		select {
		case v, ok := <-h.UdpMjpgStream:
			if ok {
				imageData := v.Data
				// 写入分隔符和图像数据
				header := strings.Builder{}
				header.WriteString("--boundarydonotcross\r\n")
				header.WriteString("Content-Type: image/jpeg\r\n")
				header.WriteString(fmt.Sprintf("Content-Length: %d\r\n\r\n", len(imageData)))

				context.Writer.WriteString(header.String())
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
	}
}
