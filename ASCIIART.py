
#文字粗體化，單純字太小不好Debug

class ASCIIArtBuilder:
    def __init__(self):
        self.device_name = {
            "dp": r""" 
 ____  ____   
|  _ \|  _ \  
| | | | |_) | 
| |_| |  __/  
|____/|_|     """,
            "ac": r"""
    _    ____  
   / \  / ___| 
  / _ \| |     
 / ___ \ |___  
/_/   \_\____| """,
            "cmos": r"""
  ____ __  __  ___  ____   
 / ___|  \/  |/ _ \/ ___|  
| |   | |\/| | | | \___ \  
| |___| |  | | |_| |___) | 
 \____|_|  |_|\___/|____/  """,
             "kvm": r"""
 _  ____     ____  __  
| |/ /\ \   / /  \/  | 
| ' /  \ \ / /| |\/| | 
| . \   \ V / | |  | | 
|_|\_\   \_/  |_|  |_| """,
            "power": r"""
 ____   ____  
|  _ \ / ___| 
| |_) | |     
|  __/| |___  
|_|    \____| """
            }
        self.status_name = r"""
     _        _              
 ___| |_ __ _| |_ _   _ ___  
/ __| __/ _` | __| | | / __| 
\__ \ || (_| | |_| |_| \__ \ 
|___/\__\__,_|\__|\__,_|___/ """
        self.operator = r"""
     __   
 ____\ \  
|_____\ \ 
|_____/ / 
     /_/  """
        self.state = {
            "on": r"""
  ___  _   _ 
 / _ \| \ | |
| | | |  \| |
| |_| | |\  |
 \___/|_| \_|""",
             "off": r"""
  ___  _____ _____ 
 / _ \|  ___|  ___|
| | | | |_  | |_   
| |_| |  _| |  _|  
 \___/|_|   |_|    """
            }
        self.Else = {
            "error": r"""
░▒▓████████▓▒░ ░▒▓███████▓▒░  ░▒▓███████▓▒░   ░▒▓██████▓▒░  ░▒▓███████▓▒░  
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░   ░▒▓███████▓▒░  ░▒▓███████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓████████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓██████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░ """,

            "programing": r"""
 ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ 
||P |||r |||o |||g |||r |||a |||m |||i |||n |||g ||
||__|||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|""",
            "success": r"""
░░      ░░░  ░░░░  ░░░      ░░░░      ░░░        ░░░      ░░░░      ░░
▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒
▓▓      ▓▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓      ▓▓▓▓▓      ▓▓▓▓      ▓▓
███████  ██  ████  ██  ████  ██  ████  ██  ██████████████  ████████  █
██      ████      ████      ████      ███        ███      ████      ██""",
            "Turn_off_failed": r"""
 _____                          __  __    __       _ _          _ 
|_   _|   _ _ __ _ __     ___  / _|/ _|  / _| __ _(_) | ___  __| |
  | || | | | '__| '_ \   / _ \| |_| |_  | |_ / _` | | |/ _ \/ _` |
  | || |_| | |  | | | | | (_) |  _|  _| |  _| (_| | | |  __/ (_| |
  |_| \__,_|_|  |_| |_|  \___/|_| |_|   |_|  \__,_|_|_|\___|\__,_|"""

        }
    def call (self,text):
        # 返回指定文本的 ASCII ART    
        return self.Else.get(text, "not found")


    def build(self, device, state):
        """
        將設備名稱、狀態名稱、操作符和開關狀態組合在一起，按行組合並返回。

        :param device: 設備名稱鍵 (如 "dp" 或 "power")
        :param state: 狀態名稱鍵 (如 "on" 或 "off")
        :return: ASCII ART 字串
        """
        # 獲取設備和狀態的 ASCII ART，按行拆分
        device_art_lines = self.device_name.get(device.lower(), "unknow").splitlines()
        status_art_lines = self.status_name.splitlines()
        operator_art_lines = self.operator.splitlines()
        state_art_lines = self.state.get(state.lower(), "unknow").splitlines()

        # 將各部分按行組合，並且不換行顯示
        combined_art = []
        for i in range(len(device_art_lines)):
            combined_art.append(
                device_art_lines[i] +  # 設備名稱部分
                status_art_lines[i] +  # 狀態名稱部分
                operator_art_lines[i]+  # 操作符部分
                state_art_lines[i]  # 狀態部分
            )
        # 最終組合成一個單行顯示的字串
        return "\n".join(combined_art)

# 示例:
# A=ASCIIArtBuilder()
# ZZ=A.build("power","on")
# print(ZZ)