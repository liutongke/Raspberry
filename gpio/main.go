package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/rand"
	"net"
	"os"
	"os/exec"
	"strconv"
	"time"
)

func get_rand_num() string {
	// 设置随机种子，一般使用当前时间的纳秒数
	rand.Seed(time.Now().UnixNano())

	// 生成一个0到100之间的随机整数
	randomNumber := rand.Intn(101)
	//fmt.Println("Random number:", randomNumber)
	return strconv.Itoa(randomNumber)
}

func save_pic(byte_data []byte) {
	err := ioutil.WriteFile("images/"+get_rand_num()+".jpg", byte_data, 0644)
	if err != nil {
		fmt.Println("Failed to save image:", err)
		os.Exit(1)
	}
}
func decode_payload(byte_data []byte) (string, []byte) {
	// 将字节流转换为int32
	value := int32(binary.BigEndian.Uint32(byte_data[:4]))
	//fmt.Println(value) // 输出: 1
	device_id := string(byte_data[4 : 4+value])
	//fmt.Println(str)

	//err := ioutil.WriteFile("images/"+get_rand_num()+".jpg", byte_data[4+value:], 0644)
	//if err != nil {
	//	fmt.Println("Failed to save image:", err)
	//	os.Exit(1)
	//}
	//
	//fmt.Println("Image saved successfully.")
	return device_id, byte_data[4+value:]
}

// UDP server端
func main() {
	ch := make(chan []byte)
	go ffmpeg(ch)
	listen, err := net.ListenUDP("udp", &net.UDPAddr{
		IP:   net.IPv4(0, 0, 0, 0),
		Port: 9090,
	})
	if err != nil {
		fmt.Println("listen failed, err:", err)
		return
	}
	defer listen.Close()
	for {
		var data [100000]byte
		n, _, err := listen.ReadFromUDP(data[:]) // 接收数据
		if err != nil {
			fmt.Println("read udp failed, err:", err)
			continue
		}
		img := data[:n]
		_, img = decode_payload(img)
		ch <- img
		//fmt.Printf("data:%v addr:%v count:%v\n", string(data[:n]), addr, n)
		//_, err = listen.WriteToUDP(data[:n], addr) // 发送数据
		//if err != nil {
		//	fmt.Println("write to udp failed, err:", err)
		//	continue
		//}
	}
}

func ffmpeg(ch chan []byte) {
	ffmpegCmd := exec.Command("ffmpeg",
		"-y",
		"-re",
		"-f", "rawvideo",
		"-vcodec", "rawvideo",
		"-pix_fmt", "bgr24",
		"-s", "800x600", // 设置视频宽高，这里假设宽高为640x480
		"-r", "6", // 设置帧率，这里假设为6帧/秒
		"-i", "-",
		"-c:v", "libx264",
		"-b:v", "2M",
		"-g", "5",
		"-bf", "0",
		"-pix_fmt", "yuv420p",
		"-preset", "ultrafast",
		"-f", "flv",
		"rtmp://192.168.1.107:1935/live/go1") // 替换为实际的RTMP服务器地址

	inputPipe, err := ffmpegCmd.StdinPipe()
	if err != nil {
		log.Fatal(err)
	}

	err = ffmpegCmd.Start()
	if err != nil {
		log.Fatal(err)
	}

	for {
		v, ok := <-ch
		if !ok {
			fmt.Println("通道已关闭")
			break
		}
		fmt.Println(get_rand_num())
		_, err = io.Copy(inputPipe, bytes.NewReader(v))
		save_pic(v)
		if err != nil {
			fmt.Print(err)
		}
	}
	//_, err = io.Copy(inputPipe, imageFile)
	//if err != nil {
	//	return err
	//}
	//imageFolder := "/" // 图片文件夹路径
	//imageFiles := []string{
	//	"image1.jpg",
	//	"image2.jpg",
	//	"image3.jpg",
	//	// 添加更多的图片文件
	//}

	//for _, imageFile := range imageFiles {
	//	imagePath := imageFolder + "/" + imageFile
	//	err = pushImage(inputPipe, imagePath)
	//	if err != nil {
	//		log.Fatal(err)
	//	}
	//}

	err = inputPipe.Close()
	if err != nil {
		log.Fatal(err)
	}

	err = ffmpegCmd.Wait()
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Streaming completed.")
}

//func pushImage(inputPipe *io.WriteCloser, imagePath string) error {
//	imageFile, err := os.Open(imagePath)
//	if err != nil {
//		return err
//	}
//	defer imageFile.Close()
//
//	_, err = io.Copy(inputPipe, imageFile)
//	if err != nil {
//		return err
//	}
//
//	return nil
//}
