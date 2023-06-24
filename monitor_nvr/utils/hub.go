package utils

import (
	"log"
	"sync"
)

var clientHub *Hub

// 所有用户管理
type Hub struct {
	Pool        *Pool
	Ch          chan *Ch
	MjpgStream  chan *Ch
	Cam         map[string]bool     //device_id=>True
	CamCh       map[string]chan *Ch //device_id=>ch
	CamLast     map[string]int64    //device_id=>上一次登录时间
	Heart       chan int
	ClientsLock sync.RWMutex // 读写锁
}

func newClientHub() *Hub {
	return &Hub{
		Ch:         make(chan *Ch, 1000),
		MjpgStream: make(chan *Ch, 1000),
		Cam:        make(map[string]bool),
		CamCh:      make(map[string]chan *Ch, 1000),
		CamLast:    make(map[string]int64),
		Heart:      make(chan int, 100),
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
			deviceId := camInfo.DeviceId
			if _, ok := h.Cam[deviceId]; ok { //该终端存在
				//fmt.Println("开始发送数据", deviceId, camInfo.Data)
				h.CamCh[deviceId] <- &Ch{
					DeviceId: deviceId,
					Data:     camInfo.Data,
					Break:    false,
					Idx:      camInfo.Idx,
				}
				h.CamLast[deviceId] = GetNowUnix()
			} else { //不存在创建
				ch := make(chan *Ch, 1000)
				go RtmpStreamPush(ch, CamParam()[deviceId], h)
				ch <- &Ch{
					DeviceId: deviceId,
					Data:     camInfo.Data,
					Break:    false,
					Idx:      camInfo.Idx,
				}
				h.Cam[deviceId] = true
				h.CamCh[deviceId] = ch
				h.CamLast[deviceId] = GetNowUnix()
			}
		case _ = <-h.Heart: //心跳检测
			for deviceId, lastTm := range h.CamLast {
				//fmt.Printf("检测在线设备:%s \n", deviceId)
				log.Printf("出现异常，踢除设备:%s,最后登录时间：%s", deviceId, GetUnixToStr(lastTm, ""))
				h.kickOutDevice(deviceId) //踢除设备
			}
		}
	}
}
func ClearTimeOutDevice() {
	h := GetHub()
	for deviceId, lastTm := range h.CamLast {
		//log.Printf("检测在线设备:%s \n", deviceId)
		if (GetNowUnix() - lastTm) >= 5 {
			log.Printf("踢出连接超时设备:%s", deviceId)
			h.kickOutDevice(deviceId) //踢除设备
		}
	}
}

// 踢掉离线设备
func (h *Hub) kickOutDevice(deviceId string) {
	h.CamCh[deviceId] <- &Ch{
		DeviceId: deviceId,
		Data:     nil,
		Break:    true,
	}
	//删除这些设备
	close(h.CamCh[deviceId])
	delete(h.Cam, deviceId)
	delete(h.CamCh, deviceId)
	delete(h.CamLast, deviceId)
}
