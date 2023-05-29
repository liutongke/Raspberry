package utils

import (
	"fmt"
	"os"
)

// MkDir 创建文件夹父级不存在一同创建
func MkDir(folderPath string) bool {
	// 检查文件夹状态
	_, err := os.Stat(folderPath)
	if os.IsNotExist(err) {
		// 文件夹不存在，创建它
		err := os.MkdirAll(folderPath, os.ModePerm)
		if err != nil {
			fmt.Printf("无法创建文件夹：%v\n", err)
			return false
		}
		fmt.Println("文件夹已创建")
	} else if err != nil {
		// 其他错误发生
		fmt.Printf("无法获取文件夹状态：%v\n", err)
		return false
	} else {
		// 文件夹已存在
		fmt.Println("文件夹已存在")
		return true
	}
	return true
}

// DirIsExist 检查文件夹状态 true存在 false不存在
func DirIsExist(folderPath string) bool {
	_, err := os.Stat(folderPath)
	if os.IsNotExist(err) {
		return false
	} else if err != nil {
		return false
	}
	return true
}
