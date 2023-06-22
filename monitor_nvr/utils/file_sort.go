package utils

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"time"
)

type FileInfo struct {
	Path        string
	Size        int64
	CreatedTime time.Time
}

type ByCreatedTime []FileInfo

func (b ByCreatedTime) Len() int           { return len(b) }
func (b ByCreatedTime) Less(i, j int) bool { return b[i].CreatedTime.Before(b[j].CreatedTime) }
func (b ByCreatedTime) Swap(i, j int)      { b[i], b[j] = b[j], b[i] }

// 将文件按照生成时间按照从小到大排序
func GetFileInfos(root string) []FileInfo {
	//root := "./video" // 指定要扫描的文件夹路径
	fileInfos := make([]FileInfo, 0)

	err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			fmt.Println("访问路径时出错:", err)
			return nil
		}
		if !info.IsDir() {
			size := info.Size()
			createdTime := info.ModTime()

			//fmt.Printf("文件：%s\n", path)
			//fmt.Printf("大小：%d bytes\n", size)
			//fmt.Printf("创建时间：%s\n", createdTime)
			//fmt.Println("-----------------------------------")

			fileInfos = append(fileInfos, FileInfo{Path: path, Size: size, CreatedTime: createdTime})
		}
		return nil
	})

	if err != nil {
		fmt.Println("扫描文件夹时出错:", err)
		return nil
	}

	sort.Sort(ByCreatedTime(fileInfos))
	fmt.Println(fileInfos)
	return fileInfos
}
