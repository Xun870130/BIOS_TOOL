import time
import requests
import ASCIIART

# 初始化 ASCII 字符藝術文本
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
    """負責管理設備控制命令的類，通過 HTTP API 發送指令控制設備開關"""
    def __init__(self, IP_adr: str):
        self.IP_adr = IP_adr  # 設備 IP 地址
        # 設置 API 端點 URL
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

    def send_request(self, endpoint_key: str, ascii_art: str) -> (str | None):
        """
        發送 HTTP GET 請求到指定的端點
        endpoint_key: 要調用的端點鍵
        ascii_art: 要顯示的 ASCII 藝術文本
        """
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

    def reset(self) -> (str | None):
        """
        執行PC重開機
        """
        try:
            response = requests.get(self.endpoints["reset"])
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(ERROR, e)
            return None

    def power_status(self) -> (str | None):
        """
        查詢電源狀態
        """
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
        """
        執行 CMOS 放電
        """
        self.cmos_on()
        time.sleep(5)
        self.cmos_off()

    def ACoffcheck(self):
        """
        檢查並關閉 AC 電源
        """
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
        """
        檢查並開啟 AC 電源
        """
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
    
# 示例:
# ctrl = DeviceController("http://192.168.0.211:16628")
# ctrl.power_status()