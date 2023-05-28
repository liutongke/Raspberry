package main

import (
	"encoding/binary"
	"fmt"
	"monitor/nvr/utils"
	"net"
)

func decodePayload(byte_data []byte) (string, []byte) {
	// 将字节流转换为int32
	value := int32(binary.BigEndian.Uint32(byte_data[:4]))
	//fmt.Println(value) // 输出: 1
	device_id := string(byte_data[4 : 4+value])
	//fmt.Println(str)

	return device_id, byte_data[4+value:]
}

// UDP server端
func main() {
	hub := utils.StartClientHub()

	go utils.PingTimer(hub) //启动定时任务
	//camList := utils.CamParam()
	//chContainer := make(map[string]chan utils.Ch, len(camList))
	//
	//for deviceId, cam := range camList {
	//	ch := make(chan utils.Ch, 1000)
	//	chContainer[deviceId] = ch
	//	go utils.RtmpSteamPush(ch, cam)
	//}

	listen, err := net.ListenUDP("udp", &net.UDPAddr{
		IP:   net.IPv4(0, 0, 0, 0),
		Port: 9090,
	})
	if err != nil {
		fmt.Println("listen failed, err:", err)
		return
	}
	fmt.Println("udp server start success")
	defer listen.Close()
	for {
		var data [65535]byte
		n, _, err := listen.ReadFromUDP(data[:]) // 接收数据
		if err != nil {
			fmt.Println("read udp failed, err:", err)
			continue
		}

		deviceId, byteData := decodePayload(data[:n])
		//fmt.Printf("udp accept:%s \n", deviceId)
		hub.Ch <- &utils.Ch{
			DeviceId: deviceId,
			Data:     byteData,
		}
		//chContainer[deviceId] <- utils.Ch{
		//	DeviceId: deviceId,
		//	Data:     byte_data,
		//}
		//fmt.Println(deviceId)
		//fmt.Printf("data:%v addr:%v count:%v\n", string(data[:n]), addr, n)
		//_, err = listen.WriteToUDP(data[:n], addr) // 发送数据
		//if err != nil {
		//	fmt.Println("write to udp failed, err:", err)
		//	continue
		//}
	}
}
