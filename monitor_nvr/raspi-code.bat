SET CGO_ENABLED=0
SET GOOS=linux
SET GOARCH=arm64
SET GOARM=7
go build -o monitor mjpg-streamer.go
set GOOS=windows
set GOARCH=amd64
