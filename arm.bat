SET CGO_ENABLED=0
SET GOOS=linux
SET GOARCH=arm64
SET GOARM=7
go build -o nat-x main.go
set GOOS=windows
set GOARCH=amd64
