package utils

import (
	"log"
)

func EchoSuccess(str string) {
	log.Printf("\033[1;32;40m%s\033[0m\n", str)
}

func EchoError(str string) {
	log.Printf("\033[1;31;40m%s\033[0m\n", str)
}
func EchoErrorExit(str string) {
	log.Fatalf("\033[1;31;40m%s\033[0m\n", str)
}
