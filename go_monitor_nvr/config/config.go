package config

import (
	"fmt"
	"os"
)

type Cam struct {
	Fps         int
	Width       int
	Height      int
	RtmpUrl     string //推流地址
	VideoFlvUrl string //前端播放地址
	Video       string //前端的class节点
}

func CamParam() map[string]Cam {
	conf := map[string]Cam{
		"a0b765593494": {
			Fps:         6,
			Width:       800,
			Height:      600,
			RtmpUrl:     "rtmp://192.168.1.106:1935/live/esp32",
			VideoFlvUrl: "http://192.168.1.107:8080/live/esp32.flv",
			Video:       ".video",
		},
		"RaspberryPi": {
			Fps:         30,
			Width:       1280,
			Height:      720,
			RtmpUrl:     "rtmp://192.168.1.106:1935/live/raspi-3b",
			VideoFlvUrl: "http://192.168.1.107:8080/live/raspi-3b.flv",
			Video:       ".video1",
		},
	}
	return conf
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

// KeepVideoTm 保留多长时间视频资料
func KeepVideoTm() int {
	return 24 * 10
}

func IsDebug() bool {
	return false
}

// SaveVideo 是否开启保存视频，srs如果开了DVR功能可以关闭 false关闭true开启
func SaveVideo() bool {
	return false
}

// SavePic 是否开启保存每帧照片 false关闭true开启
func SavePic() bool {
	return false
}

func ServerPort() int {
	return 9091
}
func UdpPort() int {
	return 9090
}
