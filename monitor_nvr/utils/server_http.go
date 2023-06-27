package utils

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
)

func Http(h *Hub) {
	var router *gin.Engine

	if IsDebug() { //开发模式
		router = gin.Default()
	} else { //生产模式
		gin.SetMode(gin.ReleaseMode)
		router = gin.New()
	}
	routers(router, h)

	router.Run(fmt.Sprintf(":%d", ServerPort()))
}

func routers(router *gin.Engine, h *Hub) {
	// 将 "/html" 路由映射到 "template" 目录下的静态文件
	router.StaticFS("/html", http.Dir("template")) //监控播放地址
	router.GET("/favicon.ico", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"msg": "success",
			"err": 200,
		})
	})

	router.POST("/get/video/url", GetVideoUrl)
	router.GET("status", GetServerStatus)
	router.GET("/stream/esp32", h.EspMjpgStreamer)
	if IsRaspi() {
		router.GET("/stream/raspi", SendLibcameraStream) //直接调用树莓派摄像头
	}
}

func GetVideoUrl(context *gin.Context) {
	camList := CamParam()

	var _dict []map[string]string

	for deviceId, camInfo := range camList {
		_dict = append(_dict, map[string]string{
			"deviceId":    deviceId,
			"VideoFlvUrl": camInfo.VideoFlvUrl,
			"video":       camInfo.Video,
		})
	}

	context.JSON(http.StatusOK, gin.H{
		"msg":  "success",
		"err":  200,
		"data": _dict,
	})
}
