# 第一批獨立 AI 審查

- 審查者為處理此批次的獨立 AI，未參與原始摘要與條目撰寫。自行開啟來源全文，對照草稿、摘要與書目。
- 初審時間為 2026-11-22 19:51–19:52（臺灣時間），審查版本為待核准草稿。以下頁碼為 PDF 內印刷頁碼。
- SRC-001 出版者 PDF 直接開啟時回傳 403。從搜索索引重開同一 PDF 已取得全文，並核對哥本哈根大學保存的正式出版版本，兩者 DOI、書目和相關章節一致。[PeerJ 全文](https://peerj.com/articles/11389.pdf) · [大學典藏版本](https://curis.ku.dk/ws/portalfiles/portal/279255725/A_review_of_sourdough_starters.pdf)
- SRC-004 直接開啟 CSU Extension 網頁並查閱正文與書目。[CSU Extension 全文](https://extension.colostate.edu/resource/sourdough-basics-caring-for-your-starter-and-making-bread/)

## 初審

| 草稿 | 結果 | 原文核對 | 退回節點與初審重試次數 |
|---|---|---|---|
| W001 | fail | Background 第 3–4 頁支持麵粉、水與菌群變化，及酸鹼值、膨脹和菌群穩定的觀察。圖 1 在第 5 頁。Organic acids produced by bacteria 第 8–9 頁與 Yeast 第 10 頁支持產酸、風味及產氣膨發。科學正確性和基本可讀性均為 pass。來源欄缺原題，對照首頁與 PMC 授權聲明須補書目。 | drafting，0 |
| W002 | fail | Flour 第 13–14 頁、Hydration 第 14–15 頁支持養分、微生物來源、含水量與偏稠酸種中乳酸菌的觀察。Temperature 第 15–16 頁、Time 第 16–18 頁與圖 3 第 17–18 頁支持溫度、餵養間隔及假說的區分。Defining traditional sourdough methods 第 23–24 頁及 Conclusions 第 24 頁支持因果限制。科學正確性和可讀性均為 pass。來源欄缺原題。 | drafting，0 |
| W003 | pass | Maintaining the Starter 步驟 1–6 支持 1–2 小時回溫、各半杯舊酸種與水、¾–1 杯麵粉、蛋白質 11–13%、約 5–8 小時及回落後冷藏的順序。每週餵養限於指南的冷藏流程。Making Sourdough Bread 的酵頭步驟支持另餵之後漲至兩倍時使用。可把取出的酸種稱為酵頭的材料，使兩篇用語一致。 | none，0 |
| W004 | fail | Making Sourdough Bread 的酵頭、揉麵、發酵及整形小節支持份量、兩段約 2–3 小時、分成兩個與海拔影響。Bake 步驟 1、3–5 支持有蓋鑄鐵鍋的 450 °F、35–45 分鐘及中心 190 °F。攝氏換算約為 232 °C、88 °C。應補預熱約在發酵完畢前 20–30 分鐘開始、未達熟度時繼續烤、出爐亦戴隔熱手套的動作。Mix 步驟 4–5 的加粉量與抹油可納入操作，幫助新手備料和判斷。 | drafting，0 |

### 書目、權利與衝突

- SRC-001 的作者、題名、2021-05-10、PeerJ 9:e11389、DOI 及 CC BY 4.0 核對為 pass。摘要的原文定位有三處退回 evidence，重試次數為 0。圖 1 應定位第 5 頁，圖 3 延伸到第 18 頁，Defining traditional sourdough methods 從第 23 頁開始。圖 1 有第三方權利標記。本批只採正文事實、書目與證據位置。[PeerJ 全文](https://peerj.com/articles/11389.pdf) · [PMC 書目與授權](https://pmc.ncbi.nlm.nih.gov/articles/PMC8117929/)
- SRC-004 的題名、署名和 2025 年 10 月審閱日期核對為 pass。指南頁面未顯示開放授權。摘要採用以自己的文字整理的事實及位置，未見正文段落、圖表或長篇翻譯的重製。[CSU Extension 全文](https://extension.colostate.edu/resource/sourdough-basics-caring-for-your-starter-and-making-bread/) · [CSU 著作權指引](https://marcomm.colostate.edu/copyright-guidelines/)
- 來源 ID、網址與可見 DOI 無重複。草稿皆具必要欄位與逐段來源 ID。兩份來源的取材範圍無安全衝突。綜述討論多種條件及假說，指南每週餵養及室溫時間用於指定的冷藏酸種及麵包流程。文章把中心溫度限定為有蓋鑄鐵鍋食譜的熟度指標。未發現需人工確認的安全主張。

## 第 1 輪修正後複查

- 複查時間為 2026-11-22 19:52（臺灣時間）。以下結果為獨立內容審查的核准建議，正式入庫仍須通過核准狀態下的 Lint。
- 複查四篇具備必填欄位、對應的來源 ID 與逐段引用。回溯原文的位置均可核對。四篇科學與實作內容、引用忠實度、新手可讀性均為 pass。

| 項目 | 結果 | 原文與修正核對 | 已用修正輪次／退回節點 |
|---|---|---|---|
| W001 | pass | 已補第 1 頁的完整書目、DOI、CC BY 4.0 及中文摘要說明。新增的自發酸種與酸鹼值說明可依 Background 第 3–4 頁及 Bacteria 第 6 頁核對，產氣與產酸敘述適切。 | 1／none |
| W002 | pass | 已補完整書目與授權。廚房筆記表述為讀者可操作的觀察方式，適用條件來自第 13–18 頁，並保留第 24 頁對因果推論的限制。 | 1／none |
| W003 | pass | 已區分取出的酸種與餵好後加入主麵糰的酵頭，接續連結指向 W004。維持指南 Maintaining the Starter 步驟 1–6 和 Make a sponge 步驟 1–2 的兩條操作順序。 | 1（用語調整）／none |
| W004 | pass | 材料準備補抹碗用油，Mix 步驟 4–5 的兩段補粉量及軟度判斷均可核對。Bake 步驟 1、3–5 的預熱時機、隔熱手套、溫度計測量後續烤及網架冷卻都已補齊。190 °F 換算為約 88 °C，限定用於這份配方的熟度觀察。 | 1／none |
| SRC-001 摘要 | pass | 已修正 Background 在第 3–4 頁、圖 1 在第 5 頁、產酸第 8–9 頁與 Yeast 第 10 頁。Temperature、Time 及圖 3 涵蓋第 15–18 頁，研究限制定位至第 23–24 頁。作者、出處、DOI 及授權和原文首頁相符。 | 1（證據定位）／none |
| SRC-004 摘要 | pass | CSU Extension 頁首署名與審閱日期、正文小節與採用條件相符。原創事實摘要與段落定位符合本次採用的權利範圍。 | 0／none |

- 複查結論為 SRC-001、SRC-004 及 W001–W004 均建議核准。四篇保留的主張中無須標為 `needs_human_review` 的食品安全衝突。W003 的操作適用於已建立的冷藏酸種，W004 的烘烤數字適用於具體食譜。來源中的概括健康效益未納入。
