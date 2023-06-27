package utils

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"runtime"
	"strconv"
)

func GetServerStatus(context *gin.Context) {
	context.JSON(http.StatusOK, gin.H{
		"Server status": runtimes(),
	})
}

func runtimes() map[string]string {
	data := make(map[string]string)

	numGoroutines := runtime.NumGoroutine()
	data["当前运行的goroutine数量:"] = strconv.Itoa(numGoroutines)

	var memStats runtime.MemStats

	// 获取当前内存统计信息
	runtime.ReadMemStats(&memStats)

	totalAlloc := BytesToMegabytes(float64(memStats.TotalAlloc))
	heapAlloc := BytesToMegabytes(float64(memStats.HeapAlloc))
	heapSys := BytesToMegabytes(float64(memStats.HeapSys))

	data["总分配的内存:"] = fmt.Sprintf("%.2fMB", totalAlloc)
	data["堆内存占用:"] = fmt.Sprintf("%.2fMB", heapAlloc)
	data["堆内存系统保留量:"] = fmt.Sprintf("%.2fMB", heapSys)
	data["堆对象数量:"] = strconv.FormatUint(memStats.HeapObjects, 10)

	data["返回Go根目录的路径:"] = runtime.GOROOT()
	data["返回当前系统可用的CPU核心数:"] = strconv.Itoa(runtime.NumCPU())

	return data
}

// BytesToMegabytes 字节转MB
func BytesToMegabytes(bytes float64) float64 {
	megabytes := bytes / (1024 * 1024)
	return megabytes
}

// BytesToGigabytes 字节转GB
func BytesToGigabytes(bytes float64) float64 {
	gigabytes := bytes / (1024 * 1024 * 1024)
	return gigabytes
}
