import powerSW2 as sw

import WindowsClient
import JavaClient

import ASCIIART
import DediProg_CMD

installer = WindowsClient.AutoInstaller()
#installer = JavaClient.AutoInstaller()

controller = sw.DeviceController("http://192.168.0.211:16628")
# 初始化 ASCII Art 和 Programmer 類
ascii_art = ASCIIART.ASCIIArtBuilder() # 一定要匯入，否則DP會出錯
directory = r"C:\Program Files (x86)\DediProg\SF100"
bios_filename = "IceLake_U_3.bin"
programmer = DediProg_CMD.Programmer(directory, bios_filename, ascii_art)


# controller.ACoffcheck()
# controller.dp_on()
# programmer.run()
# controller.dp_off()
# controller.cmos_switch()
# controller.AConcheck()
installer.start_installation()