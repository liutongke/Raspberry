package service

import (
	"io/ioutil"
	"log"
	"monitor/nvr/config"
	"monitor/nvr/utils"
	"os"
	"path/filepath"
	"strings"

	"github.com/icza/mjpeg"
)

// PicToVideo 图片转为视频
// imageFolder 替换为你的图片文件夹路径
// outputFile 替换为输出视频文件的路径和名称
func PicToVideo(imageFolder, outputFile string, camInfo config.Cam) {

	imageFiles, err := utils.GetSort(imageFolder)
	if err != nil {
		return
	}

	// 创建MJPEG编码器
	encoder, _ := mjpeg.New(outputFile, int32(camInfo.Width), int32(camInfo.Height), int32(camInfo.Fps))

	// 逐个读取图像文件并添加到编码器
	for _, imagePath := range imageFiles {
		img, err := os.Open(imageFolder + "/" + imagePath)
		if err != nil {
			return
		}
		fileBytes, err := ioutil.ReadAll(img)
		if err != nil {
			log.Printf("无法读取文件内容：%v\n", err)
			return
		}
		// 将图像添加到编码器中
		err = encoder.AddFrame(fileBytes)
		if err != nil {
			log.Printf("Error adding frame to encoder: %v\n", err)
		}
	}
	err = encoder.Close()
	if err != nil {
		log.Printf("encoder close err: %v", err)
	}

	log.Printf("Video file created path:%s", outputFile)
}

// 列出文件夹中的图像文件
func ListFolderImageFiles(folderPath string) (imageFiles []string, err error) {

	err = filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// 检查文件是否为图像文件（支持的格式：JPEG、PNG、BMP、GIF）
		ext := strings.ToLower(filepath.Ext(path))
		if ext == ".jpg" || ext == ".jpeg" || ext == ".png" || ext == ".bmp" || ext == ".gif" {
			imageFiles = append(imageFiles, path)
		}

		return nil
	})
	return
}
