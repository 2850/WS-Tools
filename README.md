# WS-Tools

一鍵互動安裝你的 Copilot CLI 自定義 plugin marketplace。

## 快速使用

```bash
npx github:2850/WS-Tools
```

執行後會出現互動式勾選清單，**所有 plugin 預設全部打勾**，按 `空白鍵` 取消不要的項目，按 `Enter` 確認並開始安裝。

```
? 選擇要安裝的 plugin（預設全部已勾選，按空格取消不想要的）：
 ❯◉ sequence-diagram-generator - My personal dev tools plugin for Copilot CLI
  ◉ youtube-summary-note - youtube-summary with transcript
```

## 包含的 Plugins

| Plugin | 說明 |
|--------|------|
| `sequence-diagram-generator` | 根據需求文件繪製時序圖，支援 Mermaid、Excalidraw、draw.io 多種格式輸出 |
| `youtube-summary-note` | 將 YouTube 逐字稿翻譯成繁體中文，並做摘要整理，輸出 Obsidian 友好格式 |

## 新增 Plugin

在 `plugins/` 目錄下建立一個新資料夾，內含標準的 Copilot CLI `plugin.json` 即可自動被偵測到。

```
plugins/
  your-plugin/
    plugin.json
    agents/
    skills/
```

## 需求

- [Node.js](https://nodejs.org/) 14+
- [GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli) 已安裝並登入

## License

MIT © Willis
