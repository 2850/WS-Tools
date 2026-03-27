---
name: sequence-diagram-generator
description: 根據使用者提供的需求文件（Obsidian 筆記），繪製流程時序圖並產出多格式圖表（Mermaid、Excalidraw、draw.io）及 UI Demo 原型。觸發情境：(1) 使用者指定一個筆記路徑並要求「畫時序圖」、「產出流程圖」、「建立 draw.io」；(2) 需要將角色互動流程視覺化；(3) 需要產出可在 Obsidian 嵌入的 .excalidraw.md 或 .drawio 檔案。
---

# Sequence Diagram Generator

## Overview

從需求文件中提取流程，依序產出 Mermaid 時序圖、Excalidraw 手繪圖、draw.io XML 圖，並可選擇產出 UI Demo 原型。每個格式產出後必須驗證，才進入下一步。

## Workflow

### Step 1：需求審查

1. 讀取指定 `.md` 檔，重點關注 `### 實作細節` 區塊
2. 識別所有參與者（Actors）及角色定義
3. 若有邏輯矛盾、缺漏或角色不明確 → 逐項提問再繼續

### Step 2：Mermaid 時序圖

使用 `skill: mermaid-visualizer` 產出草稿，用 `rect` 色塊區分階段，步驟加編號（① ② ③…）。寫入原始檔案末尾的 `## 流程時序圖 / ### Mermaid` 區塊。

### Step 3：多格式輸出（詢問使用者）

詢問：Excalidraw / draw.io / 兩者皆要 / 不需要

#### 3.1 Excalidraw

使用 `skill: excalidraw-diagram` 的 `scripts/generate_excalidraw.py`：
- 輸出：`{原始檔名}.excalidraw.md`，同資料夾
- **驗證**：解析檔案內的 JSON code block，確認 JSON 有效且 code fence 為 ` ```json `（非 `\json`）

#### 3.2 draw.io

> ⚠️ **不可使用** `drawio-open_drawio_mermaid` MCP（只開瀏覽器，不建立檔案）

使用本 skill 的 `scripts/generate_drawio.py` 直接產生 `.drawio` 檔：
- 輸出：`{原始檔名}-drawio.drawio`，同資料夾
- **驗證**：`python -c "import xml.etree.ElementTree as ET; ET.parse('PATH')"` 必須通過
- 驗證失敗 → 自動重新產生，不詢問使用者

### Step 4：UI Demo（詢問使用者）

詢問是否需要 MCP Pencil 繪製 UI 原型。若同意：
1. 從時序圖找出所有使用者輸入/輸出頁面
2. 列出每個頁面的欄位、按鈕、顯示內容
3. 用 MCP Pencil 產出 `.pen` 檔

### Step 5：統整寫回原始檔

在原始檔 `## 流程時序圖` 區塊下附加各格式的嵌入連結：
`![[{原始檔名}.excalidraw.md]]`、`![[{原始檔名}-drawio.drawio]]`、UI Demo 截圖等。

## 全域規則：產出後必須驗證

| 格式 | 驗證方法 |
|------|---------|
| `.excalidraw.md` | 解析內部 JSON block，確認有效 |
| `.drawio` | `ET.parse()` 通過 + 所有 edge cell 有 `mxGeometry` |

驗證失敗 → **自動重試**，不詢問使用者。

## Scripts

### `scripts/generate_drawio.py`

產生 draw.io mxGraph XML 的輔助函式庫。**必須使用字串樣板**（非 `xml.etree` / `minidom`）。詳見 `references/drawio-rules.md`。

## References

- `references/drawio-rules.md`：draw.io XML 規範、Edge 樣式規則、已知錯誤與解法

# Sequence Diagram Generator

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" -> "Reading" -> "Creating" -> "Editing"
- Structure: ## Overview -> ## Workflow Decision Tree -> ## Step 1 -> ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" -> "Merge PDFs" -> "Split PDFs" -> "Extract Text"
- Structure: ## Overview -> ## Quick Start -> ## Task Category 1 -> ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" -> "Colors" -> "Typography" -> "Features"
- Structure: ## Overview -> ## Guidelines -> ## Specifications -> ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" -> numbered capability list
- Structure: ## Overview -> ## Core Capabilities -> ### 1. Feature -> ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
