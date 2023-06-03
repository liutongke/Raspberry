package main

import (
	"embed"
	"io"
	"log"
	"os"
)

//go:embed database.toml
var configData embed.FS

func main() {
	// 创建一个临时文件来保存配置数据
	file, err := configData.Open("database.toml")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// 将 embed 文件内容复制到目标文件
	destFile, err := os.Create("config/database.toml")
	if err != nil {
		log.Fatal(err)
	}
	defer destFile.Close()

	_, err = io.Copy(destFile, file)
	if err != nil {
		log.Fatal(err)
	}
}
