# HTML 上线通知 — 详细参考

## 1. HTML 模板结构

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Release Notification — {Title}</title>
  <style>
    /* 见 §2 CSS 样式规范 */
  </style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1>{Title}</h1>
    <div class="subtitle">{Team Name}</div>
    <div class="subtitle">Release Date: {YYYY/MM/DD}</div>
  </div>

  <!-- 1. Release Overview -->
  <div class="section-title"><span class="section-number">1</span>Release Overview</div>
  <div class="card">
    <div class="overview-grid">
      <!-- 2×2 grid: Team, Release Period/Date, Total Items, Platforms -->
    </div>
  </div>

  <!-- Background (optional) -->
  <div class="card background-card">
    <div class="field">
      <div class="field-label">Background</div>
      <div class="field-text">{背景说明}</div>
    </div>
  </div>

  <!-- 2. Release Items -->
  <div class="section-title"><span class="section-number">2</span>Release Items</div>

  <!-- 每个 Item 一张 card -->
  <div class="card item-card">
    <div class="item-header">
      <span class="item-title">2.x {Title}</span>
      <span class="badge badge-{type}">{Type}</span>
    </div>
    <div class="field">
      <div class="field-label">Overview</div>
      <div class="field-text">{概述}</div>
    </div>
    <div class="field">
      <div class="field-label">Key Changes</div>
      <ul>
        <li>{变更点}</li>
      </ul>
    </div>
    <div class="field">
      <div class="field-label">Impact Scope</div>
      <div class="impact-tags">
        <span class="tag tag-platform">{Platform}</span>
        <span class="tag tag-user-facing">User-facing</span>
      </div>
    </div>
    <div class="screenshot-gallery">
      <img src="data:image/png;base64,{base64}" alt="{description}">
    </div>
  </div>

  <!-- 3. Outstanding Issues -->
  <div class="section-title"><span class="section-number">3</span>Outstanding Issues &amp; Known Limitations</div>
  <div class="card warning-card">
    <span class="fix-date">Expected Fix: {date}</span>
    <ul><li><strong>{问题}</strong> — {影响}</li></ul>
  </div>

  <!-- 4. Notes -->
  <div class="section-title"><span class="section-number">4</span>Notes</div>
  <div class="card tip-card">
    <div class="field-text">{补充说明}</div>
  </div>

  <!-- Footer -->
  <div class="footer">{Team} · Release Notification · Confidential</div>

</div>
</body>
</html>
```

## 2. CSS 样式规范

### 2.1 基础

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: #f5f7fa;
  color: #333;
  line-height: 1.6;
  padding: 24px;
}
.container { max-width: 860px; margin: 0 auto; }
```

### 2.2 Header

```css
.header {
  background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
  color: #fff;
  border-radius: 12px;
  padding: 36px 40px;
  margin-bottom: 24px;
}
.header h1 { font-size: 24px; font-weight: 700; }
.header .subtitle { font-size: 14px; opacity: 0.85; margin-top: 4px; }
```

### 2.3 Section 标题

```css
.section-title {
  font-size: 18px; font-weight: 700; color: #1a365d;
  margin: 28px 0 12px; padding-bottom: 6px; border-bottom: 2px solid #e2e8f0;
}
.section-number {
  display: inline-block; background: #1a365d; color: #fff;
  width: 26px; height: 26px; line-height: 26px; text-align: center;
  border-radius: 50%; font-size: 13px; margin-right: 8px;
}
```

### 2.4 卡片

```css
.card {
  background: #fff; border-radius: 10px; padding: 20px 24px;
  margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.item-card    { border-left: 4px solid #2b6cb0; }
.warning-card { border-left: 4px solid #ed8936; background: #fffaf0; }
.info-card    { border-left: 4px solid #4299e1; background: #ebf8ff; }
.tip-card     { border-left: 4px solid #38a169; background: #f0fff4; }
.background-card { border-left: 4px solid #2b6cb0; background: #ebf8ff; }
```

### 2.5 类型标签

```css
.badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
.badge-new-feature   { background: #c6f6d5; color: #22543d; }
.badge-enhancement   { background: #bee3f8; color: #2a4365; }
.badge-bug-fix       { background: #feebc8; color: #7b341e; }
.badge-config-change { background: #e2e8f0; color: #4a5568; }
```

### 2.6 Impact 标签

```css
.tag { display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 12px; font-weight: 500; }
.tag-platform    { background: #ebf4ff; color: #2b6cb0; }
.tag-user-facing { background: #f0fff4; color: #276749; border: 1px solid #c6f6d5; }
```

### 2.7 截图

```css
.screenshot-gallery {
  display: flex; gap: 12px; margin-top: 12px; flex-wrap: wrap; justify-content: center;
}
.screenshot-gallery img {
  max-height: 620px; border-radius: 8px;
  border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
```

### 2.8 响应式

```css
@media (max-width: 600px) {
  body { padding: 12px; }
  .header { padding: 24px 20px; }
  .overview-grid { grid-template-columns: 1fr; }
  .card { padding: 16px; }
  .screenshot-gallery img { max-height: 500px; }
}
```

## 3. 截图嵌入脚本模板

由于 base64 嵌入后 HTML 文件极大（通常 1MB+），无法使用 Read/Edit 工具。必须使用 Python 脚本操作：

### 3.1 初次嵌入

```python
import base64, re

HTML_FILE = "{output_file_path}"

images = {
    "placeholder comment text": "image_file_path.png",
}

with open(HTML_FILE, "r") as f:
    html = f.read()

for placeholder_key, img_path in images.items():
    with open(img_path, "rb") as img_f:
        b64 = base64.b64encode(img_f.read()).decode("utf-8")
    pattern = r'<!-- IMG_PLACEHOLDER: ' + re.escape(placeholder_key) + r' -->\s*<div class="screenshot-placeholder">.*?</div>'
    replacement = f'<img src="data:image/png;base64,{b64}" alt="{placeholder_key}">'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open(HTML_FILE, "w") as f:
    f.write(html)
```

### 3.2 追加图片到已有 gallery

```python
import base64

HTML_FILE = "{output_file_path}"

with open("new_image.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

with open(HTML_FILE, "r") as f:
    html = f.read()

# 在目标位置的已有 img 标签后追加
html = html.replace(
    'alt="existing_image_alt">',
    f'alt="existing_image_alt">\n      <img src="data:image/png;base64,{b64}" alt="new_image_alt">',
    1
)

with open(HTML_FILE, "w") as f:
    f.write(html)
```

### 3.3 通用内容修改

```python
HTML_FILE = "{output_file_path}"

with open(HTML_FILE, "r") as f:
    html = f.read()

html = html.replace("old_text", "new_text")

with open(HTML_FILE, "w") as f:
    f.write(html)
```

## 4. Item 卡片边框色规则

不同类型的 item-card 使用不同左侧边框色以增强视觉区分：

| 类型 | 边框色 | 写法 |
|------|--------|------|
| Enhancement | 蓝色（默认） | 无需额外 style |
| Bug Fix | 橙色 | `style="border-left-color: #ed8936;"` |
| New Feature | 绿色 | `style="border-left-color: #38a169;"` |
| Config Change | 灰色 | `style="border-left-color: #a0aec0;"` |

## 5. 文件大小预估

| 截图数量 | 预估 HTML 大小 |
|----------|---------------|
| 0 | ~10 KB |
| 3 | ~1.5 MB |
| 5 | ~2.5 MB |
| 8 | ~4 MB |
| 10+ | ~5 MB+ |

> 飞书文件发送限制通常为 100MB，HTML 内嵌图片不会超限。但超过 5MB 时建议检查图片是否可压缩。
