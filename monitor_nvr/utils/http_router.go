package utils

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func Http() {
	var router *gin.Engine

	if IsDebug() { //开发模式
		router = gin.Default()
	} else { //生产模式
		gin.SetMode(gin.ReleaseMode)
		router = gin.New()
	}

	// 将 "/html" 路由映射到 "template" 目录下的静态文件
	router.StaticFS("/html", http.Dir("template")) //监控播放地址
	router.GET("/favicon.ico", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"msg": "success",
			"err": 200,
		})
	})
	router.POST("/get/video/url", func(c *gin.Context) {
		camList := CamParam()

		var _dict []map[string]string

		for deviceId, camInfo := range camList {
			_dict = append(_dict, map[string]string{
				"deviceId":    deviceId,
				"VideoFlvUrl": camInfo.VideoFlvUrl,
				"video":       camInfo.Video,
			})
		}

		c.JSON(http.StatusOK, gin.H{
			"msg":  "success",
			"err":  200,
			"data": _dict,
		})
	})
	router.Run(":12349")
}
