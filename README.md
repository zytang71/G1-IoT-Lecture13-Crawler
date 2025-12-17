# G1-IoT-Lecture13-Crawler

## Weather crawler
- 路徑：`Weather crawler/`
- 主要檔案：`crawler.py`（下載並解析中央氣象署 F-A0010-001 JSON，寫入 `data.db`）、`app.py`（Streamlit 介面呈現資料庫內容）。
- 快速使用：
  1. 安裝需求：`pip install -r "Weather crawler/requirements.txt"`
  2. 產生資料庫：`python "Weather crawler/crawler.py"`
  3. 啟動介面：`streamlit run "Weather crawler/app.py"`

## Movie crawler
- 路徑：`movie crawler/`
- 主要檔案：`crawler.py`（爬取 https://ssr1.scrape.center/page/1~10，解析電影標題、圖片 URL、評分、類型並輸出 `movie.csv`）
- 快速使用：
  1. 安裝需求：`pip install -r "movie crawler/requirements.txt"`
  2. 執行：`python "movie crawler/crawler.py"`
