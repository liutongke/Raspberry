package main

import (
	"monitor/nvr/utils"
)

func main() {
	utils.StartUdp() // UDP server端
	//utils.Http()     //http
}
