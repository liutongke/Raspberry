package utils

import (
	"fmt"
	"path/filepath"
	"strings"
	"time"
)

func Task(hub *Hub) {
	PingTimer(clearTimeOutDevice, hub, 1*time.Second)
	PingTimer(picToVideo, hub, 1800*time.Second)
	PingTimer(keepVideo, hub, 3600*time.Second)
}

func picToVideo(param interface{}) {
	camList := CamParam()
	for deviceId, camInfo := range camList {
		filePath := fmt.Sprintf("%s%s/%s", ImagePath(), deviceId, GetPrevHourId())
		outputFile := fmt.Sprintf("%s%s/%s.avi", VideoPath(), deviceId, GetPrevHourId())
		if !DirIsExist(outputFile) {
			PicToVideo(filePath, outputFile, camInfo)
		}
	}
}
func clearTimeOutDevice(param interface{}) {
	//fmt.Println("检测超时设备")
	ClearTimeOutDevice()
	return
}

// 保留视频,清除超过保存时间视频
func keepVideo(param interface{}) {
	camList := CamParam()
	agoTm := GetAgoHourId(KeepVideoTm())
	for deviceId, _ := range camList {
		//删除指定图片目录
		imageFilePath, err := GetDirPathName(fmt.Sprintf("%s%s", ImagePath(), deviceId))
		if err == nil {
			for _, imageFileName := range imageFilePath {
				if imageFileName < agoTm {
					delFilePath := fmt.Sprintf("%s%s/%s", ImagePath(), deviceId, imageFileName)
					DelDir(delFilePath)
				}
			}
		}
		//删除指定视频目录
		videoFilePath := fmt.Sprintf("%s%s", VideoPath(), deviceId)
		//fmt.Println(videoFilePath)
		files, err := GetAVIFiles(videoFilePath)
		if err == nil {
			for _, path := range files {
				if extractFileName(path) < agoTm {
					DelDir(path)
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
// 启动定时器进行心跳检测
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

//func PingTimer(hub *Hub) {
//	// 创建一个定时器，每隔 1 秒触发一次
//	timer := time.NewTicker(1 * time.Second)
//
//	// 启动一个 goroutine 处理定时任务
//	go func() {
//		for {
//			select {
//			case <-timer.C:
//				// 定时任务的逻辑处理
//				//fmt.Println("定时任务触发：", time.Now())
//				hub.Heart <- 1
//			}
//		}
//	}()
//
//	// 主 goroutine 继续执行其他操作
//	// 这里可以添加你的业务逻辑代码
//
//	// 让主 goroutine 持续运行，避免程序退出
//	select {}
//}
