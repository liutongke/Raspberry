@echo off
setlocal

rem 获取批处理文件所在目录的完整路径
set "script_dir=%~dp0"

rem 输出批处理文件所在目录的完整路径
echo 批处理文件所在目录：%script_dir%

endlocal
