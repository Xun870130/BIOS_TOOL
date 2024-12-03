import pyautogui
import time
import requests
import ctrl_pwswitch as sw
from pynput.keyboard import Key, Controller
import ctrl_autogui as GCtrl
import res_image

class AutoInstaller:
    """
    Controls the automatic mounting and operation of the Java client.

    Main functionalities include:
    - Opening KVM and AC.
    - Starting the client and performing installation operations on the GUI.
    - Supports automatic mounting of ISO files.

    Attributes:
        ip (str): The IP address of the controlled device.
        iso_path (str): Path to the system image file.
        img_res (ImageResource): Image resource manager for retrieving images required for GUI operations.
        gui_ctrl (ClientController): Controller for GUI actions like clicks and image detection.
        keyboard (Controller): Keyboard controller for simulating keyboard actions.
        ctrl (DeviceController): Device controller for managing hardware switches and status checks.
    """
    def __init__(self, ip: str):
        """
        Initializes the AutoInstaller instance.

        Args:
            ip (str): The IP address of the controlled device.
        """
        self.ip = ip
        self.img_res = res_image.ImageResource()  # Image resource manager for GUI operations
        self.gui_ctrl = GCtrl.ClientController()  # GUI controller
        self.keyboard = Controller()  # Keyboard controller for simulating key presses
        self.ctrl = sw.DeviceController(self.ip)  # Device controller for controlling the device

    def start_installation(self):
        """
        Main installation process:
        Controls the power, checks the status, opens a CMD window, starts the Java client, and performs system restart
        to initiate GUI-based operations.

        This method will:
        - Power on the device.
        - Open the Java client in CMD and restart the system.
        - Perform GUI operations after the restart.
        """
        # Turn on KVM and AC, and check power status
        self.ctrl.kvm_on()
        self.ctrl.ac_on()
        time.sleep(10)
        
        try:
            status = self.ctrl.power_status()
            if "true" in status:
                print("Power is already on")
            else:
                self.ctrl.power_on()
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

        # Open CMD and start the Java client
        self.gui_ctrl.open_cmd()
        self.gui_ctrl.start_client('java', ip=self.ip)
        self.ctrl.reset()  # Restart system
        
        # Perform GUI operations
        self._perform_gui_actions()
        time.sleep(1)
        
        # Handle restart process
        self._handle_restart()

    def _perform_gui_actions(self):
        """
        Performs main GUI operations:
        Locates various UI elements and performs the required actions like clicking, mounting ISO images, and opening CMD.
        """
        dropdown_img = self.img_res.get_image_path("dropdown")
        pin_img = self.img_res.get_image_path("pin9000")
        viewer_img = self.img_res.get_image_path("viewer")

        # Click on images
        time.sleep(2)

        def dropdown():  # Repeatedly click dropdown until the image disappears
            self.gui_ctrl.locate_and_click(1, dropdown_img, confidence=0.9)

        self.gui_ctrl.wait_for_image(dropdown_img, action=dropdown, repeat=True)

        def pin():  # Repeatedly click pin until the image disappears
            self.gui_ctrl.locate_and_click(1, pin_img, confidence=0.8, delay=2)

        self.gui_ctrl.wait_for_image(pin_img, action=pin, repeat=True)

        def click_viewer():  # Repeatedly click viewer until the image disappears
            self.gui_ctrl.locate_and_click(2, viewer_img, confidence=0.8)

        self.gui_ctrl.wait_for_image(viewer_img, action=click_viewer, repeat=True)

        # Wait for the next step screen
        scr_img = self.img_res.get_image_path("scr")
        self.gui_ctrl.wait_for_image(scr_img, timeout=180)

        # Locate and click UI elements to mount the ISO
        windows_img = self.img_res.get_image_path("windows")
        cmd_img = self.img_res.get_image_path("CMD")

        # Perform ISO mounting
        self.gui_ctrl.mount_iso("java")

        # Locate CMD image and perform a double-click
        self.gui_ctrl.locate_and_click(3, windows_img, confidence=0.8, delay=1)
        cmd_location = pyautogui.locateOnScreen(cmd_img, confidence=0.8)
        if cmd_location:
            pyautogui.moveTo(pyautogui.center(cmd_location))
        else:
            pass
        time.sleep(2)
        self.gui_ctrl.locate_and_click(2, cmd_img, confidence=0.8, delay=1)

    def _handle_restart(self):
        """
        Handles system restart and UEFI mounting.

        This method will:
        - Restart the system and wait for a CMD error to appear.
        - After restarting, it will wait for the UEFI screen and perform UEFI operations.
        """
        # Restart system and wait for CMD error to appear
        self.gui_ctrl.restart_system()
        time.sleep(1)

        cmd_err_img = self.img_res.get_image_path("CMDERROR")
        self.gui_ctrl.wait_for_image(cmd_err_img, repeat=True, timeout=20, action=self.gui_ctrl.restart_system)
        
        # Wait for UEFI screen and perform UEFI operation
        uefi_img = self.img_res.get_image_path("UEFI")
        self.gui_ctrl.wait_for_image(uefi_img, action=self.gui_ctrl.UEFI)
