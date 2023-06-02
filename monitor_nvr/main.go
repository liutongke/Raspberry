package main

import (
	"monitor/nvr/utils"
)

func main() {
	go utils.StartUdp() // UDP server端
	utils.Http()        //http
}
