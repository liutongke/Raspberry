package main

import (
	"fmt"

	"github.com/fogleman/gg"
)

func main() {
	fileName := GetDirFileName("images")
	for _, name := range fileName {
		MakeWaterMarker("images/"+name, GetNowStr(), "test/"+name)
	}

}
func MakeWaterMarker(imgPath string, waterDesc string, outPath string) bool {
	im, err := gg.LoadImage(imgPath)
	if err != nil {
		return false
	}
	w := im.Bounds().Size().X
	h := im.Bounds().Size().Y
	fmt.Print(w, h)
	dc := gg.NewContext(w, h)
	rd := w / 375
	if rd == 0 {
		rd = 1
	}
	if err := dc.LoadFontFace("./fonts/miscfs_.ttf", float64(rd*24)); err != nil {
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
