# 酸種麵包科學 Wiki / Sourdough Science Wiki

**專案狀態：兩批 Wiki 知識庫已核准（7 份來源、8 篇文章、6 大主題）**。[Wiki 文章索引](wiki/index.md) · [第二批獨立審查](wiki/review/batch-2-independent.md) · [第二批 Lint 輸出](reports/batch-2-validation.txt)

## 使用方式（VS Code + Codex）
1. 解壓 ZIP，以 VS Code 開啟 `sourdough-science-wiki/`；先讓 Codex 讀 `AGENTS.md` 與 `interview.md`。
2. 第一批請 Codex 查原文 SRC-001 和 SRC-004；確認元資料及授權、將中文摘要寫入 `raw/`、文章寫入 `wiki/articles/`，更新 `sources.json`、`wiki/index.md`、`wiki/log.md`、審查檔。
3. 執行 `python scripts/lint_wiki.py` 和 `python scripts/lint_wiki.py --min-approved-sources 2`；後者須在真正核准兩份來源後才通過。保留終端機結果在 `reports/`。
4. 第一批合格後，進行剩下 SRC-002、003、005、006、007，最後 `python scripts/lint_wiki.py --strict`。
5. 來源全過、六主題齊全後，才執行 `python scripts/build_wiki_site.py` 建立一頁式 `docs/index.html`。確認可在本機瀏覽，再 GitHub Pages 部署。
6. 簡報另建 `docs/slides/index.html`，內容只用核准 Wiki；紀錄投影片與來源對應及獨立驗證；Word 報告展示真實錯誤與修改。

## 安全與品質
- 來源的匯入與查核狀態以 `sources.json` 為準。作者或年份須依原文核實。
- 僅公開有重製權的材料；摘要用自己的文字撰寫。不要上傳商用版權全文或密碼/金鑰。
- 寫到食品安全、發黴與衛生時，遇到來源歧見先停止該主張並請人工確認。

## 專案資料夾
- `AGENTS.md`：Coding Agent 工作規則
- `interview.md`：多輪需求確認原始摘要
- `sources.json`：7 篇來源清單與查核狀態
- `raw/`：合法保存的來源摘要
- `wiki/articles/`：正式 Wiki 條目
- `wiki/review/`：獨立 AI 審查紀錄
- `wiki/log.md`：執行與錯誤重試日誌
- `scripts/lint_wiki.py`：離線格式／引用／覆蓋檢查
- `scripts/build_wiki_site.py`：從已核准條目生成一頁網站
- `reports/`：檢查輸出、簡報來源對照
- `docs/`：GitHub Pages 發布位置（完成後產生首頁）

## GitHub Pages
網站完成後在 Repository Settings > Pages 中選 `Deploy from a branch`、`main`、`/docs`。`docs/` 初期沒有 index.html，這是刻意設計；不要在資料仍未驗證時發布空白假網站。
