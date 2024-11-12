import powerSW2 as sw

import WindowsClient
import JavaClient

import ASCIIART
import DediProg_CMD

# 初始化自動安裝器，可以選擇 Windows 或 Java 版本
installer = WindowsClient.AutoInstaller()
# installer = JavaClient.AutoInstaller() # 使用 Java 安裝器

# 設置設備控制器，並提供設備的控制端點 URL
controller = sw.DeviceController("http://192.168.0.211:16628")

# 初始化 ASCII Art 和 Programmer 類
ascii_art = ASCIIART.ASCIIArtBuilder() # 一定要匯入，否則DP會出錯
directory = r"C:\Program Files (x86)\DediProg\SF100"
bios_filename = "IceLake_U_3.bin" # BIOS 檔案名稱
programmer = DediProg_CMD.Programmer(directory, bios_filename, ascii_art)


#執行電源和 BIOS 燒錄程序的完整流程
controller.ACoffcheck()
controller.dp_on()               # 打開 DP
programmer.run()                 # 執行 BIOS 燒錄
controller.dp_off()              # 關閉 DP
controller.cmos_switch()         # 重置 CMOS
controller.AConcheck()           # 打開 AC 並檢查狀態
installer.start_installation()   # 開始安裝操作系統