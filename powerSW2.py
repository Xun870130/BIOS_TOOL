#
#power switch 所有跟電源切換有關的控制函數
#



import time
import requests
import ASCIIART

text=ASCIIART.ASCIIArtBuilder()
ACSOFF = text.build("ac","off")
ACSON = text.build("ac","on")
DPSON = text.build("dp","on")
DPSOFF = text.build("dp","off")
cmosOn = text.build("cmos","on")
cmosOff = text.build("cmos","off")
pcson = text.build("power","on")
pcsoff = text.build("power","off")
kvmson = text.build("kvm","on")
Turn_off_failed = text.call("Turn_off_failed")
ERROR = text.call("error")

class DeviceController:
    def __init__(self, IP_adr):
        self.IP_adr = IP_adr
        self.endpoints = {
            "pc_off": f"{self.IP_adr}/arduino/gpio?func=power_click&act=off",
            "pc_on": f"{self.IP_adr}/arduino/gpio?func=power_click&act=on",
            "ac_on": f"{self.IP_adr}/arduino/gpio?func=ac&act=on",
            "ac_off": f"{self.IP_adr}/arduino/gpio?func=ac&act=off",
            "dp_on": f"{self.IP_adr}/arduino/gpio?func=dediprog&act=on",
            "dp_off": f"{self.IP_adr}/arduino/gpio?func=dediprog&act=off",
            "p_status": f"{self.IP_adr}/arduino/gpio?func=state",
            "cmos_on": f"{self.IP_adr}/arduino/gpio?func=clear_cmos&act=on",
            "cmos_off": f"{self.IP_adr}/arduino/gpio?func=clear_cmos&act=off",
            "kvm_on": f"{self.IP_adr}/arduino/gpio?func=kvm&act=on",
            "reset": f"{self.IP_adr}/arduino/gpio?func=reset"
            }   

    def send_request(self, endpoint_key, ascii_art):
        try:
            url = self.endpoints[endpoint_key]
            response = requests.get(url)
            response.raise_for_status()
            print(ascii_art, response.text)
            return response.text
        except requests.exceptions.RequestException as e:
            print(ERROR, e)
    
    def kvm_on(self):
        self.send_request("kvm_on",kvmson)

    def ac_off(self):
        self.send_request("ac_off", ACSOFF)

    def ac_on(self):
        self.send_request("ac_on", ACSON)

    def dp_off(self):
        self.send_request("dp_off", DPSOFF)

    def dp_on(self):
        self.send_request("dp_on", DPSON)

    def reset(self):
        try:
            response = requests.get(self.endpoints["reset"])
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(ERROR, e)
            return None

    def power_status(self):
        try:
            response = requests.get(self.endpoints["p_status"])
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(ERROR, e)
            return None

    def power_off(self):
        self.send_request("pc_off", pcsoff)

    def power_on(self):
        self.send_request("pc_on",pcson)

    def cmos_on(self):
        self.send_request("cmos_on", cmosOn)

    def cmos_off(self):
        self.send_request("cmos_off", cmosOff)

    def cmos_switch(self):
        self.cmos_on()
        time.sleep(5)
        self.cmos_off()

    def ACoffcheck(self):
        try:
            ps = self.power_status()  # 檢查電源狀態
            if "true" in ps:
                self.power_off()
                time.sleep(10)
                self.ac_off()
                time.sleep(10)
            else:
                print(ACSOFF)  # 電源已經關閉
        except requests.exceptions.RequestException as e:
            print(ERROR, e)
        return

    def AConcheck(self):
        try:
            # 關閉 DP    
            dp_status = self.send_request("dp_off",DPSOFF)
            time.sleep(10)  # 等待 DP 關閉

            if "true" in dp_status:  # 檢查 DP 是否已經成功關閉
                print(DPSOFF)
                self.ac_on()  # 如果 DP 成功關閉，開啟 AC
            else:
                print(Turn_off_failed)
                exit()  # 結束程序
        except requests.exceptions.RequestException as e:
            print(ERROR, e)
        return
    
""" 
ctrl=DeviceController("http://192.168.0.211:16628")
ctrl.power_status()
"""