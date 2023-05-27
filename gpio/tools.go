package main

import (
	"math/rand"
	"strconv"
	"time"
)

// GetNowStr 获取时间戳
func GetNowStr() string {
	currentTime := time.Now()
	formattedTime := currentTime.Format("2006-01-02 15:04:05")
	//fmt.Println(formattedTime)
	return formattedTime
}
func GetRandNum() string {
	// 设置随机种子，一般使用当前时间的纳秒数
	rand.Seed(time.Now().UnixNano())

	// 生成一个0到100之间的随机整数
	randomNumber := rand.Intn(101)
	//fmt.Println("Random number:", randomNumber)
	return strconv.Itoa(randomNumber)
}
