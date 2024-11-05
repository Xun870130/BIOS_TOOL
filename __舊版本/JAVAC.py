import pyautogui
import time
import requests
import os
from pynput.keyboard import Key, Controller
keyboard = Controller()
#====================================================================================================================================================
#KVM、AC、power on
url = "http://192.168.0.211:16628/arduino/gpio?func=kvm&act=on" # kvm on
try:
    response = requests.get(url)
    response.raise_for_status()  # 確保請求成功
    print("KVM turn on:", response.text)
except requests.exceptions.RequestException as e:
    print("KVM failed:", e)
url = "http://192.168.0.211:16628/arduino/gpio?func=ac&act=on" # ac on
try:
    response = requests.get(url)
    response.raise_for_status()  # 確保請求成功
    print("AC turn on:", response.text)
except requests.exceptions.RequestException as e:
    print("AC failed:", e)

time.sleep(10)

#檢查電源狀態是否執行開啟
url = "http://192.168.0.211:16628/arduino/gpio?func=power_click&act=on" # power on
urlPS="http://192.168.0.211:16628/arduino/gpio?func=state" # power status
try:
    response = requests.get(urlPS)#檢查power status 狀態
    response.raise_for_status()  # 確保請求成功
    if "true" in response.text:
        print("power is allready on")

    else:
        response = requests.get(url)
        response.raise_for_status()  # 確保請求成功
        print("請求成功:", response.text)
except requests.exceptions.RequestException as e:
    print("請求失敗:", e)

# 開啟執行視窗(可能會產生BUG)
""" pyautogui.hotkey('win', 'r')  
time.sleep(1)
pyautogui.keyUp('win')
pyautogui.write('cmd', interval=0.1)
pyautogui.press('enter')
time.sleep(1)
current_directory = os.getcwd()

command = rf'"{current_directory}\java\bin\java.exe" -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -jar "{current_directory}\JavaClient.jar" 192.168.10.211:9000 -u administrator -p password'
pyautogui.write(command, interval=0.01)
pyautogui.press('enter')
time.sleep(20) """

#win+R CMD
keyboard.press(Key.cmd)
keyboard.press('r')
keyboard.release('r')
keyboard.release(Key.cmd)
time.sleep(1)
keyboard.type('cmd')
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

#開啟java client
current_directory = os.getcwd()
command = rf'"{current_directory}\java\bin\java.exe" -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -jar "{current_directory}\JavaClient.jar" 192.168.10.211:9000 -u administrator -p password'
keyboard.type(command)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(5)

#====================================================================================================================================================
url = "http://192.168.0.211:16628/arduino/gpio?func=reset" # reset on
try:
    response = requests.get(url)
    response.raise_for_status()  # 確保請求成功
    print("請求成功:", response.text)
except requests.exceptions.RequestException as e:
    print("請求失敗:", e)
time.sleep(25)

current_directory = os.getcwd()
image_path1 = os.path.join(current_directory, 'UI_image', 'dropdown.png')
image_path2 = os.path.join(current_directory, 'UI_image', 'pin9000.png')
image_path3 = os.path.join(current_directory, 'UI_image', 'viewer.jpg')
image_path4 = os.path.join(current_directory, 'UI_image', 'VM9000.png')
image_path5 = os.path.join(current_directory, 'UI_image', 'add.jpg')
image_path6 = os.path.join(current_directory, 'UI_image', 'iosfile.jpg')
image_path7 = os.path.join(current_directory, 'UI_image', 'CMDERROR.jpg')
image_path8 = os.path.join(current_directory, 'UI_image', 'mount.jpg')
image_path9 = os.path.join(current_directory, 'UI_image', 'windows.jpg')
image_path10 = os.path.join(current_directory, 'UI_image', 'CMD.jpg')

location = pyautogui.locateOnScreen(image_path1, confidence=0.9)
pyautogui.moveTo(pyautogui.center(location))
time.sleep(1.5)

location = pyautogui.locateOnScreen(image_path2, confidence=0.8)
pyautogui.click(pyautogui.center(location))
time.sleep(2)

location = pyautogui.locateOnScreen(image_path3, confidence=0.8)
pyautogui.click(pyautogui.center(location))
pyautogui.click(pyautogui.center(location))
time.sleep(10)

location = pyautogui.locateOnScreen(image_path4, confidence=0.8)
pyautogui.click(pyautogui.center(location))
time.sleep(1)

location = pyautogui.locateOnScreen(image_path5, confidence=0.6)
pyautogui.click(pyautogui.center(location))
time.sleep(1)

location = pyautogui.locateOnScreen(image_path6, confidence=0.6)
pyautogui.click(pyautogui.center(location))
time.sleep(1)

command = r'\\192.168.0.231\ABT-Dropbox\Common\ISO\Windows\OS_image\Win10_20H1_19041\OS.iso'
keyboard.type(command)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

location = pyautogui.locateOnScreen(image_path8, confidence=0.8)
pyautogui.click(pyautogui.center(location))
time.sleep(5)

location = pyautogui.locateOnScreen(image_path9, confidence=0.8)
pyautogui.rightClick(pyautogui.center(location))  
time.sleep(1)
location = pyautogui.locateOnScreen(image_path10, confidence=0.9)
pyautogui.moveTo(pyautogui.center(location))
time.sleep(1)
pyautogui.click(pyautogui.center(location))
time.sleep(1)
#====================================================================================================================================================
keyboard = Controller()
keyboard.release(Key.cmd) 
keyboard.release(Key.shift)  # 手動釋放WIN、Shift 鍵
time.sleep(3)

keyboard.type('shutdown /r /fw /t 0')
keyboard.press(Key.enter)
time.sleep(0.1)
keyboard.release(Key.enter)
time.sleep(1)

while True:  
    # 使用 locateOnScreen 檢測圖片
    time.sleep(1)
    location = pyautogui.locateOnScreen(image_path7, confidence=0.8) 
    if location is not None:
        keyboard.type('shutdown /r /fw /t 0')
        keyboard.press(Key.enter)
        time.sleep(0.1)
        keyboard.release(Key.enter)
        time.sleep(1)
        print('AA')
    else:
        i=0
        print(i)
        i=i=1
        # 如果圖片不存在，跳出循環
        break
    
    # 延遲，避免頻繁檢查導致系統過載
    time.sleep(1)



time.sleep(35)#重開機

keyboard.press(Key.right)
keyboard.release(Key.right)
time.sleep(0.1)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(0.1)
keyboard.press(Key.down)
keyboard.release(Key.down)
time.sleep(0.1)
keyboard.press(Key.enter)
keyboard.release(Key.enter) 
time.sleep(4)#讀取緩衝
keyboard.press(Key.enter)
keyboard.release(Key.enter)  