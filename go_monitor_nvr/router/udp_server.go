package router

import (
	"log"
	"monitor/nvr/config"
	"monitor/nvr/service"
	"monitor/nvr/utils"
	"net"
)

func StartUdp() {
	hub := service.StartClientHub()
	go Http(hub)
	service.Task(hub) //启动定时任务
	if utils.IsRaspi() {
		service.StartRaspiCam()
	}
	listen, err := net.ListenUDP("udp", &net.UDPAddr{
		IP:   net.IPv4(0, 0, 0, 0),
		Port: config.UdpPort(),
	})

	if err != nil {
		log.Fatalf("listen failed, err:%v", err)
	}

	utils.EchoSuccess("The udp server started successfully")

	defer func(listen *net.UDPConn) {
		err := listen.Close()
		if err != nil {
			log.Printf("udp close err: %v\n", err)
		}
	}(listen)

	for {
		var data [65535]byte
		n, _, udpErr := listen.ReadFromUDP(data[:]) // 接收数据
		if udpErr != nil {
			log.Printf("read udp failed, err: %v", udpErr)
			continue
		}

		deviceId, byteData := utils.DecodePayload(data[:n])

		//发送给ffmpeg推流处理
		hub.Ch <- &service.RtmpStreamPushCh{
			DeviceId: deviceId,
			Data:     byteData,
			Idx:      utils.GetMicroseconds(),
		} //传给ffmpeg推流服务器
		hub.UdpMjpgStream <- &service.RtmpStreamPushCh{
			DeviceId: deviceId,
			Data:     byteData,
			Idx:      utils.GetMicroseconds(),
		} //传给mjpg-streamer

		//_, err = listen.WriteToUDP(data[:n], UDPAddr) // 发送数据
		//if err != nil {
		//	fmt.Println("write to udp failed, err:", err)
		//	continue
		//}
	}
}
