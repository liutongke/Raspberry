package main

import (
	"fmt"
	"io/ioutil"
	"monitor/nvr/utils"
	"os"
	"path/filepath"
	"strings"

	"github.com/icza/mjpeg"
)

func main() {
	imageFolder := "2023052907" // 替换为你的图片文件夹路径
	outputFile := "output.avi"  // 替换为输出视频文件的路径和名称

	imageFiles, err := utils.GetSort(imageFolder)
	if err != nil {
		return
	}
	fmt.Println(len(imageFiles) / 3600)
	// 创建MJPEG编码器
	encoder, _ := mjpeg.New(outputFile, 800, 600, 5)

	// 逐个读取图像文件并添加到编码器
	for _, imagePath := range imageFiles {
		img, err := os.Open(imageFolder + "/" + imagePath)
		if err != nil {
			return
		}
		fileBytes, err := ioutil.ReadAll(img)
		if err != nil {
			fmt.Printf("无法读取文件内容：%v\n", err)
			return
		}
		// 将图像添加到编码器中
		err = encoder.AddFrame(fileBytes)
		if err != nil {
			fmt.Printf("Error adding frame to encoder: %v\n", err)
		}
	}
	encoder.Close()

	fmt.Println("Video file created:", outputFile)
}

// 列出文件夹中的图像文件
func listImageFiles(folderPath string) ([]string, error) {
	var imageFiles []string

	err := filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
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

	if err != nil {
		return nil, err
	}

	return imageFiles, nil
}

// 加载图像文件
//func loadImage(filePath string) (image.Image, error) {
//	file, err := os.Open(filePath)
//	if err != nil {
//		return nil, err
//	}
//	defer file.Close()
//
//	img, _, err := image.Decode(file)
//	if err != nil {
//		return nil, err
//	}
//
//	return img, nil
//}

// 调整图像大小
//func resizeImage(img image.Image, width, height int) image.Image {
//	resizedImg := image.NewRGBA(image.Rect(0, 0, width, height))
//	draw.Draw(resizedImg, resizedImg.Bounds(), img, img.Bounds().Min, draw.Src)
//	return resizedImg
//}

// 在图像上添加文本
//func addTextToImage(img draw.Image, text string, x, y int, textColor color.Color) {
//	draw.Draw(img, img.Bounds(), &image.Uniform{textColor}, image.ZP, draw.Src)
//
//	c := freetype.NewContext()
//	c.SetDPI(72)
//	c.SetFont(font)
//	c.SetFontSize(fontSize)
//	c.SetClip(img.Bounds())
//	c.SetDst(img)
//	c.SetSrc(image.White)
//
//	pt := freetype.Pt(x, y+int(c.PointToFixed(fontSize)>>6))
//	_, err := c.DrawString(text, pt)
//	if err != nil {
//		fmt.Printf("Error adding text to image: %v\n", err)
//	}
//}
