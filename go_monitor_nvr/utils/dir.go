package utils

import (
	"fmt"
	"os"
	"path/filepath"
)

// GetAVIFiles 获取指定路径下的avi文件
func GetAVIFiles(dirPath string) ([]string, error) {
	var aviFiles []string

	err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() && filepath.Ext(path) == ".avi" {
			aviFiles = append(aviFiles, path)
		}

		return nil
	})

	if err != nil {
		return nil, err
	}

	return aviFiles, nil
}

// GetDirPathName 获取指定路径下的所有目录
func GetDirPathName(dirPath string) ([]string, error) {
	// 打开目录
	dir, err := os.Open(dirPath)
	if err != nil {
		fmt.Println("无法打开目录:", err)
		return nil, err
	}
	defer dir.Close()

	// 读取目录内容
	fileInfos, err := dir.Readdir(-1)
	if err != nil {
		fmt.Println("无法读取目录内容:", err)
		return nil, err
	}

	// 过滤出目录
	var directories []string
	for _, fileInfo := range fileInfos {
		if fileInfo.IsDir() {
			directories = append(directories, fileInfo.Name())
		}
	}
	return directories, err
}

// GetAbsDirPath 根据当前的工作目录来解析相对路径，可以使用../test
func GetAbsDirPath(filePath string) string {
	absPath, err := filepath.Abs(filePath)
	if err != nil {
		return ""
	}
	return absPath
}

// DelDir 删除目录
func DelDir(dirPath string) bool {
	err := os.RemoveAll(dirPath)
	return err == nil
}

// MkDirAll 父目录不存在一同创建
func MkDirAll(dirPath string) bool {
	err := os.MkdirAll(dirPath, os.ModePerm)
	return err == nil
}

// IsExist 判断目录是否存在
func IsExist(dirPath string) bool {
	// 检查目录是否存在
	_, err := os.Stat(dirPath)
	if err != nil {
		if os.IsNotExist(err) {
			return false
		} else {
			return false
		}
	}
	return true
}
