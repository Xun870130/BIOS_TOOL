
#Java版本的客戶端自動開啟掛載系統映像檔 自動重啟 開啟UEFI掛載OS並安裝

import pyautogui
import time
import requests
import powerSW2 as sw
from pynput.keyboard import Key, Controller
import GUI_Ctrl as GCtrl
import ImageResource
impath=ImageResource.ImageResource()
Guic = GCtrl.JavaClientController()
keyboard = Controller()
ctrl=sw.DeviceController("http://192.168.0.211:16628")
#====================================================================================================================================================
#KVM、AC、power on
ctrl.kvm_on()
ctrl.ac_on()
time.sleep(10)
#檢查電源狀態是否執行開啟
try:
    status = ctrl.power_status()
    if "true" in status:
        print("power is allready on")
    else:
        ctrl.power_on()
except requests.exceptions.RequestException as e:
    print("請求失敗:", e)

# 開啟執行視窗(可能會產生BUG)
#win+R CMD
Guic.open_cmd()
#開啟java client
Guic.start_java_client()
#====================================================================================================================================================
ctrl.reset()#重開機
time.sleep(25)

image_path1 = impath.get_image_path("dropdown")
Guic.locate_and_click(1,image_path1, confidence=0.9)
time.sleep(1.5)
image_path2 = impath.get_image_path("pin9000")
Guic.locate_and_click(1,image_path2, confidence=0.8)
time.sleep(2)
image_path3 = impath.get_image_path("viewer")
Guic.locate_and_click(2,image_path3, confidence=0.8)

while True:  
    location = pyautogui.locateOnScreen(image_path3, confidence=0.8) 
    if location is not None:
        Guic.locate_and_click(2,image_path3, confidence=0.8)
        time.sleep(1)
    else:
        break
    
    # 延遲，避免頻繁檢查導致系統過載
    time.sleep(1)

time.sleep(10)
image_path4 = impath.get_image_path("VM9000")
Guic.locate_and_click(1,image_path4, confidence=0.8)
time.sleep(1)
image_path5 = impath.get_image_path("add")
Guic.locate_and_click(1,image_path5, confidence=0.6)
time.sleep(1)
image_path6 = impath.get_image_path("iosfile")
Guic.locate_and_click(1,image_path6, confidence=0.6)
time.sleep(1)

iso_path = r'\\192.168.0.231\ABT-Dropbox\Common\ISO\Windows\OS_image\Win10_20H1_19041\OS.iso'
Guic.mount_iso(iso_path)
time.sleep(1)
image_path8 = impath.get_image_path("mount")
Guic.locate_and_click(1,image_path8, confidence=0.8)
time.sleep(5)
image_path9 = impath.get_image_path("windows")
Guic.locate_and_click(3,image_path9, confidence=0.8)  
time.sleep(1)
image_path10 = impath.get_image_path("CMD")
pyautogui.moveTo(pyautogui.center(pyautogui.locateOnScreen(image_path10,confidence=0.8)))
time.sleep(2)
Guic.locate_and_click(2,image_path10, confidence=0.8)
time.sleep(1)
#====================================================================================================================================================
keyboard = Controller()
keyboard.release(Key.cmd) 
keyboard.release(Key.shift)  # 手動釋放WIN、Shift 鍵
time.sleep(3)

Guic.restart_system()
time.sleep(1)

image_path7 = impath.get_image_path("CMDERROR")
while True:  
    time.sleep(1)
    location = pyautogui.locateOnScreen(image_path7, confidence=0.8) 
    if location is not None:
        Guic.restart_system()
        time.sleep(1)
    else:
        # 如果圖片不存在，跳出循環
        break
    time.sleep(1)

image_path11 = impath.get_image_path("UEFI")
start_time = time.time()
while True:
    time.sleep(1)
    location = pyautogui.locateOnScreen(image_path11, confidence=0.8) 
    if location is not None:
        Guic.UEFI()
        break
    else:
        elapsed_time = time.time() - start_time  # 計算已經過時間
        print(f"\r waiting . . . {int(elapsed_time)} sec",end="")
        
        if elapsed_time >= 60:
            print("timeout")
            break
    time.sleep(1)

