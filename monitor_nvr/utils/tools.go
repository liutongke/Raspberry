package utils

import (
	"bytes"
	"fmt"
	"image/jpeg"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
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

// 获取11位unix时间戳
func GetTime() int64 {
	// 获取当前时间
	currentTime := time.Now()

	// 获取11位的Unix时间戳（秒级）
	unixTimestamp := currentTime.Unix()

	//fmt.Println(unixTimestamp)
	return unixTimestamp
	//return strconv.FormatInt(unixTimestamp, 10)
}

// CheckJPEGValidity 检测 JPEG 二进制流的正确性
func CheckJPEGValidity(data []byte) bool {
	_, err := jpeg.DecodeConfig(bytes.NewReader(data))
	if err != nil {
		log.Println("Invalid JPEG format:", err)
		return false
	}
	return true
}

// 将文件夹下的图片自然排序
func GetSort(imageFolder string) ([]string, error) {
	//imageFolder := "images" // 图片所在的文件夹路径

	imageNames, err := getImageNamesInFolder(imageFolder)
	if err != nil {
		fmt.Println("无法获取图片名称列表:", err)
		return nil, err
	}

	sort.SliceStable(imageNames, func(i, j int) bool {
		return naturalLess(imageNames[i], imageNames[j])
	})

	fmt.Println("排序后的图片名称列表:")
	//for _, name := range imageNames {
	//	fmt.Println(name)
	//}
	return imageNames, nil
}

// 获取目录下所有图片文件的名称
func getImageNamesInFolder(folderPath string) ([]string, error) {
	var imageNames []string

	err := filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() && IsImageFile(path) {
			imageNames = append(imageNames, info.Name())
		}

		return nil
	})

	if err != nil {
		return nil, err
	}

	return imageNames, nil
}

// 判断文件是否为图片文件
func isImageFile(filePath string) bool {
	extension := filepath.Ext(filePath)
	return extension == ".jpg" || extension == ".jpeg" || extension == ".png" || extension == ".gif" || extension == ".bmp"
}

// 自然排序比较函数
func naturalLess(s1, s2 string) bool {
	parts1 := strings.Split(s1, ".")
	parts2 := strings.Split(s2, ".")

	for i := 0; i < len(parts1) && i < len(parts2); i++ {
		num1, err1 := strconv.Atoi(parts1[i])
		num2, err2 := strconv.Atoi(parts2[i])

		// 如果无法转换为数字，则按字符串比较
		if err1 != nil || err2 != nil {
			if parts1[i] != parts2[i] {
				return parts1[i] < parts2[i]
			}
		} else {
			if num1 != num2 {
				return num1 < num2
			}
		}
	}

	// 如果前缀部分完全相同，长度较短的字符串更小
	return len(parts1) < len(parts2)
}
