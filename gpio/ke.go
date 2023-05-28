package main

import (
	"fmt"
	"os"
)

func main() {

	file, err := os.Open("1.jpg")
	if err != nil {
		fmt.Println("Error opening image file:", err)

	}
	fmt.Println(file)
}
