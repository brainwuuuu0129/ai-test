# Jira Bug 质量报告 — Reference

## 1. Jira API 调用规范

### 认证方式

Basic Auth：`email:api_token` Base64 编码

```bash
curl -s -X POST \
  -u "email@company.com:API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jql":"...","maxResults":500,"fields":["key","summary",...]}' \
  "https://{domain}/rest/api/3/search/jql"
```

### 注意事项

- **必须用 POST**：GET `/rest/api/3/search` 已废弃，会返回 `The requested API has been removed`
- **maxResults 范围**：1 ~ 5000，不可为 0
- **分页**：响应包含 `nextPageToken` 和 `isLast`，循环直到 `isLast: true`

### 分页模板（Python）

```python
all_issues = []
next_token = None

while True:
    body = {
        "jql": jql,
        "maxResults": 500,
        "fields": field_list
    }
    if next_token:
        body["nextPageToken"] = next_token
    
    result = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "-u", f"{email}:{token}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(body),
         f"https://{domain}/rest/api/3/search/jql"],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    issues = data.get("issues", [])
    all_issues.extend(issues)
    
    if data.get("isLast", True):
        break
    next_token = data.get("nextPageToken")
    if not next_token:
        break
```

### 自定义字段发现

```bash
curl -s -u "email:token" "https://{domain}/rest/api/3/field" \
  | python3 -c "
import json, sys
for f in json.load(sys.stdin):
    if 'keyword' in f.get('name','').lower():
        print(f'{f[\"id\"]:30} | {f[\"name\"]}')"
```

已知字段映射（saltalk.atlassian.net）：

| 字段名 | Field ID |
|--------|----------|
| Is Leak Bug | `customfield_10224` |
| Bug Type | `customfield_10461` |

## 2. 分析维度计算规则

### 维度1: 按 Parent 项目

**数据提取**：
```python
parent = issue["fields"].get("parent")
if parent:
    label = f'{parent["key"]} {parent.get("fields",{}).get("summary","")}'
else:
    label = "（无 Parent）"
```

**输出**：按 bug 数降序 → 每行展示 Parent label + 总数 + CONFIRM/FIXED/Cancel/Open 分列。

### 维度2: Leak Bug（线上问题）

**字段结构**：`customfield_10224` 是数组类型：
```json
[{"self": "...", "value": "Leak Bug", "id": "10128"}]
```

**判断逻辑**：
```python
def is_leak(issue):
    field = issue["fields"].get("customfield_10224")
    if field and isinstance(field, list):
        return any(
            isinstance(item, dict) and item.get("value") == "Leak Bug"
            for item in field
        )
    return False
```

**输出**：Leak bug 明细表 + 未设置字段的 warning（提示可能存在漏标）。

### 维度3: 月度趋势

**两次查询**：
1. 新增：`type = Bug AND created >= "start" AND created <= "end"`
2. 关闭：`type = Bug AND resolved >= "start" AND resolved <= "end"`

**计算**：
```
净增 = 新增 - 关闭
趋势 = 净增 ≤ 0 → "收敛" | 净增 > 0 → "积压"
```

**注意**：关闭查询可能包含时间范围之前创建的 bug，这是正确的（跨期关闭）。

### 维度4: Bug 生命周期

**已解决 Bug**：
```python
days = (resolutiondate - created).days
```

**时长分段**：

| 分段 | 范围 | 含义 |
|------|------|------|
| 当天 | 0 天 | 当日修复 |
| 1天 | 1 天 | 次日修复 |
| 2-3天 | 2-3 天 | 快速修复 |
| 4-7天 | 4-7 天 | 一周内 |
| 1-2周 | 8-14 天 | 较慢 |
| 2周-1月 | 15-30 天 | 慢 |
| 超1月 | >30 天 | 严重滞后 |

**未关闭 Bug**：
```python
age = (today - created).days
```
按 age 降序排列，标记超过 100 天的为高风险。

### 维度5: P1 Bug

**JQL**：追加 `AND priority in (High, Highest)`

**输出**：
- 完整明细表（含 Jira 链接）
- 每条标注修复时长或"已挂 N 天"
- 未关闭的 P1 bug 单独高亮

## 3. HTML 报告模板与样式

### 配色方案

**优先级**：

| 优先级 | 颜色 | badge class |
|--------|------|-------------|
| Highest | `#dc2626` | `badge-highest` |
| High | `#f97316` | `badge-high` |
| Medium | `#eab308` (文字色 `#1e293b`) | `badge-medium` |
| Low | `#22c55e` | `badge-low` |
| Lowest | `#9ca3af` | `badge-lowest` |

**状态**：

| 状态 | 颜色 | badge class |
|------|------|-------------|
| CONFIRM | `#3b82f6` | `badge-confirm` |
| Cancel | `#9ca3af` | `badge-cancel` |
| FIXED | `#22c55e` | `badge-fixed` |
| Open | `#f59e0b` | `badge-open` |

**生命周期分布条颜色**（从快到慢）：
```
当天: #22c55e → 1天: #84cc16 → 2-3天: #a3e635 → 4-7天: #eab308 → 1-2周: #f97316 → 2周-1月: #ef4444 → 超1月: #dc2626
```

### CSS 核心样式

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f8fafc;
  color: #1e293b;
  line-height: 1.6;
}
.container { max-width: 1200px; margin: 0 auto; padding: 24px; }

/* Summary Cards - 6列自适应 */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}
.card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.card-value { font-size: 32px; font-weight: 700; }

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  font-size: 13px;
}
th { background: #f1f5f9; padding: 10px 12px; font-weight: 600; }
td { padding: 8px 12px; border-top: 1px solid #f1f5f9; }

/* Badges */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
}

/* Trend chart bars */
.trend-chart {
  display: flex;
  align-items: flex-end;
  gap: 24px;
  justify-content: center;
  padding: 20px;
}
.trend-bar {
  width: 36px;
  border-radius: 4px 4px 0 0;
}

/* Lifecycle distribution bar */
.lifecycle-bar {
  display: flex;
  border-radius: 6px;
  overflow: hidden;
  height: 32px;
}

/* Bar chart rows */
.bar-row { display: flex; align-items: center; margin: 6px 0; }
.bar-label { width: 120px; text-align: right; padding-right: 12px; }
.bar-track { flex: 1; height: 24px; background: #f1f5f9; border-radius: 4px; }
.bar-fill { height: 100%; border-radius: 4px; }

/* Section wrapper */
.section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  margin-bottom: 24px;
}

/* Warning / Danger callouts */
.warning {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 12px 16px;
  border-radius: 0 8px 8px 0;
}
.danger {
  background: #fef2f2;
  border-left: 4px solid #dc2626;
  padding: 12px 16px;
  border-radius: 0 8px 8px 0;
}
```

### Jira 链接格式

```html
<a class="jira-link" href="https://{domain}/browse/{key}" target="_blank">{key}</a>
```

### 报告页面结构

```
<h1>                     → {period} Bug Quality Report
<p class="subtitle">     → {project} | {date_range} | Generated {today}
<div class="summary-grid"> → 6 张 Summary Cards
<div class="section">    → 维度一：按 Parent 项目分布
<div class="section">    → 维度二：Leak Bug（线上问题）
<div class="section">    → 维度三：月度趋势
<div class="section">    → 维度四：Bug 生命周期
<div class="section">    → 维度五：P1 Bug
<footer>                 → Generated by Claude Code
```

### 趋势图实现

柱状图用 CSS flex + absolute 定位实现（非 canvas/JS），高度按比例缩放：

```python
max_val = max(created, resolved)
bar_height = max(int(value / max_val * 120), 20)  # 最小 20px
```

新增柱颜色：`#f97316`（橙色）
关闭柱颜色：`#22c55e`（绿色）

## 4. 输出文件命名

| 格式 | 文件名 |
|------|--------|
| HTML | `{period}-bug-report.html`（如 `q1-bug-report.html`） |
| 季度 | `q1` / `q2` / `q3` / `q4` |
| 月度 | `2026-01` |
| 自定义 | 用户指定的名称 |

## 5. 边界处理

| 场景 | 处理 |
|------|------|
| 自定义字段 ID 未知 | 先调用 `/rest/api/3/field` 搜索确认 |
| Is Leak Bug 字段未设置 | 归入"非 Leak"，并在报告中输出 warning 提示漏标 |
| Parent 为空 | 归入"（无 Parent）"分组 |
| resolutiondate 为空 | 视为未关闭 bug，计算已挂天数 |
| 数据超过 500 条 | 自动分页，使用 nextPageToken 循环 |
| API 返回错误 | 打印错误信息，提示用户检查认证/JQL |
