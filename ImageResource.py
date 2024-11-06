import os

class ImageResource:
    def __init__(self):
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
            "wiso": "UI_image/Wiosfile.jpg",
            "UEFI": "UI_image/UEFI.jpg",
            "scr": "UI_image/Screem.jpg",
            "wmount": "UI_image/Wmount.jpg"
        }

    def get_image_path(self, image_name):
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
            raise ValueError(f"No image found for key: {image_name}")
