package test

import (
	"fmt"
	"monitor/nvr/config"
	"monitor/nvr/utils"
	"testing"
)

func TestKeepVideo(t *testing.T) {
	agoTm := utils.GetAgoHourId(config.KeepVideoTm())
	fmt.Println("KeepVideoTm:", agoTm)
	//dir := "C:\\Users\\keke\\dev\\Raspberry-Pi\\monitor_nvr\\data\\images\\a0b765593494"
	//fmt.Println(dir)
	//utils.GetDirPathName(dir)
	//utils.KeepVideo()
}
