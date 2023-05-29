@echo off
set container_name=php1

docker ps -a --format "{{.Names}}" | findstr /i "%container_name%" > nul
if %errorlevel% equ 0 (
    echo Container %container_name% exists.
) else (
    echo Container %container_name% does not exist.
)
