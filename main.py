import argparse
import powerSW2 as sw
import WindowsClient
import JavaClient
import ASCIIART
import DediProg_CMD

def main():
    # 設定命令列參數解析
    parser = argparse.ArgumentParser(description="自動安裝程序")
    parser.add_argument("ip", help="設備控制器 IP，例如：http://192.168.0.211:16628")
    parser.add_argument("bios_filename", help="BIOS 檔案名稱，例如：IceLake_U_3.bin")
    parser.add_argument("type", choices=["win", "java"], help="選擇安裝器類型：win 或 java")

    # 解析輸入參數
    args = parser.parse_args()
    ip = args.ip
    bios_filename = args.bios_filename
    installer_type = args.type

    # 選擇安裝器類型
    if installer_type == "win":
        installer = WindowsClient.AutoInstaller(ip=ip)
    elif installer_type == "java":
        installer = JavaClient.AutoInstaller(ip=ip)
    else:
        raise ValueError("未知的安裝器類型，請使用 'win' 或 'java'")

    # 初始化控制器、ASCII 輔助與燒錄器
    controller = sw.DeviceController(IP_adr=ip)
    ascii_art = ASCIIART.ASCIIArtBuilder()  # 一定要匯入，否則 DP 會出錯
    directory = r"C:\Program Files (x86)\DediProg\SF100"  # 修改為實際路徑
    programmer = DediProg_CMD.Programmer(directory, bios_filename, ascii_art)

    # 執行程序
    controller.ACoffcheck()
    controller.dp_on()               # 打開 DP
    programmer.run()                 # 執行 BIOS 燒錄
    controller.dp_off()              # 關閉 DP
    controller.cmos_switch()         # 重置 CMOS
    controller.AConcheck()           # 打開 AC 並檢查狀態
    installer.start_installation()   # 開始安裝操作系統

if __name__ == "__main__":
    main()
