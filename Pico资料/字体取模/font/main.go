package main

import (
	"encoding/hex"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"regexp"
	"strings"
)

func utf8To16(word string) string {
	return "0x" + hex.EncodeToString([]byte(word))
}

func main() {
	list := word()
	ziti := WordCode()

	str := ""
	for key, word := range list {
		str += utf8To16(word) + ":" + ziti[key] + ",#" + word + "\r\n"
	}
	WriteFile("font.txt", str)
}

func word() map[int]string {
	s := ReadFile("./word.txt")

	pattern := "\\d+"
	re := regexp.MustCompile(pattern)
	s = re.ReplaceAllString(s, "")

	res := strings.Split(s, "()")

	i := 0
	list := make(map[int]string)

	for _, val := range res {
		str := strings.ReplaceAll(val, " ", "")
		p := "[\\p{Han}]+"
		r := regexp.MustCompile(p)
		match := r.FindAllString(str, -1)

		if len(match) > 0 && len(str) > 0 {
			list[i] = str
			i++
		}
	}
	return list
}

func WordCode() map[int]string {
	s := ReadFile("./word_code.txt")
	//去除所有空格和换行
	pattern := "[\\s]+"
	re := regexp.MustCompile(pattern)
	s = re.ReplaceAllString(s, "")

	//去除中文
	pattern = "[\u4e00-\u9fa5]+"
	re = regexp.MustCompile(pattern)
	s = re.ReplaceAllString(s, "")

	//正则去除,2*这种格式
	pattern = ",\\d*\\*\\/\\s*"
	re = regexp.MustCompile(pattern)
	s = re.ReplaceAllString(s, "")

	ziti := make(map[int]string)

	strArr := strings.Split(s, ",/*\"\"")
	for k, v := range strArr {
		if len(v) > 10 {
			s1 := strings.Replace(v, "},{", ",", -1)
			s1 = strings.Replace(s1, "{", "[", -1)
			s1 = strings.Replace(s1, "}", "]", -1)
			ziti[k] = s1
		}
	}
	return ziti
}

func WriteFile(fileName, strTest string) {

	var f *os.File
	var err error

	if CheckFileExist(fileName) { //文件存在
		f, err = os.OpenFile(fileName, os.O_APPEND, 0666) //打开文件
		if err != nil {
			fmt.Println("file open fail", err)
			return
		}
	} else { //文件不存在
		f, err = os.Create(fileName) //创建文件
		if err != nil {
			fmt.Println("file create fail")
			return
		}
	}
	//将文件写进去
	n, err1 := io.WriteString(f, strTest)
	if err1 != nil {
		fmt.Println("write error", err1)
		return
	}
	fmt.Println("写入的字节数是：", n)
}

func ReadFile(filePath string) string {
	f, err := os.Open(filePath)
	if err != nil {
		fmt.Println("read file fail", err)
		return ""
	}
	defer func(f *os.File) {
		err := f.Close()
		if err != nil {

		}
	}(f)

	fd, err := ioutil.ReadAll(f)
	if err != nil {
		fmt.Println("read to fd fail", err)
		return ""
	}

	return string(fd)
}

func CheckFileExist(fileName string) bool {
	_, err := os.Stat(fileName)
	if os.IsNotExist(err) {
		return false
	}
	return true
}
