# 自動化裝置控制與安裝腳本

此專案提供了一套自動化控制與安裝系統，主要用於透過 KVM、BIOS 燒錄和 ISO 檔掛載完成系統的自動化操作與安裝。適合在 Windows 或 Java 環境中執行自動安裝程序。

## 專案結構

```plaintext
.
├── java/                   # Java 客戶端相關資源
├── UI_image/               # 用於 GUI 操作的圖像資源
├── res_ASCIIart.py             # ASCII 藝術字生成器
├── ctrl_dediprog.py         # DediProg BIOS 燒錄控制
├── ctrl_autogui.py             # 圖形界面控制腳本
├── res_image.py        # 管理 UI 圖像資源
├── JavaClient.jar          # Java 客戶端 JAR 檔案
├── client_java.py           # Java 客戶端自動安裝控制
├── client_windows.py        # Windows 客戶端自動安裝控制
├── main.py                 # 主程序，用於啟動控制與安裝流程
├── ctrl_pwswitch.py             # 電源開關與設備控制
├── requirements.txt
└── README.md              
```
安裝指引
1. 建立虛擬環境 (py-env)
```bash
python -m venv py-env
```
2. 啟動虛擬環境
Windows:
```bash
py-env\Scripts\activate
```
```bash
source py-env/bin/activate
```
3. 安裝相依套件
在虛擬環境中安裝專案所需的 Python 相依套件：

```bash
pip install -r requirements.txt
```
備註: requirements.txt 文件中應包含以下主要相依套件：

pyautogui
requests
pynput
使用說明
啟動程式
透過以下命令執行主程序 main.py，並依需求提供 IP 和 type 參數：

```bash
python main.py <IP> <type>
```
IP (必填): 選擇設備的控制 IP 地址，支援以下選項：

192.168.0.213
192.168.0.211
type (必填): 指定安裝類型，支援以下選項：

win (Windows 安裝流程)
java (Java 環境安裝流程)
範例：
```bash
python main.py 192.168.0.211 java
```
程序流程
執行 main.py 後，程序將自動完成以下步驟：

- 檢查 AC 電源狀態。
- 啟動 DP (DisplayPort) 模組。
- 執行 BIOS 燒錄：
- 根據 IP 地址選擇對應的 BIOS 映像檔。
- 使用 DediProg BIOS 燒錄工具。
- 關閉 DP 模組。
- 重置 CMOS。
- 開啟 AC 電源。
啟動對應類型的安裝程序：
- Windows: 使用 client_windows.py 啟動安裝。
- Java: 使用 client_java.py 啟動安裝。
程序完成提示。
模組說明
主模組 (main.py)
統籌整個自動化流程，根據命令列參數初始化控制模組與安裝程序。

電源控制模組 (ctrl_pwswitch.py)
提供對以下設備的電源控制功能：

- AC 電源
- DisplayPort 模組
- CMOS 重置
- BIOS 燒錄模組 (ctrl_dediprog.py)
- 透過 DediProg 工具控制 BIOS 燒錄過程，包括芯片檢測與 BIOS 映像檔寫入。

ASCII 輸出模組 (res_ASCIIart.py)
- 生成 ASCII 藝術字作為系統提示訊息，提升操作可讀性。

安裝程序模組
- client_windows.py: Windows 環境的安裝流程自動化。
- client_java.py: Java 環境的安裝流程自動化。
