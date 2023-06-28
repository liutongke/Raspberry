package main

import (
	"fmt"
	"monitor/nvr/config"
	"monitor/nvr/router"
	"monitor/nvr/utils"
)

func init() {
	for deviceId, _ := range config.CamParam() {
		utils.MkDirAll(fmt.Sprintf("%s%s", config.ImagePath(), deviceId))
		utils.MkDirAll(fmt.Sprintf("%s%s", config.VideoPath(), deviceId))
	}
}
func main() {
	utils.EchoSuccess(fmt.Sprintf("listen http port:%d listen udp port:%d", config.ServerPort(), config.UdpPort()))

	router.StartUdp() // UDP server端
	//utils.Http()     //http
}
