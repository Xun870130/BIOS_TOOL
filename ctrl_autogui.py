import pyautogui
import os
import time
import sys
import res_image
from pynput.keyboard import Key, Controller

class ClientController:
    """
    ClientController 類:
    用於控制客戶端的自動化啟動和 GUI 操作，包括打開 CMD、啟動 Java 客戶端、掛載 ISO 文件，
    以及控制圖片檢測和鍵盤模擬操作。
    """

    def __init__(self, iso_path: str = r'\\192.168.0.231\ABT-Dropbox\Common\ISO\Windows\OS_image\Win10_20H1_19041\OS.iso'):
        """
        初始化 ClientController 類:
        設定 ISO 檔案路徑、資源加載器和鍵盤控制器。

        Args:
            iso_path (str): 預設的 ISO 檔案路徑。
        """
        self.iso_path = iso_path
        self.get_path = res_image.ImageResource()
        self.keyboard = Controller()
        self.current_directory2 = os.getcwd()
        if hasattr(sys, '_MEIPASS'):
            # 如果在 PyInstaller 打包後的環境中，使用 _MEIPASS 獲取路徑
            self.current_directory = sys._MEIPASS
        else:
            # 否則，使用標準的當前工作目錄
            self.current_directory2 = os.getcwd()

    def open_cmd(self):
        """
        打開 CMD 視窗:
        執行 Windows 鍵 + R 打開執行視窗，並輸入 'cmd' 以啟動命令提示字元。
        """
        self.keyboard.press(Key.cmd)
        self.press_and_release('r', delay=0.5)
        self.keyboard.release(Key.cmd)
        time.sleep(1)
        self.keyboard.type('cmd')
        self.press_and_release(Key.enter, delay=1)

    def start_client(self, type: str, ip: str):
        """
        打開 Client:
        在 CMD 中執行客戶端的啟動命令，並設置字體平滑參數。

        Args:
            type (str): 客戶端類型 (java/windows)。
            ip (str): 客戶端目標 IP。
        """
        if ip == "http://192.168.0.211:16628":
            if type == 'java':
                command = rf'"{self.current_directory2}\java\bin\java.exe" -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -jar "{self.current_directory2}\JavaClient.jar" 192.168.10.211:9000 -u administrator -p password '
            elif type == 'windows':
                command = rf' "C:\__RVS_Execute_Software__\Winclient\WinClient.exe" 192.168.10.211:9000 -u administrator -p password '
            else:
                print('path error')
        elif ip == "http://192.168.0.213:16628":
            if type == 'java':
                command = rf'"{self.current_directory2}\java\bin\java.exe" -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -jar "{self.current_directory2}\JavaClient.jar" 192.168.10.213:9000 -u administrator -p password '
            elif type == 'windows':
                command = rf' "C:\__RVS_Execute_Software__\Winclient\WinClient.exe" 192.168.10.213:9000 -u administrator -p password '
            else:
                print('path error') 
        else:
            print("ip error")
        self.keyboard.type(command)
        self.press_and_release(Key.enter, delay=5)

    def locate_and_click(self, click: int, image_path: str, confidence: float = 0.8, delay: float = 0) -> bool:
        """
        根據圖片定位並點擊:
        使用指定的匹配度來定位螢幕上的圖片，並根據 `click` 的值執行不同的點擊操作。

        Args:
            click (int): 點擊操作類型 (1: 單擊, 2: 雙擊, 3: 右鍵點擊)。
            image_path (str): 圖片的檔案路徑。
            confidence (float): 圖片匹配的信心度，範圍為 0.0 - 1.0 (默認為 0.8)。
            delay (float): 操作執行完成後的延遲，預設為 0 秒。

        Returns:
            bool: 成功找到並點擊圖片則返回 True，否則返回 False。
        """
        self.click = click
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        try:
            if location:
                if click == 1:
                    pyautogui.click(pyautogui.center(location))
                    time.sleep(delay)
                elif click == 2:
                    pyautogui.doubleClick(pyautogui.center(location))
                    time.sleep(delay)
                elif click == 3:
                    pyautogui.rightClick(pyautogui.center(location))
                    time.sleep(delay)
                else:
                    print(image_path, "error")
                return True
            return False
        except pyautogui.ImageNotFoundException:
            pass

    def mount_iso(self, type: str):
        """
        掛載 ISO 檔案:
        根據客戶端類型選擇對應的資源圖片並掛載 ISO 檔案。

        Args:
            type (str): 客戶端類型 (windows/java)。
        """
        self.type = type
        if type == "java":
            vm9000_img = self.get_path.get_image_path("VM9000")
            add_img = self.get_path.get_image_path("add")
            isofile_img = self.get_path.get_image_path("isofile")
            mount_img = self.get_path.get_image_path("mount")
        elif type == "windows":
            vm9000_img = self.get_path.get_image_path("VM9000")
            add_img = self.get_path.get_image_path("wadd")
            isofile_img = self.get_path.get_image_path("wiso")
            mount_img = self.get_path.get_image_path("wmount") 

        self.locate_and_click(1, vm9000_img, confidence=0.8, delay=1)
        self.locate_and_click(1, add_img, confidence=0.6, delay=2)
        self.locate_and_click(1, isofile_img, confidence=0.6, delay=1)
        self.keyboard.type(self.iso_path)
        self.press_and_release(Key.enter, delay=1)
        self.locate_and_click(1, mount_img, confidence=0.8, delay=5)

    def restart_system(self):
        """
        重啟系統:
        使用 CMD 中的命令 `shutdown /r /fw /t 0` 重啟系統並進入韌體介面。
        """
        self.keyboard.type('shutdown /r /fw /t 0')
        self.press_and_release(Key.enter, delay=0.5)

    def press_and_release(self, press_Key, delay: float = 0, do: int = 1):
        """
        模擬按鍵操作:
        模擬按下和釋放指定按鍵的動作，並根據需要重複執行。

        Args:
            press_Key: 要模擬的按鍵 (Key)。
            delay (float): 每次按鍵操作後的延遲時間，默認為 0 秒。
            do (int): 要重複執行的次數，默認為 1。
        """
        for i in range(do, 0, -1):
            self.keyboard.press(press_Key)
            self.keyboard.release(press_Key)
            time.sleep(delay)

    def fast_boot_close(self):
        """
        關閉快速啟動:
        在 UEFI 設置中，導航到快速啟動選項並將其禁用，然後儲存設定並重新啟動。
        """
        time.sleep(1)
        self.press_and_release(Key.right, delay=1, do=2)
        self.press_and_release(Key.down, delay=1)
        self.press_and_release(Key.enter, delay=2)

        # 進入啟動選項列表
        self.press_and_release(Key.down, delay=0.5, do=4)
        self.press_and_release(Key.right, delay=0.5)

        # 選擇快速啟動選項
        self.press_and_release(Key.down, delay=0.5, do=10)

        # 判斷是否需要設定
        path = self.get_path.get_image_path("fast_boot")
        time.sleep(1)
        self.wait_for_image(path, confidence=0.9, delay=0.1)
        time.sleep(1)
        self.press_and_release(Key.enter, delay=0.5)

        try:
            locate = pyautogui.locateOnScreen(self.get_path.get_image_path("fast_boot_enable"), confidence=0.9)

            if locate is not None:
                # 快速啟動已啟用，返回上層菜單
                self.press_and_release(Key.esc, delay=0.5)
                self.press_and_release(Key.f10, delay=0.5)
                self.press_and_release(Key.enter, delay=0.5)
            else:
                # 禁用快速啟動，保存設定
                self.press_and_release(Key.down, delay=0.5)
                self.press_and_release(Key.enter, delay=0.5)
                self.press_and_release(Key.f10, delay=0.5)
                self.press_and_release(Key.enter, delay=0.5)
        except Exception as e:
            # 捕捉所有其他未預期的例外
            print(f"Unhandled error: {e}")

        # 持續按下 ESC 進入 UEFI 選單
        time.sleep(1)
        start = time.time()
        while True:
            try:
                locate = pyautogui.locateOnScreen(self.get_path.get_image_path("esc"), confidence=0.8)
                if locate is None:
                    self.press_and_release(Key.esc, delay=0.1)
                else:
                    print('Release ESC key.')
                    break
            except Exception as e:
                pass
            if time.time() - start > 20:
                print('Timeout: Stop pressing ESC key.')
                break

    def select_usb_device(self):
        """
        選擇 USB 裝置:
        在啟動管理器中選擇 USB 裝置以啟動，若失敗則重新掛載 ISO 並再次嘗試。
        """
        self.wait_for_image(self.get_path.get_image_path("boot_manager"))
        try:
            locate = pyautogui.locateOnScreen(self.get_path.get_image_path("usb_device"), confidence=0.8)
            pyautogui.screenshot("usb_device.png", locate)
            if locate is not None:
                time.sleep(1)
                self.press_and_release(Key.down, delay=0.1)
                self.press_and_release(Key.enter)
                self.wait_for_image(self.get_path.get_image_path("press_enter"),
                                    confidence=0.6,
                                    timeout=10,
                                    action=lambda: self.press_and_release(Key.enter))
            else:
                # 再次掛載 ISO 並選擇裝置
                self.mount_iso(self.type)
                time.sleep(5)
                self.press_and_release(Key.down, delay=0.1)
                self.press_and_release(Key.enter)
                self.wait_for_image(self.get_path.get_image_path("press_enter"),
                                    confidence=0.6,
                                    timeout=10,
                                    action=lambda: self.press_and_release(Key.enter))
        except pyautogui.ImageNotFoundException:
            pass

    def re_mount(self):
        """
        重新掛載 ISO:
        若啟動失敗，進行 ISO 的重新掛載，並再次選擇啟動裝置。
        """
        time.sleep(5)
        self.press_and_release(Key.enter, delay=0.1)
        self.wait_for_image(self.get_path.get_image_path("UEFI"))
        self.mount_iso(self.type)

        # 進入啟動管理器
        self.press_and_release(Key.right, delay=0.1)
        self.press_and_release(Key.enter, delay=0.1)
        self.select_usb_device()

    def UEFI(self):
        """
        進入 UEFI 模式:
        模擬按鍵操作進入 UEFI 模式，進行快速啟動的禁用與啟動裝置的選擇。
        """
        self.wait_for_image(self.get_path.get_image_path("UEFI"))
        self.fast_boot_close()
        self.wait_for_image(self.get_path.get_image_path("UEFI"))

        # 進入啟動管理器
        self.press_and_release(Key.right, delay=0.1)
        self.press_and_release(Key.enter, delay=0.1)
        self.wait_for_image(self.get_path.get_image_path("boot_manager"))

        self.select_usb_device()
        self.wait_for_image(self.get_path.get_image_path("boot_failed"),
                            timeout=20,
                            action=self.re_mount)

    def wait_for_image(self, image_path: str, confidence: float = 0.8,
                       timeout: int = 60, action: callable = None, repeat: bool = False, delay: float = 1):
        """
        等待圖片出現在螢幕上並執行指定動作 (action):
        在 `timeout` 秒內反覆檢查螢幕是否出現指定圖片。若圖片找到並指定 `action`，
        則執行 `action` 函數。若 `repeat=True`，則圖片每次出現都執行 `action`。

        Args:
            image_path (str): 圖片的路徑。
            confidence (float): 圖片匹配的信心度，範圍為 0.0 - 1.0 (默認為 0.8)。
            timeout (int): 超時時間，預設為 60 秒。
            action (callable): 找到圖片後執行的動作函數。
            repeat (bool): 是否在圖片多次出現時重複執行動作，預設為 False。
            delay (float): 每次檢查後的延遲時間，預設為 1 秒。

        Returns:
            bool: 成功找到並執行動作則返回 True，否則返回 False。
        """
        start_time = time.time()

        while True:
            try:
                time.sleep(0.5)  # 增加檢查間隔，減少頻繁檢查
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location is not None:
                    if action:
                        action()
                        try:
                            time.sleep(0.3)
                            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                            if location is None:
                                break
                        except pyautogui.ImageNotFoundException:
                            break
                    if not repeat:
                        return True

                elapsed_time = time.time() - start_time
                print(f"\r Waiting . . . {int(elapsed_time)} sec", image_path, end="")
                if elapsed_time >= timeout:
                    print("\nTimeout:", image_path, "not found.")
                    return False
                time.sleep(delay)
            except pyautogui.ImageNotFoundException:
                pass

