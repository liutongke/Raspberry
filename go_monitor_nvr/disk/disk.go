package disk

import (
	"fmt"
	"os/exec"
	"strings"
)

type DiskInfo struct {
	Filesystem     string
	TotalSpace     string
	UsedSpace      string
	AvailableSpace string
	Use            string
	MountPoint     string
}

// GetSpecifyPathDiskInfo 获取指定路径磁盘信息
func GetSpecifyPathDiskInfo(directory string) (disk *DiskInfo) {
	// 指定目录路径
	//directory := "/var/www/html"

	// 执行 df 命令获取目录的磁盘信息
	out, err := exec.Command("df", "-h", directory).Output()
	if err != nil {
		fmt.Println("执行 df 命令时出错:", err)
		return
	}

	// 解析输出并提取磁盘空间信息
	lines := strings.Split(string(out), "\n")
	if len(lines) >= 2 {
		fields := strings.Fields(lines[1])
		if len(fields) >= 6 {
			disk = &DiskInfo{
				Filesystem:     fields[0],
				TotalSpace:     fields[1],
				UsedSpace:      fields[2],
				AvailableSpace: fields[3],
				Use:            fields[4],
				MountPoint:     fields[5],
			}
			//fmt.Println(disk)
			//mountPoint := fields[5]
			//totalSpace := fields[1]
			//usedSpace := fields[2]
			//availableSpace := fields[3]
			//[drvfs 931G 174G 758G 19% /var/www/html]
			// 打印磁盘空间信息
			//fmt.Println("已使用空间:", fields[4])
			//fmt.Println("挂载点:", mountPoint)
			//fmt.Println("总空间:", totalSpace)
			//fmt.Println("已使用空间:", usedSpace)
			//fmt.Println("可用空间:", availableSpace)
			//fmt.Println("------------------------------------")
		}
	}
	return
}

// GetAllPathDiskInfo 获取所有磁盘信息
func GetAllPathDiskInfo() (disk []*DiskInfo) {
	// 执行 df 命令获取磁盘信息
	out, err := exec.Command("df", "-h").Output()
	if err != nil {
		fmt.Println("执行 df 命令时出错:", err)
		return
	}

	// 解析输出并提取磁盘空间信息
	lines := strings.Split(string(out), "\n")
	for _, line := range lines[1:] {
		fields := strings.Fields(line)
		if len(fields) >= 6 {
			disk = append(disk, &DiskInfo{
				Filesystem:     fields[0],
				TotalSpace:     fields[1],
				UsedSpace:      fields[2],
				AvailableSpace: fields[3],
				Use:            fields[4],
				MountPoint:     fields[5],
			})
			//mountPoint := fields[5]
			//totalSpace := fields[1]
			//usedSpace := fields[2]
			//availableSpace := fields[3]

			// 打印磁盘空间信息
			//fmt.Println("挂载点:", mountPoint)
			//fmt.Println("总空间:", totalSpace)
			//fmt.Println("已使用空间:", usedSpace)
			//fmt.Println("可用空间:", availableSpace)
			//fmt.Println("------------------------------------")
		}
	}
	return
}
