package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func GetDirFileName(directory string) []string {
	//directory := "images" // 替换为你要遍历的目录路径
	var fileList []string

	err := filepath.Walk(directory, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() && isImageFiles(path) {
			fileList = append(fileList, info.Name())
		}

		return nil
	})

	if err != nil {
		fmt.Println("遍历目录时发生错误:", err)
		return nil
	}

	var fileName []string
	for _, file := range fileList {
		//fmt.Println(file)
		fileName = append(fileName, file)
	}
	return fileName
}

// 检查文件是否为图片文件
func isImageFiles(filename string) bool {
	ext := strings.ToLower(filepath.Ext(filename))
	return ext == ".jpg" || ext == ".jpeg" || ext == ".png" || ext == ".gif" || ext == ".bmp"
}
