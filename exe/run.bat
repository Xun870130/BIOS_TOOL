@echo off
BIOS_tool.exe 192.168.0.211 java
:WAIT
echo 按 Q 鍵退出，其他快捷鍵將被忽略...
choice /c Q /n >nul
goto :EOF