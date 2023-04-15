SET CGO_ENABLED=0
SET GOOS=linux
SET GOARCH=arm64
SET GOARM=7
go build -o tinypng main.go Tinypng.go
