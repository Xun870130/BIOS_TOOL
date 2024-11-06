import pyautogui
import time
import requests
import powerSW2 as sw
from pynput.keyboard import Key, Controller
import GUI_Ctrl as GCtrl
import ImageResource

class AutoInstaller:
    """
    控制 Windows 客戶端的自動掛載和操作。

    主要功能包括：
    - 開啟 KVM 和 AC。
    - 啟動客戶端並進行圖形界面上的安裝操作。
    - 支援 ISO 檔案的自動掛載。

    屬性:
    - ip (str): 控制裝置的 IP 地址
    - iso_path (str): 系統映像檔的路徑
    - img_res (ImageResource): 圖像資源管理，獲取 GUI 操作所需的圖像
    - gui_ctrl (ClientController): 控制 GUI 點擊和圖片檢測
    - keyboard (Controller): 鍵盤控制器，模擬鍵盤操作
    - ctrl (DeviceController): 裝置控制器，管理硬體開關和狀態檢查
    """

    def __init__(self, ip="http://192.168.0.211:16628", iso_path=r'\\192.168.0.231\ABT-Dropbox\Common\ISO\Windows\OS_image\Win10_20H1_19041\OS.iso'):
        """
        初始化。

        :param ip: 控制設備的 IP 地址
        :param iso_path: ISO 檔案的路徑
        """
        self.ip = ip
        self.iso_path = iso_path
        self.img_res = ImageResource.ImageResource()  
        self.gui_ctrl = GCtrl.ClientController()  
        self.keyboard = Controller()  
        self.ctrl = sw.DeviceController(self.ip)  

    def start_installation(self):
        """
        主安裝流程:
        控制設備上電、檢查電源狀態，並自動開啟 CMD 視窗啟動 Java 客戶端，並重啟系統進行 GUI 操作。
        """
        # 打開 KVM 和 AC，並檢查電源狀態
        self.ctrl.kvm_on()
        self.ctrl.ac_on()
        time.sleep(20)
        
        try:
            status = self.ctrl.power_status()
            if "true" in status:
                print("Power is already on")
            else:
                self.ctrl.power_on()
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

        # 打開 CMD，並啟動 Java 客戶端
        self.gui_ctrl.open_cmd()
        self.gui_ctrl.start_client('windows')
        self.ctrl.reset()  # 系統重啟
        
        # 執行 GUI 操作
        self._perform_gui_actions()
        time.sleep(1)
        
        # 處理重啟流程
        self._handle_restart()

    def _perform_gui_actions(self):
        """
        執行主要 GUI 操作:
        定位各個 UI 元素並執行相應的點擊操作，掛載 ISO 映像，並打開 CMD。
        """
        dropdown_img = self.img_res.get_image_path("dropdown")
        pin_img = self.img_res.get_image_path("pin9000")
        viewer_img = self.img_res.get_image_path("viewer")

        # 點擊各個圖片元素
        time.sleep(1.5)
        self.gui_ctrl.locate_and_click(1, dropdown_img, confidence=0.9)
        time.sleep(1.5)
        self.gui_ctrl.locate_and_click(1, pin_img, confidence=0.8)
        time.sleep(2)
        
        # 反覆點擊 viewer 直到圖片消失
        def click_viewer():
            self.gui_ctrl.locate_and_click(2, viewer_img, confidence=0.8)
        self.gui_ctrl.wait_for_image(viewer_img, action=click_viewer, repeat=True)

        # 等待進入下一步操作的畫面
        scr_img = self.img_res.get_image_path("scr")
        self.gui_ctrl.wait_for_image(scr_img, timeout=90)

        # 定位並點擊 UI 元素進行掛載 ISO
        vm9000_img = self.img_res.get_image_path("VM9000")
        add_img = self.img_res.get_image_path("wadd")
        isofile_img = self.img_res.get_image_path("wiso")
        mount_img = self.img_res.get_image_path("wmount")
        windows_img = self.img_res.get_image_path("windows")
        cmd_img = self.img_res.get_image_path("CMD")

        # 執行掛載操作
        self.gui_ctrl.locate_and_click(1, vm9000_img, confidence=0.8)
        time.sleep(1)
        self.gui_ctrl.locate_and_click(1, add_img, confidence=0.6)
        time.sleep(2)
        self.gui_ctrl.locate_and_click(1, isofile_img, confidence=0.6)
        time.sleep(1)
        self.gui_ctrl.mount_iso(self.iso_path)
        self.gui_ctrl.locate_and_click(1, mount_img, confidence=0.8)
        time.sleep(5)
        self.gui_ctrl.locate_and_click(3, windows_img, confidence=0.8)
        time.sleep(1)
        
        # 定位 CMD 圖片，並進行雙擊
        cmd_location = pyautogui.locateOnScreen(cmd_img, confidence=0.8)
        if cmd_location:
            pyautogui.moveTo(pyautogui.center(cmd_location))
        time.sleep(2)
        self.gui_ctrl.locate_and_click(2, cmd_img, confidence=0.8)
        time.sleep(1)
        
        # 釋放 Win 和 Shift 鍵
        self.keyboard.release(Key.cmd) 
        self.keyboard.release(Key.shift)
        time.sleep(3)

    def _handle_restart(self):
        """
        處理系統重啟及 UEFI 掛載
        """
        # 重啟系統，並等待 CMD 錯誤出現
        self.gui_ctrl.restart_system()
        time.sleep(1)

        cmd_err_img = self.img_res.get_image_path("CMDERROR")
        self.gui_ctrl.wait_for_image(cmd_err_img, repeat=True, action=self.gui_ctrl.restart_system)
        
        # 等待 UEFI 畫面後執行 UEFI 操作
        uefi_img = self.img_res.get_image_path("UEFI")
        self.gui_ctrl.wait_for_image(uefi_img, action=self.gui_ctrl.UEFI)
