package main

import (
	"log"
	"monitor/nvr/utils"
)

func main() {
	log.Printf("start udp port:%d start http port:%d", 9090, 9091)
	utils.StartUdp() // UDP server端
	//utils.Http()     //http
}
