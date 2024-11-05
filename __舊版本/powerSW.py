import time
import requests
pc_off = "http://192.168.0.211:16628/arduino/gpio?func=power_click&act=off"
ac_on = "http://192.168.0.211:16628/arduino/gpio?func=ac&act=on" # AC on
ac_off = "http://192.168.0.211:16628/arduino/gpio?func=ac&act=off" # AC off
dp_on = "http://192.168.0.211:16628/arduino/gpio?func=dediprog&act=on" # DP on 
dp_off = "http://192.168.0.211:16628/arduino/gpio?func=dediprog&act=off" # DP off
p_statu = "http://192.168.0.211:16628/arduino/gpio?func=state" # power status
cmos_on = "http://192.168.0.211:16628/arduino/gpio?func=clear_cmos&act=on" # 放電
cmos_off = "http://192.168.0.211:16628/arduino/gpio?func=clear_cmos&act=off"
ACSOFF = r"""   
    _    ____       _        _                   __     ___  _____ _____  
   / \  / ___|  ___| |_ __ _| |_ _   _ ___   ____\ \   / _ \|  ___|  ___|
  / _ \| |     / __| __/ _` | __| | | / __| |_____\ \ | | | | |_  | |_   
 / ___ \ |___  \__ \ || (_| | |_| |_| \__ \ |_____/ / | |_| |  _| |  _|  
/_/   \_\____| |___/\__\__,_|\__|\__,_|___/      /_/   \___/|_|   |_|    
"""


ACSON = r""" 
    _    ____       _        _                   __     ___  _   _ 
   / \  / ___|  ___| |_ __ _| |_ _   _ ___   ____\ \   / _ \| \ | |
  / _ \| |     / __| __/ _` | __| | | / __| |_____\ \ | | | |  \| |
 / ___ \ |___  \__ \ || (_| | |_| |_| \__ \ |_____/ / | |_| | |\  |
/_/   \_\____| |___/\__\__,_|\__|\__,_|___/      /_/   \___/|_| \_|
"""

DPSON = r""" 
 ____  ____        _        _                   __     ___  _   _ 
|  _ \|  _ \   ___| |_ __ _| |_ _   _ ___   ____\ \   / _ \| \ | |
| | | | |_) | / __| __/ _` | __| | | / __| |_____\ \ | | | |  \| |
| |_| |  __/  \__ \ || (_| | |_| |_| \__ \ |_____/ / | |_| | |\  |
|____/|_|     |___/\__\__,_|\__|\__,_|___/      /_/   \___/|_| \_|
"""

DPSOFF = r""" 
 ____  ____        _        _                   __     ___  _____ _____ 
|  _ \|  _ \   ___| |_ __ _| |_ _   _ ___   ____\ \   / _ \|  ___|  ___|
| | | | |_) | / __| __/ _` | __| | | / __| |_____\ \ | | | | |_  | |_   
| |_| |  __/  \__ \ || (_| | |_| |_| \__ \ |_____/ / | |_| |  _| |  _|  
|____/|_|     |___/\__\__,_|\__|\__,_|___/      /_/   \___/|_|   |_|    
"""

Turn_off_failed = r""" 
 _____                          __  __    __       _ _          _ 
|_   _|   _ _ __ _ __     ___  / _|/ _|  / _| __ _(_) | ___  __| |
  | || | | | '__| '_ \   / _ \| |_| |_  | |_ / _` | | |/ _ \/ _` |
  | || |_| | |  | | | | | (_) |  _|  _| |  _| (_| | | |  __/ (_| |
  |_| \__,_|_|  |_| |_|  \___/|_| |_|   |_|  \__,_|_|_|\___|\__,_|
"""

cmosOn = r"""
  ____ __  __  ___  ____        __     ___  _   _ 
 / ___|  \/  |/ _ \/ ___|   ____\ \   / _ \| \ | |
| |   | |\/| | | | \___ \  |_____\ \ | | | |  \| |
| |___| |  | | |_| |___) | |_____/ / | |_| | |\  |
 \____|_|  |_|\___/|____/       /_/   \___/|_| \_|
                                                   
"""

cmosOff = r"""
  ____ __  __  ___  ____        __     ___  _____ _____ 
 / ___|  \/  |/ _ \/ ___|   ____\ \   / _ \|  ___|  ___|
| |   | |\/| | | | \___ \  |_____\ \ | | | | |_  | |_   
| |___| |  | | |_| |___) | |_____/ / | |_| |  _| |  _|  
 \____|_|  |_|\___/|____/       /_/   \___/|_|   |_|    
                                                   
"""

ERROR = """
░▒▓████████▓▒░ ░▒▓███████▓▒░  ░▒▓███████▓▒░   ░▒▓██████▓▒░  ░▒▓███████▓▒░  
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░   ░▒▓███████▓▒░  ░▒▓███████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓████████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓██████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ """
def ACoffcheck():
    try:
        response = requests.get(p_statu) # 檢查 power status 狀態
        response.raise_for_status()  # 確保請求成功
        time.sleep(1)
        if "true" in response.text:
            response = requests.get(pc_off)
            response.raise_for_status()
            time.sleep(10)
            response = requests.get(ac_off)        
            response.raise_for_status()
            time.sleep(10)
            print(ACSOFF, response.text)
        else:
            print(ACSOFF, response.text)
    except requests.exceptions.RequestException as e:
        print(ERROR, e)
    return

def AConcheck():
    try:
        response = requests.get(dp_off)
        response.raise_for_status()
        time.sleep(10) # 等待DP關閉
        if "true" in response.text:
            print(DPSOFF,response.text)
            response = requests.get(ac_on) # 開啟電源
            response.raise_for_status()
            print(ACSON,response.text)
        else:
            print(Turn_off_failed)
            exit()
    except requests.exceptions.RequestException as e:
        print(ERROR, e)
    return

def DPoff():
    try:
        response = requests.get(dp_off)
        response.raise_for_status()
        time.sleep(10) # 等待DP關閉
        print(DPSOFF,response.text)
    except requests.exceptions.RequestException as e:
        print(ERROR, e)
    return

def DPon():
    try:
        response = requests.get(dp_on)
        response.raise_for_status()
        time.sleep(10) # 等待DP
        print(DPSON,response.text)
    except requests.exceptions.RequestException as e:
        print(ERROR, e)
    return

def CMOSon():
    try:
        response = requests.get(cmos_on)
        response.raise_for_status()
        print(cmosOn,response.text)
    except requests.exceptions.RequestException as e:
        print(ERROR, e)
    return

def CMOSoff():
    try:
        response = requests.get(cmos_off)
        response.raise_for_status()
        print(cmosOff,response.text)
    except requests.exceptions.RequestException as e:
        print(ERROR, e)
    return

def COMSswitch():
    CMOSon()
    time.sleep(5)
    CMOSoff()