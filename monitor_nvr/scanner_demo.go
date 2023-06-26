package main

import (
	"bufio"
	"bytes"
	"fmt"
	"strings"
)

var (
	nalSeparator = []byte{0xFF, 0xD8} // 分隔符：0xFFD8
)

func main() {
	data := "data1\xFF\xD8data2\xFF\xD8data3\xFF\xD9data4\xFF\xD8data5"

	// 创建一个包含示例数据的字符串读取器
	reader := strings.NewReader(data)

	// 创建一个扫描器，并设置分割函数
	scanner := bufio.NewScanner(reader)
	scanner.Split(scanNalSeparator)

	// 逐个读取分割后的数据片段
	for scanner.Scan() {
		token := scanner.Bytes()
		fmt.Printf("Token: %s\n", token)
	}

	if scanner.Err() != nil {
		fmt.Printf("Error: %s\n", scanner.Err())
	}
}

func scanNalSeparators(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}

	if i := bytes.Index(data, nalSeparator); i >= 0 {
		return i + len(nalSeparator), data[0:i], nil
	}

	if atEOF {
		return len(data), data, nil
	}

	return 0, nil, nil
}
