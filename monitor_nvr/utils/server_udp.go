package utils

import (
	"log"
	"net"
)

func StartUdp() {
	hub := StartClientHub()
	go Http(hub)
	Task(hub) //启动定时任务

	listen, err := net.ListenUDP("udp", &net.UDPAddr{
		IP:   net.IPv4(0, 0, 0, 0),
		Port: UdpPort(),
	})

	if err != nil {
		log.Fatalf("listen failed, err:%v", err)
	}

	log.Println("udp server start success")

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

		deviceId, byteData := decodePayload(data[:n])

		//发送给ffmpeg推流处理
		hub.Ch <- &RtmpStreamPushCh{
			DeviceId: deviceId,
			Data:     byteData,
			Idx:      GetMicroseconds(),
		} //传给ffmpeg推流服务器
		hub.UdpMjpgStream <- &RtmpStreamPushCh{
			DeviceId: deviceId,
			Data:     byteData,
			Idx:      GetMicroseconds(),
		} //传给mjpg-streamer

		//_, err = listen.WriteToUDP(data[:n], UDPAddr) // 发送数据
		//if err != nil {
		//	fmt.Println("write to udp failed, err:", err)
		//	continue
		//}
	}
}
