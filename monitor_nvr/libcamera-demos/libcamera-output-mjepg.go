package libcamera_demos

import (
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
)

func main() {
	cmd := exec.Command("libcamera-vid", "-t", "0", "--codec", "mjpeg", "-o", "-", "-n")

	stdoutPipe, err := cmd.StdoutPipe()
	if err != nil {
		log.Fatal(err)
	}
	defer stdoutPipe.Close()

	err = cmd.Start()
	if err != nil {
		log.Fatal(err)
	}

	file, err := os.Create("output.mjpeg")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	_, err = io.Copy(file, stdoutPipe)
	if err != nil {
		log.Fatal(err)
	}

	err = cmd.Wait()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Video saved successfully.")
}
