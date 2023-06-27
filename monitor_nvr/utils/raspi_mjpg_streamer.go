package utils

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"sync"
)

type RaspiMjpeg struct {
	Data []byte
}

var (
	RaspiMjpgStream chan *RaspiMjpeg
	rw              sync.RWMutex
)

// SendLibcameraStream 在MJPEG视频格式中，每个帧之间是通过特定的分隔符来进行分隔的。这个分隔符通常由两个字节组成，即`0xFF`和`0xD8`，它们对应的是十进制的255和216。这个分隔符也被称为帧起始标记（Start of Frame marker）或帧头（Frame Header）。
// 在MJPEG视频流中，每个帧都以帧起始标记（`0xFFD8`）开始，然后紧接着是帧的数据内容。帧的结束位置可以通过扫描帧数据来确定。帧的结束标记也是由两个字节组成，即`0xFF`和`0xD9`，对应的是十进制的255和217。这个结束标记被称为帧结束标记（End of Frame marker）或帧尾（Frame Tail）。
// 因此，在MJPEG视频流中，每个帧的分隔符是以`0xFFD8`作为起始标记和`0xFFD9`作为结束标记。这样可以识别每个帧并进行分割和处理。
func SendLibcameraStream(context *gin.Context) {
	// 设置响应头
	context.Writer.Header().Set("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")

	for {
		select {
		case v, ok := <-RaspiMjpgStream:
			if ok {
				imageData := v.Data

				header := strings.Builder{}
				header.WriteString("--boundarydonotcross\r\n")
				header.WriteString("Content-Type: image/jpeg\r\n")
				header.WriteString(fmt.Sprintf("Content-Length: %d\r\n\r\n", len(imageData)))

				context.Writer.WriteString(header.String())
				context.Writer.Write(imageData)

				// 强制刷新缓冲区，将数据发送到客户端
				flusher, ok := context.Writer.(http.Flusher)
				if !ok {
					log.Println("Flusher not supported")
					return
				}
				flusher.Flush()
			}
		}
	}
}
func saveImg(frameCount int, imageData []byte) {
	rw.Lock()
	defer rw.Unlock()
	filename := fmt.Sprintf("frame%d.jpg", frameCount)
	err := ioutil.WriteFile(filename, imageData, 0644)
	if err != nil {
		log.Fatal(err)
	}
}
