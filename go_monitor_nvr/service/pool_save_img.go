package service

import (
	"fmt"
	"math/rand"
	"monitor/nvr/config"
	"monitor/nvr/utils"
)

type Pool struct {
	pool []chan *SendData
}

var (
	MaxPool  = 10   //消费者最大数量
	capacity = 1000 //队列容量
	//Wg         sync.WaitGroup
	//WgSendData sync.WaitGroup
)

func NewPool() *Pool {
	return &Pool{pool: make([]chan *SendData, MaxPool)}
}

// 生成工作work
func (p *Pool) startPool() {
	for i := 0; i < MaxPool; i++ {
		p.pool[i] = make(chan *SendData, capacity)
		go p.startOneWork(i, p.pool[i])
	}
	utils.EchoSuccess("The image processing thread pool starts successfully")
}

// 创建工作work
func (p *Pool) startOneWork(workerID int, taskQueue chan *SendData) {
	//fmt.Println("Worker Pool ID = ", workerID, " is started.")
	//Wg.Done()
	//不断的等待队列中的消息
	for {
		select {
		//有消息则取出队列的Request，并执行绑定的业务方法
		case request := <-taskQueue:

			//fmt.Printf("接收到的任务信息：workdId:%d,数据：%s,idx：%d\n", workerID, request.DeviceId, request.idx)
			filePath := fmt.Sprintf("%s%s/%s", config.ImagePath(), request.DeviceId, utils.GetNowHourId())

			utils.MkDirAll(filePath) //不存在则创建，存在则跳过
			utils.SaveImages(fmt.Sprintf("%s/%d.jpg", filePath, request.Idx), request.Data)
		}
	}
}

type SendData struct {
	DeviceId string
	Data     []byte
	Idx      int64
}

// 生产者
func (p *Pool) SendToWork(data *SendData) {
	i := rand.Intn(9)
	p.pool[i] <- data
}
