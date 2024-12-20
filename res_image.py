import os
import sys

class ImageResource:
    def __init__(self):
        """初始化 ImageResource 類別，設置當前目錄及圖片路徑字典。"""
        if hasattr(sys, '_MEIPASS'):
            # 如果在 PyInstaller 打包后的環境中，使用 _MEIPASS 獲取路徑
            self.current_directory = sys._MEIPASS
        else:
            # 否則，使用標準的當前工作目錄
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
            "fast_boot": "UI_image/fast_boot_disable.jpg",
            "fast_boot_enable": "UI_image/fast_boot_disable2.jpg",
            "usb_device": "UI_image/usb_device.jpg",
            "boot_manager": "UI_image/boot_manager.jpg",
            "press_enter": "UI_image/press_enter.jpg"
        }

    def get_image_path(self, image_name: str) -> str:
        """
        返回指定圖片的絕對路徑。

        根據給定的圖片名稱，返回對應的絕對路徑。若圖片名稱無效，則引發 ValueError。

        Args:
            image_name (str): 圖片名稱的鍵，例如 "dropdown" 或 "pin9000"。

        Returns:
            str: 圖片的絕對路徑。

        Raises:
            ValueError: 如果給定的圖片鍵不存在於 image_paths 中。
        """
        relative_path = self.image_paths.get(image_name)
        if relative_path:
            return os.path.join(self.current_directory, relative_path)
        else:
            print(f"No image found for key: {image_name}")
            raise ValueError(f"No image found for key: {image_name}")
