package libcamera_demos

import (
	"log"
	"os"
	"os/exec"
)

func main() {
	// 创建libcamera-vid的命令对象，并设置相关参数
	cmd := exec.Command("libcamera-vid", "-t", "10000", "--codec", "mjpeg", "--segment", "1", "-o", "-")

	// 创建输出文件
	file, err := os.Create("output.mjpeg")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// 将libcamera-vid命令的输出管道连接到文件
	cmd.Stdout = file

	// 启动libcamera-vid命令
	if err := cmd.Start(); err != nil {
		log.Fatal(err)
	}

	// 等待libcamera-vid命令完成并释放资源
	err = cmd.Wait()
	if err != nil {
		log.Fatal(err)
	}

	log.Println("视频流已保存到 output.mjpeg 文件")
}
