# 自動化裝置控制與安裝腳本

此專案提供了一套自動化控制與安裝系統，主要用於透過 KVM、BIOS 燒錄和 ISO 檔掛載完成系統的自動化操作與安裝。適合在 Windows 或 Java 環境中執行自動安裝程序。

## 專案結構

```plaintext
.
├── BIOS/                   # BIOS 映像檔案資料夾
├── java/                   # Java 客戶端相關資源
├── py-env/                 # 虛擬環境資料夾
├── UI_image/               # 用於 GUI 操作的圖像資源
├── ASCIIART.py             # ASCII 藝術字生成器
├── DediProg_CMD.py         # DediProg BIOS 燒錄控制
├── GUI_Ctrl.py             # 圖形界面控制腳本
├── ImageResource.py        # 管理 UI 圖像資源
├── JavaClient.jar          # Java 客戶端 JAR 檔案
├── JavaClient.py           # Java 客戶端自動安裝控制
├── WindowsClient.py        # Windows 客戶端自動安裝控制
├── main.py                 # 主程序，用於啟動控制與安裝流程
├── powerSW2.py             # 電源開關與設備控制
└── README.md               # 專案說明文件
```
安裝指引
1. 建立虛擬環境 (py-env)

```bash
python -m venv py-env
```

2. 啟動虛擬環境
Windows:
```bash
複製程式碼
py-env\Scripts\activate
```
macOS / Linux:
```bash
source py-env/bin/activate
```
3. 安裝相依套件
在虛擬環境中安裝相依的 Python 套件：

```bash
pip install -r requirements.txt
```
備註: requirements.txt 文件中應包含 pyautogui, requests, pynput 等相依套件。

4. 設定 BIOS 映像
將 BIOS 檔案 (例如 IceLake_U_3.bin) 放置於 BIOS 資料夾中，並在 main.py 中指定正確的 BIOS 檔案名稱。

5. 設定 KVM 控制 IP
修改 main.py 中的裝置 IP 位址來匹配您的設備環境。預設 IP 為 http://192.168.0.211:16628。

使用說明
啟動 main.py 主程序會執行以下操作:

檢查 AC 和電源狀態並啟動設備。
BIOS 燒錄控制：使用 DediProg 控制器進行 BIOS 燒錄。
GUI 自動化操作：透過 GUI 控制掛載 ISO 檔案，並自動進行安裝流程。
支援 Windows 與 Java 環境的安裝流程。
```bash
python main.py
```
## 模組說明
ASCIIART.py
提供 ASCII 藝術字生成器，用於系統訊息的 ASCII 輸出。

DediProg_CMD.py
管理 DediProg BIOS 燒錄命令，包含芯片檢測與燒錄操作。

GUI_Ctrl.py
負責 GUI 的自動點擊控制，包含圖像匹配與 UI 點擊操作。

ImageResource.py
管理 UI 圖像資源的檔案路徑，用於 GUI 自動操作的圖像檢測。

JavaClient.py
Java 環境的自動安裝控制腳本，包括 ISO 掛載、KVM 開關與系統重啟。

WindowsClient.py
Windows 環境的自動安裝控制腳本，與 JavaClient 類似，用於控制 Windows 客戶端的安裝。

main.py
主程序，整合各模組並執行設備控制與自動安裝流程。

powerSW2.py
電源開關控制模組，提供 KVM、AC、DP 等多種開關控制，以及 CMOS 重置功能。

注意事項
確保您的設備網路連線正常，並設定正確的 IP 地址來控制裝置。
建議在操作之前確認所有硬體連接良好，包括 KVM、BIOS 燒錄器等。
圖像檢測與點擊基於 pyautogui 和 pynput，操作環境需與 GUI 資源相容。
聯絡方式
如有任何問題或建議，請聯絡專案維護者。
