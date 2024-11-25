import os
import sys

class ImageResource:
    def __init__(self):
        if hasattr(sys, '_MEIPASS'):
            # 如果在 PyInstaller 打包后的环境中，使用 _MEIPASS 获取路径
            self.current_directory = sys._MEIPASS
        else:
            # 否则，使用标准的当前工作目录
            self.current_directory = os.getcwd()
        self.image_paths = {
            "dropdown": "UI_image/dropdown.png",
            "pin9000": "UI_image/pin9000.png",
            "viewer": "UI_image/viewer.jpg",
            "VM9000": "UI_image/VM9000.png",
            "add": "UI_image/add.jpg",
            "isofile": "UI_image/isofile.jpg",
            "CMDERROR": "UI_image/CMDERROR.jpg",
            "mount": "UI_image/mount.jpg",
            "windows": "UI_image/windows.jpg",
            "CMD": "UI_image/CMD.jpg",
            "wadd": "UI_image/Wadd.jpg",
            "wiso": "UI_image/Wisofile.jpg",
            "UEFI": "UI_image/UEFI.jpg",
            "scr": "UI_image/Screem.jpg",
            "wmount": "UI_image/Wmount.jpg",
            "boot_failed": "UI_image/boot_failed.jpg",
            "esc": "UI_image/esc.png",
            "fast_boot_disable": "UI_image/fast_boot_disable.jpg",
            "usb_device": "UI_image/usb_device.jpg",
            "boot_manager": "UI_image/boot_manager.jpg"
        }

    def  get_image_path(self, image_name: str) -> str:
        """
        返回指定圖片的絕對路徑。
        
        :param image_name: 圖片名稱的鍵，例如 "dropdown" 或 "pin9000"。
        :return: 圖片的絕對路徑。
        :raises ValueError: 如果給定的圖片鍵不存在於 image_paths 中。
        """
        relative_path = self.image_paths.get(image_name)
        if relative_path:
            return os.path.join(self.current_directory, relative_path)
        else:
            print(f"No image found for key: {image_name}")
            raise ValueError(f"No image found for key: {image_name}")
