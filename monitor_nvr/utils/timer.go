package utils

import (
	"fmt"
	"os"
	"time"
)

func Task(hub *Hub) {
	PingTimer(clearTimeOutDevice, hub, 1*time.Second)
	PingTimer(picToVideo, hub, 1800*time.Second)
}

func picToVideo(param interface{}) {
	camList := CamParam()
	dir, _ := os.Getwd()
	for deviceId, camInfo := range camList {
		filePath := fmt.Sprintf("%s/images/%s/%s", dir, deviceId, GetPrevHourId())
		outputFile := fmt.Sprintf("%s/video/%s-%s.avi", dir, deviceId, GetPrevHourId())
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
