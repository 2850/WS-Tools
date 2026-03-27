---
name: merge-video-transcript-and-notes
description: 將 YouTube 逐字稿翻譯檔（-zh.md）與整理筆記檔（-notes.md）合併成一個完整的筆記檔（-full.md）
---

你是一個筆記整理 skill，負責把 YouTube 逐字稿的翻譯與整理筆記合併成一個完整的 Markdown 檔案。

# 輸入參數
- `inputPath`: 翻譯檔路徑，例如：`notes/2026/2026-03-20-video.md`

# 輸出規則
- 產生一個新檔，檔名為 `inputPath-full.md`，例如：`2026-03-20-video-full.md`。
- `notesPath`: 整理筆記檔路徑，例如：`notes/2026/2026-03-20-video-summery.md`
- 結構如下：
  - `## Transcript`（直接貼 `transcriptPath` 內容）
  - `## Notes`（直接貼 `inputPath` 內容）
  - `## Sources`（在最後加上來源連結，用 Obsidian 格式：`來源：[[2026-03-20-video.md]]`）

# 處理規則
- 不要改寫、不要刪減，只做「合併」。
- 保留所有原始格式、時間戳、段落。
- 用 Markdown，方便貼回 Obsidian。