import pyautogui
import os
import time
import sys
import ImageResource
from pynput.keyboard import Key, Controller

class ClientController:
    """
    ClientController 類:
    用於控制客戶端的自動化啟動和 GUI 操作，包括打開 CMD、啟動 Java 客戶端、掛載 ISO 文件，
    以及控制圖片檢測和鍵盤模擬操作。
    """
    def __init__(self, iso_path: str=r'\\192.168.0.231\ABT-Dropbox\Common\ISO\Windows\OS_image\Win10_20H1_19041\OS.iso'):
        self.iso_path = iso_path
        self.get_path = ImageResource.ImageResource()
        self.keyboard = Controller()
        if hasattr(sys, '_MEIPASS'):
            # 如果在 PyInstaller 打包后的环境中，使用 _MEIPASS 获取路径
            self.current_directory = sys._MEIPASS
        else:
            # 否则，使用标准的当前工作目录
            self.current_directory = os.getcwd()

    def open_cmd(self):
        """
        打開 CMD 視窗:
        執行 Windows 鍵 + R 打開執行視窗，並輸入 'cmd' 以啟動命令提示字元。
        """
        self.keyboard.press(Key.cmd)
        self.press_and_release('r',delay=0.5)
        self.keyboard.release(Key.cmd)
        time.sleep(1)
        self.keyboard.type('cmd')
        self.press_and_release(Key.enter,delay=1)

    def start_client(self,type: str):
        """
        打開 Client:
        在 CMD 中執行客戶端的啟動命令，並設置字體平滑參數。
        - type : java/windows
        """
        if type == 'java':
            command = rf'"{self.current_directory}\java\bin\java.exe" -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -jar "{self.current_directory}\JavaClient.jar" 192.168.10.211:9000 -u administrator -p password '
        elif type == 'windows':
            command = rf' "C:\__RVS_Execute_Software__\Winclient\WinClient.exe" 192.168.10.211:9000 -u administrator -p password '
        else:
            print('path error')
        self.keyboard.type(command)
        self.press_and_release(Key.enter,delay=5)

    def locate_and_click(self, click: int, image_path: str, confidence: float=0.8,delay: float=0) -> bool:
        """
        根據圖片定位並點擊:
        使用指定的匹配度來定位螢幕上的圖片，並根據 `click` 的值執行不同的點擊操作。
        
        :param click: 點擊操作類型 (1: 單擊, 2: 雙擊, 3: 右鍵點擊)
        :param image_path: 圖片的檔案路徑
        :param confidence: 圖片匹配的信心度，範圍為 0.0 - 1.0 (默認為 0.8)
        :param delay: 操作執行完成後，等待下一個判讀圖片刷新，預設為0秒
        :return: 成功找到並點擊圖片則返回 True，否則返回 False
        """
        self.click=click
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        try:
            if location:
                if click==1:
                    pyautogui.click(pyautogui.center(location))
                    time.sleep(delay)
                elif click==2:
                    pyautogui.doubleClick(pyautogui.center(location))
                    time.sleep(delay)
                elif click==3:
                    pyautogui.rightClick(pyautogui.center(location))
                    time.sleep(delay)
                else:
                    print(image_path,"error")
                return True
            return False
        except pyautogui.ImageNotFoundException:
            pass

    def mount_iso(self, type: str):
        self.type=type
        """
        在 usb_device 中掛載 ISO 檔案:
        
        :param type: 客戶端類型(windows/java)
        """
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
        self.press_and_release(Key.enter,delay=1)
        self.locate_and_click(1, mount_img, confidence=0.8, delay=5)
 

    def restart_system(self):
        """
        重啟系統:
        使用 CMD 中的命令 `shutdown /r /fw /t 0` 重啟系統並進入韌體介面。
        """

        self.keyboard.type('shutdown /r /fw /t 0')
        self.press_and_release(Key.enter,delay=0.5)

    def press_and_release(self, press_Key, delay: float=0, do: int=1):
        for i in range(do,0,-1):
            self.keyboard.tap(press_Key)
            time.sleep(delay) 

    def fast_boot_close(self):
        #setup utility
        time.sleep(1)
        self.press_and_release(Key.right,delay=1,do=2)
        self.press_and_release(Key.down,delay=1)
        self.press_and_release(Key.enter,delay=2)
        #enter boot list
        self.press_and_release(Key.down,delay=0.5,do=4)
        self.press_and_release(Key.right,delay=0.5)
        #select fast os boot
        self.press_and_release(Key.down,delay=0.5,do=10)
        #判斷是否需要設定
        path = self.get_path.get_image_path("fast_boot_disable")
        #self.wait_for_image(path,confidence=0.9,delay=0.1)
        try:
            locate = pyautogui.locateOnScreen(path, confidence=0.9)
            if locate is not None:
                self.press_and_release(Key.f10,delay=0.5)
                self.press_and_release(Key.enter,delay=0.5)
            else:
                self.press_and_release(Key.enter,delay=0.5)
                self.press_and_release(Key.down,delay=0.5)
                self.press_and_release(Key.enter,delay=0.5)
                self.press_and_release(Key.f10,delay=0.5)
                self.press_and_release(Key.enter,delay=0.5)
        except pyautogui.ImageNotFoundException:
                 pass
        #press ESC restart UEFI
        time.sleep(1)
        start = time.time()
        while True:
            try:
                locate = pyautogui.locateOnScreen(self.get_path.get_image_path("esc"),confidence=0.8)
                if locate is None:
                    self.press_and_release(Key.esc,delay=0.1)
                    print('in 143 line')
                else:
                    print('release')
                    break
            except pyautogui.ImageNotFoundException:
                pass
            if time.time()-start > 20 :
                print('times up,stop press esc key')
                break
    
    def select_usb_device(self):
        time.sleep(1)
        try:
            locate = pyautogui.locateOnScreen(self.get_path.get_image_path("usb_device"),confidence=0.8)
            
            if locate is not None:
                time.sleep(1)
                self.press_and_release(Key.down,delay=0.1)
                self.press_and_release(Key.enter,delay=2)
                self.press_and_release(Key.enter)
                
            else:
                #mount iso again & select device
                self.mount_iso(self.type)
                time.sleep(5)
                self.press_and_release(Key.down,delay=0.1)
                self.press_and_release(Key.enter,delay=2)
                self.press_and_release(Key.enter)   
                    
        except pyautogui.ImageNotFoundException:
            pass

    def UEFI(self):
        """
        進入 UEFI 模式:
        模擬按鍵以進入 UEFI 模式並選擇啟動選項。

        :param type: 客戶端類型(windows/java)
        """
        self.fast_boot_close()
        self.wait_for_image(self.get_path.get_image_path("UEFI"))
        #enter boot manager
        self.press_and_release(Key.right, delay=0.1)
        self.press_and_release(Key.enter, delay=0.1)
        self.wait_for_image(self.get_path.get_image_path("boot_manager"))

        self.select_usb_device()

        def re_mount():
            self.mount_iso(self.type)
            self.press_and_release(Key.enter, delay=0.1)
            #enter boot manager
            self.press_and_release(Key.right, delay=0.1)
            self.press_and_release(Key.enter, delay=0.1)
            self.select_usb_device()
        self.wait_for_image(self.get_path.get_image_path("boot_failed"),timeout=20,action=re_mount)
        
  
                
    def wait_for_image(self, image_path: str, confidence: float=0.8, timeout: int=60, action: callable=None,repeat: bool=False,delay: float=1):
        """
        等待圖片出現在螢幕上並執行指定動作 (action):
        在 `timeout` 秒內反覆檢查螢幕是否出現指定圖片。若圖片找到並指定 `action`，
        則執行 `action` 函數。若 `repeat=True`，則圖片每次出現都執行 `action`。
        
        :param image_path: 圖片的路徑
        :param confidence: 圖片匹配的信心度，範圍為 0.0 - 1.0 (默認為 0.8)
        :param timeout: 超時時間，預設為 60 秒
        :param action: 找到圖片後執行的動作函數 
        :param repeat: 是否在圖片多次出現時重複執行動作，預設為 False
        :param delay: 預設 1 秒
        :return: 成功找到並執行動作則返回 True，否則返回 False
        """
        start_time = time.time()
        while True:
            try:
                time.sleep(0.1)
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location is not None:
                    # 如果有指定動作，則執行
                    if action:
                        action()
                        
                        try:
                            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                            print("246")
                            if location is None:
                                # 圖片消失後跳出迴圈
                                break
                        except pyautogui.ImageNotFoundException:
                            break   
                    if not repeat:  
                        return True  
            except pyautogui.ImageNotFoundException:
                pass
            # 計算已經過時間
            elapsed_time = time.time() - start_time
            print(f"\r Waiting . . . {int(elapsed_time)} sec",image_path, end="")
            if elapsed_time >= timeout:
                print("\nTimeout:" ,image_path ,"not found.")
                return False
            # 延遲，避免頻繁檢查
            time.sleep(delay)