# 新市餐廳 GitHub Pages 生成器

這個專案會把 `restaurent_xinshi.csv` 裡的餐廳資料轉成靜態網站，並放在 `docs/` 資料夾，方便用 GitHub Pages 發佈。

## 使用方式
1. 安裝 Python 3（本機或 CI 環境）。
2. 執行生成腳本：
   ```bash
   python generate_sites.py
   ```
   會更新 `docs/index.html` 以及每間餐廳的介紹頁（位於 `docs/restaurants/`）。
3. 在 GitHub 儲存庫的 Settings → Pages 將來源設為 `Deploy from a branch`，路徑選擇 `docs/`。儲存後就能透過 GitHub Pages 瀏覽所有餐廳頁面。

## 結構說明
- `generate_sites.py`：讀取 CSV、建立 slug、輸出 HTML 的腳本，會自動清理舊的餐廳頁面以避免殘留。
- `docs/assets/style.css`：全站共用樣式。
- `docs/index.html`：首頁格狀卡片列表，每張卡片連到餐廳獨立頁。
- `docs/restaurants/*.html`：每間餐廳的詳細頁，附上評分、價格、類型、地址與 Google 地圖連結。

更新 CSV 後重新執行腳本即可刷新站點內容。
