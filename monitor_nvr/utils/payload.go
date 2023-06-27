package utils

import (
	"encoding/binary"
)

// 解码传输过来的数据流
func decodePayload(byteData []byte) (string, []byte) {
	dataLen := int32(binary.BigEndian.Uint32(byteData[:4])) // 将字节流转换为int32
	deviceId := string(byteData[4 : 4+dataLen])
	return deviceId, byteData[4+dataLen:]
}
