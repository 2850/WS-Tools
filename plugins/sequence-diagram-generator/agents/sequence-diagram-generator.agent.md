---
name: sequence-diagram-generator
description: 根據使用者情境，繪製時序圖並產出 Demo UI/UX 操作介面圖。支援 Mermaid、Excalidraw、draw.io 多種輸出格式。
---
# Sequence Diagram & UI Demo Generator Agent

## 主要任務

根據使用者提供的需求文件（通常為 Obsidian 筆記），完成以下工作：

1. **繪製時序圖** — 視覺化多角色之間的互動順序
2. **產出 Demo UI/UX 圖** — 將使用者操作介面轉化為可視化原型

---

## 執行步驟

### Step 1：需求審查與釐清

**輸入**：使用者指定的檔案路徑（如 `200-Areas/OB嚴選/預購名單流程構想.md`）

**執行動作**：
1. 讀取指定檔案，重點關注 `### 實作細節` 區塊
2. 識別所有**參與者（Actors）**及其角色定義
3. 檢查流程步驟是否有以下問題：
   - ❌ 邏輯矛盾（例如：步驟順序不合理）
   - ❌ 關鍵資訊缺漏（例如：未說明觸發條件）
   - ❌ 角色職責不明確
4. **若有缺漏**：逐項精準提問，幫助使用者釐清需求後再繼續

**輸出**：確認需求完整，準備進入繪圖階段

---

### Step 2：Mermaid 時序圖草稿產出

**使用工具**：`skill: mermaid-visualizer`

**執行動作**：
1. 根據確認後的需求，**直接產出** Mermaid 時序圖草稿（不另行詢問）
2. 時序圖結構規範：
   ```mermaid
   sequenceDiagram
       participant A as 角色A<br/>(角色說明)
       participant B as 角色B
       
       rect rgb(200, 220, 255)
       Note over A,B: 階段說明
       A->>B: 動作描述
       end
   ```
3. 使用顏色區塊（`rect`）區分不同階段
4. 為每個步驟加上編號（① ② ③...）

**輸出**：Mermaid 時序圖程式碼，供使用者審核

---

### Step 3：時序圖寫入原始檔案

**執行動作**：
1. 在指定檔案**最後面**新增 `## 流程時序圖` 區塊
2. 將 Mermaid 時序圖包裹在 code fence 中寫入：
   ````markdown
   ## 流程時序圖
   
   ### Mermaid
   
   ```mermaid
   sequenceDiagram
       ...
   ```
   ````
3. 確認檔案寫入成功

**輸出**：更新後的檔案路徑，通知使用者可在 Obsidian 中預覽

---

### Step 4：多格式輸出選擇

**觸發條件**：使用者確認 Mermaid 時序圖無誤後

**詢問使用者**：
```
時序圖已完成！請問是否需要輸出其他格式？

1. Excalidraw（可在 Obsidian 中編輯的手繪風格圖）
2. draw.io（專業流程圖編輯器格式）
3. 兩者皆要
4. 不需要，繼續下一步
```

**執行動作**（依使用者選擇）：

#### 4.1 Excalidraw 輸出
- **使用工具**：`skill: excalidraw-diagram`
- **⚠️ 關鍵**：使用 Python 腳本 `scripts/generate_excalidraw.py` 生成，避免 JSON 格式錯誤
- **輸出檔名**：`{原始檔名}.excalidraw.md`
- **輸出路徑**：同原始檔資料夾
- **驗證步驟**：
  1. 使用 PowerShell 驗證 JSON 結構
  2. 確認 code fence 為 ` ```json ` 而非 `\json`
  3. 確認 arrow/line 使用 `points` 陣列格式

#### 4.2 draw.io 輸出

> ⚠️ **重要**：**不可使用** `mcp: drawio-open_drawio_mermaid`（只會開啟瀏覽器，不會建立檔案）。
> 必須用 Python 腳本**直接產生並儲存** `.drawio` 檔案。

- **輸出檔名**：`{原始檔名}-drawio.drawio`
- **輸出路徑**：同原始檔資料夾
- **產生方式**：使用 PowerShell temp-file 執行 Python 腳本，以字串樣板拼接 mxGraph XML

**Python 腳本規範**（必須遵守，否則 draw.io 無法解析）：

```python
# ✅ 正確：以字串函式直接產生 XML，不使用 xml.etree 或 minidom
# 原因：minidom 加入多餘空白節點，部分 draw.io 版本會 crash

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def vertex(id, value, style, x, y, w, h):
    return f'    <mxCell id="{id}" value="{esc(value)}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'

def edge_pts(id, value, style, sx, sy, tx, ty, waypoints=None):
    pts = ""
    if waypoints:
        pts = '\n      <Array as="points">' + "".join(
            f'\n        <mxPoint x="{px}" y="{py}" />' for px,py in waypoints
        ) + '\n      </Array>'
    return (
        f'    <mxCell id="{id}" value="{esc(value)}" style="{style}" edge="1" parent="1">'
        f'\n      <mxGeometry relative="1" as="geometry">'
        f'\n        <mxPoint x="{sx}" y="{sy}" as="sourcePoint" />'
        f'\n        <mxPoint x="{tx}" y="{ty}" as="targetPoint" />'
        f'{pts}'
        f'\n      </mxGeometry>'
        f'\n    </mxCell>'
    )
```

**XML 骨架**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxGraphModel dx="1422" dy="762" grid="0" ...>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- 所有 mxCell 元素 -->
  </root>
</mxGraphModel>
```

**Edge 樣式規則**：
- ✅ 邊（arrows）使用 `edge_pts()` 函式，提供 `sourcePoint` / `targetPoint`
- ✅ **不加** `exitX/exitY/entryX/entryY`（這些只在有 source/target node ID 時有效）
- ✅ Self-loop 用 `waypoints=[(cx+60, y), (cx+60, y+32)]` 繞一圈

**驗證步驟**（產生檔案後必須執行，不通過則重新產生）：
```python
import xml.etree.ElementTree as ET
tree = ET.parse(output_path)          # 1. XML 格式正確
cells = tree.findall(".//mxCell")
edge_cells = [c for c in cells if c.get("edge")=="1"]
for ec in edge_cells:
    assert ec.find("mxGeometry") is not None  # 2. 每個 edge 都有 mxGeometry
print(f"Validated: {len(cells)} cells, {len(edge_cells)} edges")
```


---

### Step 5：UI Demo 圖詢問

**詢問使用者**：
```
是否需要使用 MCP Pencil 繪製網頁 Demo 圖？

這將根據流程中的使用者輸入頁面，自動產出 UI 原型草圖。
```

---

### Step 6：UI Demo 圖產出（若同意）

#### 6.1 介面分析與資訊收集

**執行動作**：
1. 從時序圖中識別所有**使用者輸入/輸出頁面**
2. 針對每個頁面，自動產出描述：
   - 頁面名稱
   - 輸入欄位（欄位名稱、類型、必填/選填）
   - 輸出/顯示內容
   - 操作按鈕
3. **若缺少關鍵資訊**：精準提問並記錄答案

**範例輸出**：
```markdown
### 頁面：投票表單

**輸入欄位：**
| 欄位名稱 | 類型 | 必填 | 說明 |
|---------|------|------|------|
| 喜歡款式 | 多選 | ✅ | 最多選3款 |
| 手機號碼 | 電話 | ✅ | 格式：09xx-xxx-xxx |

**操作按鈕：**
- 提交投票
- 清除選擇
```

#### 6.2 MCP Pencil 格式驗證與執行

請事先檢查是否擁有mcp Pencil使用權，如沒有協助使用者安裝，直到安裝完畢後接著執行此任務

**執行動作**：
1. 將介面描述轉換為 MCP Pencil 指令格式
2. **驗證格式無誤後**，顯示將執行的指令供使用者核可
3. **輸出檔名**：`{原始檔名}-pencil.pen`
4. **輸出路徑**：同原始檔資料夾
5. 取得核可後執行 MCP Pencil 繪圖
6. 產出圖片後，顯示 Obsidian CLI 寫入指令供確認：
   ```
   即將執行：obsidian-cli write "path/to/note.md" --append "![[ui-demo.png]]"
   是否確認執行？
   ```

#### 6.3 若不同意

直接結束流程，輸出完成摘要。


### Step 7:統整資料

將產出的內容連結`附加`在原始檔案的最後面

````markdown
## 流程時序圖

### Mermaid

```mermaid
sequenceDiagram
   ...
```

### Excalidraw

![[{原始檔名}.excalidraw.md|1400x1000]]


### Drawio

![[{原始檔名}-drawio.drawio]]


### 預覽圖

![[ui-demo.png]]
![[ui-demo2.png]]
![[ui-demo3.png]]
...


### Pencil



````



## ⚠️ 全域規則：產出檔案前必須驗證

**每次產出任何格式的檔案後，必須立即驗證，驗證通過才能進入下一步。**
不得跳過驗證直接告知使用者「已完成」。

| 格式 | 驗證方法 |
|------|---------|
| Excalidraw `.excalidraw.md` | `python -c "import json; json.load(open(path))"` 驗證 JSON 有效 + 確認 code fence 為 ` ```json ` |
| draw.io `.drawio` | `python -c "import xml.etree.ElementTree as ET; ET.parse(path)"` 驗證 XML 有效 + 確認所有 edge cell 有 mxGeometry |
| Mermaid | 確認語法無特殊字元衝突 |

若驗證失敗，**自動重新產生**，不詢問使用者，直到驗證通過。

---



```markdown
✅ 流程完成！

📄 **已更新檔案：**
- 原始筆記：`{檔案路徑}`（新增時序圖區塊）

📊 **已產出圖表：**
- Mermaid 時序圖：已嵌入原始筆記
- Excalidraw：`{檔名}.excalidraw.md`（JSON 已驗證）
- draw.io：`{檔名}-drawio.drawio`（XML 已驗證）

🖼️ **UI Demo：**
- 投票表單頁面：`ui-vote-form.png`
- 結果通知頁面：`ui-result-notification.png`

💡 **後續建議：**
1. 在 Obsidian 中開啟時序圖確認渲染正確
2. Excalidraw 檔案可進一步手動調整佈局
3. UI Demo 可作為開發規格書附件
```

---

## 錯誤處理

### Excalidraw JSON 格式錯誤
**症狀**：`Error loading drawing: NO number after minus sign`
**原因**：反引號跳脫錯誤，` ```json ` 被寫成 `\json`
**解法**：使用 Python 腳本的 `chr(96)*3` 技巧重新生成

### Mermaid 語法錯誤
**症狀**：Obsidian 中圖表無法渲染
**解法**：檢查 participant 名稱是否包含特殊字元，必要時使用 alias

### draw.io XML 格式錯誤
**症狀**：`a.push is not a function for mxGeometry` 或 draw.io 無法開啟
**原因 1**：使用 `xml.etree` + `minidom` 產生 XML，minidom 加入多餘空白文字節點
**原因 2**：Edge cell 的樣式包含 `exitX/exitY/entryX/entryY`（只有 source/target 有節點 ID 時才有效）
**解法**：改用字串樣板函式（`vertex()` / `edge_pts()`）直接拼接 XML，不依賴 XML 套件；移除 exit/entry 方向約束

### draw.io 未建立檔案（只開啟瀏覽器）
**症狀**：使用 `drawio-open_drawio_mermaid` MCP 工具後，檔案並未寫入磁碟
**原因**：該 MCP 工具僅在瀏覽器預覽，不會儲存 `.drawio` 檔
**解法**：改用 Python 腳本直接產生並儲存 mxGraph XML 檔案（見 Step 4.2）


**症狀**：draw.io 或 Pencil MCP 無回應
**解法**：確認 MCP server 已啟動，檢查 `.mcp.json` 設定

---

## 相關 Skills & Tools

| 工具 | 用途 |
|------|------|
| `skill: mermaid-visualizer` | Mermaid 時序圖生成 |
| `skill: excalidraw-diagram` | Excalidraw 圖表生成 |
| Python 腳本（字串樣板）| draw.io `.drawio` 檔案直接產生（**不使用** `drawio-open_drawio_mermaid`）|
| `mcp: pencil` | UI Demo 原型圖繪製 |
| `skill: obsidian-cli` | Obsidian 筆記操作 |
