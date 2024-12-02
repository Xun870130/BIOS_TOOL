import time
import requests
import BIOS_OS.res_ASCIIart as res_ASCIIart

# 初始化 ASCII 字符藝術文本
text = res_ASCIIart.ASCIIArtBuilder()
ACSOFF = text.build("ac", "off")
ACSON = text.build("ac", "on")
DPSON = text.build("dp", "on")
DPSOFF = text.build("dp", "off")
cmosOn = text.build("cmos", "on")
cmosOff = text.build("cmos", "off")
pcson = text.build("power", "on")
pcsoff = text.build("power", "off")
kvmson = text.build("kvm", "on")
Turn_off_failed = text.call("Turn_off_failed")
ERROR = text.call("error")


class DeviceController:
    """
    A class to manage device control commands via HTTP API.

    Attributes:
        IP_adr (str): The IP address of the device.
        endpoints (dict): A dictionary of API endpoints for different device commands.
    """

    def __init__(self, IP_adr: str):
        """
        Initializes DeviceController with a specified IP address.

        Args:
            IP_adr (str): The IP address of the device.
        """
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

    def send_request(self, endpoint_key: str, ascii_art: str) -> (str | None):
        """
        Sends an HTTP GET request to a specified endpoint.

        Args:
            endpoint_key (str): The key of the endpoint in the `endpoints` dictionary.
            ascii_art (str): ASCII art text to display.

        Returns:
            str | None: The response text from the API, or None if the request fails.
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
        """Turns on the KVM switch."""
        self.send_request("kvm_on", kvmson)

    def ac_off(self):
        """Turns off the AC power."""
        self.send_request("ac_off", ACSOFF)

    def ac_on(self):
        """Turns on the AC power."""
        self.send_request("ac_on", ACSON)

    def dp_off(self):
        """Turns off the DediProg."""
        self.send_request("dp_off", DPSOFF)

    def dp_on(self):
        """Turns on the DediProg."""
        self.send_request("dp_on", DPSON)

    def reset(self) -> (str | None):
        """
        Performs a PC reset.

        Returns:
            str | None: The response text from the API, or None if the request fails.
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
        Queries the power status.

        Returns:
            str | None: The power status as a string, or None if the request fails.
        """
        try:
            response = requests.get(self.endpoints["p_status"])
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(ERROR, e)
            return None

    def power_off(self):
        """Turns off the PC power."""
        self.send_request("pc_off", pcsoff)

    def power_on(self):
        """Turns on the PC power."""
        self.send_request("pc_on", pcson)

    def cmos_on(self):
        """Turns on the CMOS switch."""
        self.send_request("cmos_on", cmosOn)

    def cmos_off(self):
        """Turns off the CMOS switch."""
        self.send_request("cmos_off", cmosOff)

    def cmos_switch(self):
        """
        Performs CMOS discharge by turning it on and then off.
        """
        self.cmos_on()
        time.sleep(5)
        self.cmos_off()

    def ACoffcheck(self):
        """
        Checks and turns off the AC power if necessary.

        Ensures the PC power is off before turning off the AC.
        """
        try:
            ps = self.power_status()
            if "true" in ps:
                self.power_off()
                time.sleep(10)
                self.ac_off()
                time.sleep(10)
            else:
                print(ACSOFF)
        except requests.exceptions.RequestException as e:
            print(ERROR, e)

    def AConcheck(self):
        """
        Checks and turns on the AC power if necessary.

        Ensures the DediProg is off before turning on the AC.
        """
        try:
            dp_status = self.send_request("dp_off", DPSOFF)
            time.sleep(10)
            if "true" in dp_status:
                print(DPSOFF)
                self.ac_on()
            else:
                print(Turn_off_failed)
                exit()
        except requests.exceptions.RequestException as e:
            print(ERROR, e)

# 示例:
# ctrl = DeviceController("http://192.168.0.211:16628")
# ctrl.power_status()
