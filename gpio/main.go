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
	ch := make(chan utils.Ch, 1000)
	go utils.RtmpSteamPush(ch)

	listen, err := net.ListenUDP("udp", &net.UDPAddr{
		IP:   net.IPv4(0, 0, 0, 0),
		Port: 9090,
	})
	if err != nil {
		fmt.Println("listen failed, err:", err)
		return
	}
	defer listen.Close()
	for {
		var data [65535]byte
		n, _, err := listen.ReadFromUDP(data[:]) // 接收数据
		if err != nil {
			fmt.Println("read udp failed, err:", err)
			continue
		}

		deviceId, byte_data := decodePayload(data[:n])
		ch <- utils.Ch{
			DeviceId: deviceId,
			Data:     byte_data,
		}
		//fmt.Println(deviceId)
		//fmt.Printf("data:%v addr:%v count:%v\n", string(data[:n]), addr, n)
		//_, err = listen.WriteToUDP(data[:n], addr) // 发送数据
		//if err != nil {
		//	fmt.Println("write to udp failed, err:", err)
		//	continue
		//}
	}
}
