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
	dir, _ := os.Getwd()
	for deviceId, _ := range camList {
		MkDir(fmt.Sprintf("%s/images/%s", dir, deviceId))
		MkDir(fmt.Sprintf("%s/video/%s", dir, deviceId))
	}
}
