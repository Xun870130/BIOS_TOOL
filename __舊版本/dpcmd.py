#
#自動更新BIOS
#
import subprocess
import os

fdilded_message = """
░▒▓████████▓▒░ ░▒▓███████▓▒░  ░▒▓███████▓▒░   ░▒▓██████▓▒░  ░▒▓███████▓▒░  
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░   ░▒▓███████▓▒░  ░▒▓███████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓████████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓██████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ 
    """

prog_message = """
 ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ 
||P |||r |||o |||g |||r |||a |||m |||i |||n |||g ||
||__|||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|
"""

success_message="""
░░      ░░░  ░░░░  ░░░      ░░░░      ░░░        ░░░      ░░░░      ░░
▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒
▓▓      ▓▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓      ▓▓▓▓▓      ▓▓▓▓      ▓▓
███████  ██  ████  ██  ████  ██  ████  ██  ██████████████  ████████  █
██      ████      ████      ████      ███        ███      ████      ██
"""



# 切換到目標目錄
directory = r"C:\Program Files (x86)\DediProg\SF100"

# 檢查芯片的命令
detect_command = ["dpcmd", "-d"]

# 程式燒錄的命令
current_directory = os.getcwd()
BIOS_path = os.path.join(current_directory, "BIOS", "IceLake_U_3.bin")
program_command = ["dpcmd", "-u", BIOS_path ]

# 用來檢查是否有目標字串
def run_command_and_check(command, success_keyword):
    try:
        # 執行命令並捕捉即時輸出
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=directory)

        # 讀取並即時輸出
        success = False
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())  # 即時輸出到控制台

                # 判斷是否找到目標字串
                if success_keyword in output:
                    success = True

        return success

    except Exception as e:
        print(f"命令執行失敗: {e}")
        return False


# 執行檢測芯片命令
print("正在檢測芯片...")
if run_command_and_check(detect_command, "W25Q256FV chip size is 33554432 bytes"):

    print(prog_message)
    
    # 執行燒錄命令
    if run_command_and_check(program_command, "Automatic program OK"):
        print(success_message)
    else:
        print("Failed: 程式燒錄失敗")
else:
    print(fdilded_message)
