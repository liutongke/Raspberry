package main

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"path/filepath"
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

// GetRandNum 获取随机数
func GetRandNum() string {
	// 设置随机种子，一般使用当前时间的纳秒数
	rand.Seed(time.Now().UnixNano())

	// 生成一个0到100之间的随机整数
	randomNumber := rand.Intn(101)
	//fmt.Println("Random number:", randomNumber)
	return strconv.Itoa(randomNumber)
}

// SaveImages 保存照片
func SaveImages(filePath string, byteData []byte) {
	err := ioutil.WriteFile(filePath, byteData, 0644)
	if err != nil {
		fmt.Println("Failed to save image:", err)
		os.Exit(1)
	}
}

// 检查文件是否为图片文件
func IsImageFile(filePath string) bool {
	extension := filepath.Ext(filePath)
	switch extension {
	case ".jpg", ".jpeg", ".png", ".gif":
		return true
	}
	return false
}

// 获取指定文件夹下的图片文件列表
func GetImageFiles(folderPath string) ([]string, error) {
	var imageFiles []string

	// 遍历文件夹中的文件
	err := filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
		// 如果是文件且是图片文件，则将其添加到列表中
		if !info.IsDir() && IsImageFile(path) {
			imageFiles = append(imageFiles, path)
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	return imageFiles, nil
}
