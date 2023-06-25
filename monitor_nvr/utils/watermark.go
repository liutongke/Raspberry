package utils

import (
	"bytes"
	"github.com/fogleman/gg"
	"image"
	"image/jpeg"
)

// FileAddMakeWater 读取给定路径文件添加水印后重新保存
func FileAddMakeWater(imgPath string, waterDesc string, outPath string) bool {
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
	if err = dc.LoadFontFace(GetAbsDirPath("./fonts/Microsoft_YaHei.ttf"), float64(rd*24)); err != nil {
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

// AddWatermarkPic 给图片添加水印
func AddWatermarkPic(pic []byte, waterDesc string) ([]byte, error) {

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
	if err = dc.LoadFontFace(GetAbsDirPath("./fonts/Microsoft_YaHei.ttf"), float64(rd*12)); err != nil {
		return nil, err
	}
	dc.DrawImage(im, 0, 0)
	dc.SetHexColor("#64FF00") // 设置画笔颜色为绿色
	dc.Push()
	//dc.DrawString(waterDesc, float64(550), float64(580)) //水印显示位置
	dc.DrawString(waterDesc, float64(550), float64(70)) //水印显示位置
	dc.Pop()

	buf := new(bytes.Buffer)                // 创建一个缓冲区来保存图像字节流
	err = jpeg.Encode(buf, dc.Image(), nil) // 将图像编码为PNG格式，并将结果写入缓冲区
	if err != nil {
		return nil, err
	}

	// 从缓冲区中获取字节流
	return buf.Bytes(), nil
}
