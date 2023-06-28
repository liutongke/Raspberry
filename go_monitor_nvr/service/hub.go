package service

import (
	"fmt"
	"monitor/nvr/config"
	"monitor/nvr/utils"
	"sync"
)

var clientHub *Hub

// 所有用户管理
type Hub struct {
	Pool          *Pool
	Ch            chan *RtmpStreamPushCh
	UdpMjpgStream chan *RtmpStreamPushCh
	Cam           map[string]bool                   //device_id=>True
	CamCh         map[string]chan *RtmpStreamPushCh //device_id=>ch
	CamLast       map[string]int64                  //device_id=>上一次登录时间
	Heart         chan int
	rwMutex       sync.RWMutex // 读写锁
}

func newClientHub() *Hub {
	return &Hub{
		Ch:            make(chan *RtmpStreamPushCh, 1000),
		UdpMjpgStream: make(chan *RtmpStreamPushCh, 1000),
		Cam:           make(map[string]bool),
		CamCh:         make(map[string]chan *RtmpStreamPushCh, 1000),
		CamLast:       make(map[string]int64),
		Heart:         make(chan int, 100),
	}
}

var pool *Pool

func GetHub() *Hub {
	return clientHub
}

// StartClientHub 启动hub
func StartClientHub() *Hub {
	clientHub = newClientHub()
	go clientHub.run()

	pool = NewPool()
	go pool.startPool()

	return clientHub
}

func (h *Hub) run() {
	for {
		select {
		//接收udp处理过来的数据
		case camInfo := <-h.Ch: //
			h.rwMutex.Lock() // 加互斥锁

			deviceId := camInfo.DeviceId
			if _, ok := h.Cam[deviceId]; ok { //该终端存在
				//fmt.Println("开始发送数据", deviceId, camInfo.Data)
				h.CamCh[deviceId] <- &RtmpStreamPushCh{
					DeviceId: deviceId,
					Data:     camInfo.Data,
					Break:    false,
					Idx:      camInfo.Idx,
				}
				h.CamLast[deviceId] = utils.GetNowUnix()

			} else { //不存在创建
				ch := make(chan *RtmpStreamPushCh, 1000)
				go RtmpStreamPush(ch, config.CamParam()[deviceId], h)
				ch <- &RtmpStreamPushCh{
					DeviceId: deviceId,
					Data:     camInfo.Data,
					Break:    false,
					Idx:      camInfo.Idx,
				}
				h.Cam[deviceId] = true
				h.CamCh[deviceId] = ch
				h.CamLast[deviceId] = utils.GetNowUnix()
			}

			h.rwMutex.Unlock() // 解互斥锁
		case _ = <-h.Heart: //心跳检测
			h.rwMutex.Lock() // 加互斥锁
			for deviceId, lastTm := range h.CamLast {
				//fmt.Printf("检测在线设备:%s \n", deviceId)
				utils.EchoError(fmt.Sprintf("心跳检测，踢出设备:%s,最后登录时间：%s", deviceId, utils.GetUnixToStr(lastTm, "")))
				//删除这些设备
				close(h.CamCh[deviceId])
				delete(h.Cam, deviceId)
				delete(h.CamCh, deviceId)
				delete(h.CamLast, deviceId)
			}
			h.rwMutex.Unlock() // 解互斥锁
		}
	}
}
func ClearTimeOutDevice() {
	h := GetHub()
	//h.rwMutex.Lock()         // 加互斥锁
	//defer h.rwMutex.Unlock() // 解互斥锁
	for deviceId, lastTm := range h.CamLast {
		if (utils.GetNowUnix() - lastTm) >= 5 {
			utils.EchoError(fmt.Sprintf("踢出连接超时设备:%s", deviceId))
			if val, ok := h.CamCh[deviceId]; ok {
				val <- &RtmpStreamPushCh{
					DeviceId: deviceId,
					Data:     nil,
					Break:    true,
				} //踢除设备
			}
		}
	}
}
