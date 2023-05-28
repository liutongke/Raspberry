package utils

import (
	"bytes"
	"fmt"
	"github.com/fogleman/gg"
	"image"
	"image/jpeg"
)

func MakeWaterMarker(imgPath string, waterDesc string, outPath string) bool {
	im, err := gg.LoadImage(imgPath)
	if err != nil {
		return false
	}
	w := im.Bounds().Size().X
	h := im.Bounds().Size().Y

	dc := gg.NewContext(w, h)
	rd := w / 375
	if rd == 0 {
		rd = 1
	}
	if err := dc.LoadFontFace("./fonts/Microsoft_YaHei.ttf", float64(rd*24)); err != nil {
		fmt.Print(err)
		return false
	}
	dc.DrawImage(im, 0, 0)
	//sw, sh := dc.MeasureString(waterDesc)
	dc.SetHexColor("#64FF00") // 设置画笔颜色为绿色
	dc.Push()
	dc.DrawString(waterDesc, float64(100), float64(100))
	dc.Pop()
	dc.SavePNG(outPath)
	return true
}
func MakeWaterMarkerTobyte(pic []byte, waterDesc string) ([]byte, error) {

	im, _, err := image.Decode(bytes.NewReader(pic))
	if err != nil {
		return nil, err
	}
	w := im.Bounds().Size().X
	h := im.Bounds().Size().Y

	dc := gg.NewContext(w, h)
	rd := w / 375
	if rd == 0 {
		rd = 1
	}
	//rd字体大小
	if err := dc.LoadFontFace("./fonts/Microsoft_YaHei.ttf", float64(rd*12)); err != nil {
		fmt.Print(err)
		return nil, err
	}
	dc.DrawImage(im, 0, 0)
	dc.SetHexColor("#64FF00") // 设置画笔颜色为绿色
	dc.Push()
	dc.DrawString(waterDesc, float64(550), float64(580)) //水印显示位置
	dc.Pop()

	// 创建一个缓冲区来保存图像字节流
	buf := new(bytes.Buffer)
	// 将图像编码为PNG格式，并将结果写入缓冲区
	err = jpeg.Encode(buf, dc.Image(), nil)
	if err != nil {
		return nil, err
	}

	// 从缓冲区中获取字节流
	imgBytes := buf.Bytes()
	return imgBytes, nil
	//return bytes.NewReader(imgBytes), nil
}
