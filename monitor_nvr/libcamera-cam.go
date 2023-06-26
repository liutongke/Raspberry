package main

import (
	"fmt"
	"os/exec"
)

func main() {
	cmd := exec.Command("libcamera-jpeg", "-o", "test-go.jpg")

	if err := cmd.Run(); err != nil {
		fmt.Println("Command execution failed:", err)
		return
	}

	fmt.Println("Command execution completed")
}
