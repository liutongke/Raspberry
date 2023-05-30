package utils

import (
	"fmt"
	"os"
)

type Cam struct {
	Fps     int
	Width   int
	Height  int
	RtmpUrl string
}

func CamParam() map[string]Cam {
	conf := map[string]Cam{
		"a0b765593494": {
			Fps:     6,
			Width:   800,
			Height:  600,
			RtmpUrl: "rtmp://192.168.1.107:1935/live/esp32",
		},
		"RaspberryPi": {
			Fps:     6,
			Width:   800,
			Height:  600,
			RtmpUrl: "rtmp://192.168.1.107:1935/live/raspi-3b",
		},
	}
	return conf
}

func InitDir() {
	camList := CamParam()
	for deviceId, _ := range camList {
		MkDir(fmt.Sprintf("%s%s", ImagePath(), deviceId))
		MkDir(fmt.Sprintf("%s%s", VideoPath(), deviceId))
	}
}

func GetRunDirPath() string {
	dir, _ := os.Getwd()
	return dir
}

// ImagePath 图片保存路径
func ImagePath() string {
	return fmt.Sprintf("%s/data/images/", GetRunDirPath())
}

// VideoPath 保存视频路径
func VideoPath() string {
	return fmt.Sprintf("%s/data/video/", GetRunDirPath())
}

// 保留多长时间视频资料
func KeepVideoTm() int {
	return 24 * 10
}
