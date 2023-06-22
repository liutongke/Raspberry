package utils

import "encoding/binary"

// 解码传输过来的数据流
func decodePayload(byte_data []byte) (string, []byte) {
	dataLen := int32(binary.BigEndian.Uint32(byte_data[:4])) // 将字节流转换为int32
	device_id := string(byte_data[4 : 4+dataLen])
	return device_id, byte_data[4+dataLen:]
}
