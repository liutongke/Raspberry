package utils

import (
	"fmt"
	"math/rand"
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
}

// 创建工作work
func (p *Pool) startOneWork(workerID int, taskQueue chan *SendData) {
	fmt.Println("Worker Pool ID = ", workerID, " is started.")
	//Wg.Done()
	//不断的等待队列中的消息
	for {
		select {
		//有消息则取出队列的Request，并执行绑定的业务方法
		case request := <-taskQueue:

			//fmt.Printf("接收到的任务信息：workdId:%d,数据：%s,idx：%d\n", workerID, request.DeviceId, request.idx)
			filePath := fmt.Sprintf("%s%s/%s", ImagePath(), request.DeviceId, GetNowHourId())
			//fmt.Println(!DirIsExist(filePath), filePath)
			if !DirIsExist(filePath) {
				MkDir(filePath)
			}
			SaveImages(fmt.Sprintf("%s/%d.jpg", filePath, request.idx), request.Data)
			//time.Sleep(1 * time.Second)
			//WgSendData.Done()
		}
	}
}

type SendData struct {
	DeviceId string
	Data     []byte
	idx      int64
}

// 生产者
func (p *Pool) SendToWork(data *SendData) {
	i := rand.Intn(9)
	p.pool[i] <- data
}

//func main() {
//	Wg.Add(MaxPool)
//	pool := NewPool()
//	pool.startPool()
//
//	Wg.Wait()
//
//	for i := 0; i <= 100; i++ {
//		WgSendData.Add(1)
//
//		//生产者，投递任务
//		pool.SendToWork(&SendData{
//			Data: i,
//		})
//	}
//
//	WgSendData.Wait()
//}
