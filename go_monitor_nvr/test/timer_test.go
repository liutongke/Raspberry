package test

import (
	"fmt"
	"monitor/nvr/utils"
	"testing"
)

func TestTimer(t *testing.T) {
	fmt.Printf("GetNowHourId:%s\n", utils.GetNowHourId())
	fmt.Printf("GetPrevHourId:%s\n", utils.GetPrevHourId())
	fmt.Printf("GetAgoHourId:%s\n", utils.GetAgoHourId(100))
}
