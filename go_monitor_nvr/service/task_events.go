package service

import (
	"fmt"
	"monitor/nvr/config"
	"monitor/nvr/utils"
	"path/filepath"
	"strings"
	"time"
)

func Task(hub *Hub) {
	PingTimer(clearTimeOutDevice, hub, 1*time.Second)
	PingTimer(picToVideo, hub, 1800*time.Second)
	PingTimer(keepVideo, hub, 3600*time.Second)
}

// 定时任务将图片转换为视频
func picToVideo(param interface{}) {
	if config.SaveVideo() {
		camList := config.CamParam()
		for deviceId, camInfo := range camList {
			filePath := fmt.Sprintf("%s%s/%s", config.ImagePath(), deviceId, utils.GetPrevHourId())
			outputFile := fmt.Sprintf("%s%s/%s.avi", config.VideoPath(), deviceId, utils.GetPrevHourId())
			if !utils.IsExist(outputFile) {
				PicToVideo(filePath, outputFile, camInfo)
			}
		}
	}
}

// 定时检测超时设备并且清除
func clearTimeOutDevice(param interface{}) {
	ClearTimeOutDevice()
	return
}

// 清除超过保存时间时限视频
func keepVideo(param interface{}) {
	camList := config.CamParam()
	agoTm := utils.GetAgoHourId(config.KeepVideoTm())
	for deviceId, _ := range camList {
		//删除指定图片目录
		imageFilePath, err := utils.GetDirPathName(fmt.Sprintf("%s%s", config.ImagePath(), deviceId))
		if err == nil {
			for _, imageFileName := range imageFilePath {
				if imageFileName < agoTm {
					delFilePath := fmt.Sprintf("%s%s/%s", config.ImagePath(), deviceId, imageFileName)
					utils.DelDir(delFilePath)
				}
			}
		}
		//删除指定视频目录
		videoFilePath := fmt.Sprintf("%s%s", config.VideoPath(), deviceId)
		//fmt.Println(videoFilePath)
		files, err := utils.GetAVIFiles(videoFilePath)
		if err == nil {
			for _, path := range files {
				if extractFileName(path) < agoTm {
					utils.DelDir(path)
				}
				//fmt.Println(path)
			}
		}
	}
}

func extractFileName(path string) string {
	base := filepath.Base(path)
	ext := filepath.Ext(base)
	name := strings.TrimSuffix(base, ext)
	return name
}

type fun func(interface{}) // 声明了一个函数类型

// PingTimer 启动定时器进行心跳检测
func PingTimer(f fun, param interface{}, d time.Duration) {
	go func() {
		ticker := time.NewTicker(d)
		defer ticker.Stop()
		for {
			<-ticker.C //d执行一次
			//发送心跳
			f(param) //调用下函数
		}
	}()
}
