# Loop / Graph 說明

可用 VS Code Mermaid 預覽 `graph.mmd`，或將內容放到 Mermaid 編輯器。

- 每筆文章失敗只退回最小有問題節點，最多自動修正三輪。
- `lint_wiki.py` 只能驗證結構、來源與引用，**不能**推論論文內容是否正確。
- 涉及食品安全衝突停止自動處理，不記作自動修正成功。
- 每個節點的真實輸出記在 `wiki/log.md` 與 `reports/`；圖是設計，不能假稱已執行。
