import pyautogui
import os
import time
from pynput.keyboard import Key, Controller

class ClientController:
    """
    ClientController 類:
    用於控制客戶端的自動化啟動和 GUI 操作，包括打開 CMD、啟動 Java 客戶端、掛載 ISO 文件，
    以及控制圖片檢測和鍵盤模擬操作。
    """
    def __init__(self):
        self.keyboard = Controller()
        self.current_directory = os.getcwd()

    def open_cmd(self):
        """
        打開 CMD 視窗:
        執行 Windows 鍵 + R 打開執行視窗，並輸入 'cmd' 以啟動命令提示字元。
        """
        self.keyboard.press(Key.cmd)
        self.keyboard.press('r')
        self.keyboard.release('r')
        self.keyboard.release(Key.cmd)
        time.sleep(1)
        self.keyboard.type('cmd')
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(1)

    def start_client(self,type: str):
        """
        打開 Client:
        在 CMD 中執行客戶端的啟動命令，並設置字體平滑參數。
        - type : java/windows
        """
        if type == 'java':
            command = rf'"{self.current_directory}\java\bin\java.exe" -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -jar "{self.current_directory}\JavaClient.jar" 192.168.10.211:9000 -u administrator -p password'
        elif type == 'windows':
            command = rf' "C:\__RVS_Execute_Software__\Winclient\WinClient.exe" 192.168.10.211:9000 -u administrator -p password'
        else:
            print('path error')
        self.keyboard.type(command)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(5)

    def locate_and_click(self, click: int, image_path: str, confidence: float=0.8) -> bool:
        """
        根據圖片定位並點擊:
        使用指定的匹配度來定位螢幕上的圖片，並根據 `click` 的值執行不同的點擊操作。
        
        :param click: 點擊操作類型 (1: 單擊, 2: 雙擊, 3: 右鍵點擊)
        :param image_path: 圖片的檔案路徑
        :param confidence: 圖片匹配的信心度，範圍為 0.0 - 1.0 (默認為 0.8)
        :return: 成功找到並點擊圖片則返回 True，否則返回 False
        """
        self.click=click
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            if click==1:
                pyautogui.click(pyautogui.center(location))
            elif click==2:
                pyautogui.doubleClick(pyautogui.center(location))
            elif click==3:
                pyautogui.rightClick(pyautogui.center(location))
            else:
                print(image_path,"error")
            return True
        return False

    def mount_iso(self, iso_path: str):
        """
        在 CMD 中掛載 ISO 檔案:
        
        :param iso_path: ISO 檔案的完整路徑
        """
        self.keyboard.type(iso_path)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(1)

    def restart_system(self):
        """
        重啟系統:
        使用 CMD 中的命令 `shutdown /r /fw /t 0` 重啟系統並進入韌體介面。
        """

        self.keyboard.type('shutdown /r /fw /t 0')
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def UEFI(self):
        """
        進入 UEFI 模式:
        模擬按鍵以進入 UEFI 模式並選擇啟動選項。
        """
        time.sleep(5)
        self.keyboard.press(Key.right)
        self.keyboard.release(Key.right)
        time.sleep(0.1)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(0.1)
        self.keyboard.press(Key.down)
        self.keyboard.release(Key.down)
        time.sleep(0.1)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter) 
        time.sleep(4)#讀取緩衝
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)  

    def wait_for_image(self, image_path: str, confidence: float=0.8, timeout: int=60, action: callable=None,repeat: bool=False):
        """
        等待圖片出現在螢幕上並執行指定動作 (action):
        在 `timeout` 秒內反覆檢查螢幕是否出現指定圖片。若圖片找到並指定 `action`，
        則執行 `action` 函數。若 `repeat=True`，則圖片每次出現都執行 `action`。
        
        :param image_path: 圖片的路徑
        :param confidence: 圖片匹配的信心度，範圍為 0.0 - 1.0 (默認為 0.8)
        :param timeout: 超時時間，預設為 60 秒
        :param action: 找到圖片後執行的動作函數 
        :param repeat: 是否在圖片多次出現時重複執行動作，預設為 False

        :return: 成功找到並執行動作則返回 True，否則返回 False
        """
        start_time = time.time()
        while True:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location is not None:
                # 如果有指定動作，則執行
                if action:
                    action()
                    time.sleep(3)
                    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                    if location is None:
                        print(image_path)
                        return True
                if not repeat:  
                    return True
            # 計算已經過時間
            elapsed_time = time.time() - start_time
            print(f"\r Waiting . . . {int(elapsed_time)} sec", end="")
            if elapsed_time >= timeout:
                print("\nTimeout:" ,image_path ,"not found.")
                return False
            # 延遲，避免頻繁檢查
            time.sleep(1)