import subprocess
import os

class Programmer:
    """
    Programmer 類:
    用於管理芯片的檢測和燒錄過程。包含執行檢查芯片、執行燒錄命令並顯示結果的功能。
    """

    def __init__(self, directory: str, bios_filename: str, ascii_art: callable):
        """
        初始化 Programmer 類。

        :param directory: dpcmd 執行目錄
        :param bios_filename: BIOS 檔案的名稱，用於燒錄
        :param ascii_art: ASCIIArtBuilder 對象，用於顯示 ASCII 輸出消息
        """
        self.directory = directory
        self.bios_path = os.path.join(os.getcwd(), "BIOS", bios_filename)
        self.ascii_art = ascii_art
        self.detect_command = ["dpcmd", "-d"]
        self.program_command = ["dpcmd", "-u", self.bios_path]

    def run_command_and_check(self, command: list[str], success_keyword: str) ->bool:
        """
        執行指定的命令並檢查輸出中是否包含目標字串。

        :param command: 執行的命令列表
        :param success_keyword: 輸出中成功的關鍵字，判斷是否執行成功
        :return: 如果找到關鍵字返回 True，否則返回 False
        """
        try:
            # 執行命令並捕捉即時輸出
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=self.directory)
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

    def detect_chip(self) ->bool:
        """
        檢測芯片是否存在。
        使用 `run_command_and_check` 方法執行檢測命令。
        
        :return: 如果檢測成功返回 True，否則返回 False
        """
        print("正在檢測芯片...")
        return self.run_command_and_check(self.detect_command, "W25Q256FV chip size is 33554432 bytes")

    def program_chip(self) ->bool:
        """
        執行芯片燒錄過程。
        使用 `run_command_and_check` 方法執行燒錄命令。
        
        :return: 如果燒錄成功返回 True，否則返回 False
        """
        print(self.ascii_art.call("programing"))
        return self.run_command_and_check(self.program_command, "Automatic program OK")

    def run(self):
        """
        主程序入口:
        執行芯片檢測和燒錄，並根據結果輸出對應的 ASCII 信息。
        """
        if self.detect_chip():
            if self.program_chip():
                print(self.ascii_art.call("success"))
            else:
                print("Failed: 程式燒錄失敗")
        else:
            print(self.ascii_art.call("error"))
            


