package test

import (
	"fmt"
	"monitor/nvr/disk"
	"testing"
)

func TestDisk(t *testing.T) {
	fmt.Println(disk.GetSpecifyPathDiskInfo("/var/www/html"))
	fmt.Println(disk.GetAllPathDiskInfo())
}
