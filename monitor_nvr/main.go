package main

import (
	"fmt"
	"monitor/nvr/utils"
)

func main() {
	utils.EchoSuccess(fmt.Sprintf("start http port:%d start udp port:%d", utils.ServerPort(), utils.UdpPort()))

	if utils.IsRaspi() {
		utils.StartRaspiCam()
	}
	utils.StartUdp() // UDP server端
	//utils.Http()     //http
}
