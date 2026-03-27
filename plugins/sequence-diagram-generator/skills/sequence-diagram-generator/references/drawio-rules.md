# draw.io XML 規範與錯誤處理

## 基本結構

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxGraphModel dx="1422" dy="762" grid="0" ...>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- 所有圖形元素 -->
  </root>
</mxGraphModel>
```

所有圖形元素的 `parent` 必須設為 `"1"`。

---

## Vertex（圖形節點）

```xml
<mxCell id="myId" value="顯示文字" style="..." vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="40" as="geometry" />
</mxCell>
```

- `mxGeometry` 必須是 self-closing 或包含子元素
- `as="geometry"` 必填

常用 style 範例：
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=16;fontStyle=1;
line;strokeColor=#9673a6;strokeWidth=1;dashed=1;fillColor=none;html=1;
```

---

## Edge（箭頭/連線）

```xml
<mxCell id="myEdge" value="標籤" style="..." edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="200" as="sourcePoint" />
    <mxPoint x="300" y="200" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

### ⚠️ Edge 樣式禁止事項

| 禁止 | 原因 |
|------|------|
| `exitX/exitY/entryX/entryY` | 只在有 source/target node ID 時有效；浮點 edge 加了會造成解析錯誤 |
| 使用 `source="nodeId"` + `sourcePoint` 混用 | 二擇一，不能混用 |

### ✅ 正確 Edge 樣式

```
endArrow=block;startArrow=none;strokeColor=#6c8ebf;strokeWidth=1.5;html=1;
```

虛線（return message）：
```
endArrow=block;startArrow=none;strokeColor=#82b366;strokeWidth=1.5;dashed=1;dashPattern=8 4;html=1;
```

### Self-loop（自我引用）

使用 `waypoints` 繞一圈：

```xml
<mxCell id="selfLoop" value="⑩ 自我處理" style="endArrow=block;strokeColor=#b85450;html=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="880" y="800" as="sourcePoint" />
    <mxPoint x="880" y="832" as="targetPoint" />
    <Array as="points">
      <mxPoint x="940" y="800" />
      <mxPoint x="940" y="832" />
    </Array>
  </mxGeometry>
</mxCell>
```

---

## 已知錯誤與解法

### 錯誤 1：`a.push is not a function for mxGeometry`

**原因**：使用 `xml.etree.ElementTree` + `minidom.toprettyxml()` 產生 XML 時，minidom 在元素間插入多餘空白文字節點（`#text`），draw.io 的解析器誤認為非法子元素。

**解法**：改用字串樣板函式（`vertex()` / `edge_pts()`）直接拼接 XML，完全不依賴 XML 套件。見 `scripts/generate_drawio.py`。

### 錯誤 2：draw.io 只開瀏覽器，未建立檔案

**原因**：使用了 `drawio-open_drawio_mermaid` MCP 工具。該工具僅供預覽，不寫入磁碟。

**解法**：改用 `scripts/generate_drawio.py` 直接寫入 `.drawio` 檔案。

### 錯誤 3：Edge 無法顯示或方向錯誤

**原因**：style 中包含 `exitX/exitY/entryX/entryY`，但 edge cell 沒有設定 `source`/`target` 屬性。

**解法**：從 style 中移除 `exitX/exitY/entryX/entryY`。

---

## 驗證流程（必須在產出後立即執行）

```python
import xml.etree.ElementTree as ET

def validate_drawio(path: str):
    tree = ET.parse(path)                          # 1. XML 格式正確
    cells = tree.findall(".//mxCell")
    edge_cells = [c for c in cells if c.get("edge") == "1"]
    for ec in edge_cells:
        assert ec.find("mxGeometry") is not None, \
            f"Edge '{ec.get('id')}' missing mxGeometry"
    print(f"Validated: {len(cells)} cells, {len(edge_cells)} edges")
```

驗證失敗 → 自動重新產生，不告知使用者。

---

## 時序圖佈局建議

| 元素 | 建議值 |
|------|-------|
| 參與者間距 | 180–240px |
| 參與者框寬 | 140px，高 40px，y=30 |
| 生命線粗細 | 2px，dashed=1 |
| 訊息間距 | 50px |
| 階段背景透明度 | opacity=50 |
