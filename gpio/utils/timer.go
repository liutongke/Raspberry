package utils

import (
	"time"
)

func PingTimer(hub *Hub) {
	// 创建一个定时器，每隔 1 秒触发一次
	timer := time.NewTicker(1 * time.Second)

	// 启动一个 goroutine 处理定时任务
	go func() {
		for {
			select {
			case <-timer.C:
				// 定时任务的逻辑处理
				//fmt.Println("定时任务触发：", time.Now())
				hub.Heart <- 1
			}
		}
	}()

	// 主 goroutine 继续执行其他操作
	// 这里可以添加你的业务逻辑代码

	// 让主 goroutine 持续运行，避免程序退出
	select {}
}
