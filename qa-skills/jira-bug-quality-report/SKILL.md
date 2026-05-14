---
name: jira-bug-quality-report
description: Generate periodic bug quality reports from Jira data with multi-dimension analysis and HTML visualization. Use when user needs bug report, quality report, bug analysis, bug statistics, or mentions Bug 质量报告, 缺陷报告, Bug 统计, bug quality report.
---

# Jira Bug 质量报告生成

## 适用场景

从 Jira 拉取指定时间范围内的 Bug 数据，按多维度分析后生成可视化 HTML 报告。

**触发示例**：
- "帮我出一份 Q1 的 bug 质量报告"
- "统计一下这个月的 bug 情况"
- "generate a bug quality report for Q2"
- "看下上个季度有多少 bug"

## 前置依赖

| 依赖 | 用途 |
|------|------|
| Jira REST API | Bug 数据查询（需要 domain + email + API token） |
| Python 3 | 数据聚合和 HTML 生成 |

## 执行流程

### Step 1: 收集连接信息

通过对话确认以下信息：

| 字段 | 必填 | 说明 |
|------|------|------|
| Jira 域名 | 是 | 如 `company.atlassian.net` |
| 账号邮箱 | 是 | Atlassian 登录邮箱 |
| API Token | 是 | Atlassian API Token |
| 时间范围 | 是 | 如 Q1 2026 → `2026-01-01` ~ `2026-03-31` |
| JQL 基础条件 | 否 | 默认 `type = Bug`，用户可追加项目/标签等条件 |

**安全提醒**：每次对话结束后提醒用户轮换 API Token。

### Step 2: 数据获取

1. 使用 Jira REST API v3 `/rest/api/3/search/jql`（POST）
2. 分页获取全部数据（`maxResults: 500` + `nextPageToken`）
3. 需要获取的 fields：
   - 基础：`key, summary, status, priority, assignee, created, resolutiondate`
   - 项目归属：`parent`（Parent 字段，代表需求/功能）
   - 线上问题：`customfield_10224`（Is Leak Bug 字段）
   - 按需扩展：用户指定的其他自定义字段
4. 同时查询时间范围内被解决的 Bug（用于趋势分析）：
   - `type = Bug AND resolved >= "start" AND resolved <= "end"`

> API 调用细节、字段发现方法、分页逻辑见 [reference.md §1](references/reference.md#1-jira-api-调用规范)

### Step 3: 多维度分析

报告固定包含 **5 个分析维度**：

| 维度 | 分析内容 | 关键指标 |
|------|---------|---------|
| **1. 按 Parent 项目** | Bug 在各需求/功能下的分布 | 每个 Parent 的 bug 数、状态分布 |
| **2. Leak Bug（线上问题）** | 标记为线上问题的 Bug | Leak 数量、占比、明细 |
| **3. 月度趋势** | 每月新增 vs 关闭 | 净增/收敛趋势、累计未关闭 |
| **4. Bug 生命周期** | 修复效率分析 | 平均/中位数修复天数、时长分布、未关闭风险项 |
| **5. P1 Bug（High+）** | 高优先级 Bug 专项 | P1 数量、修复率、明细列表 |

**各维度计算规则**：

#### 维度1: 按 Parent 项目
- 从 `parent` 字段提取 `parent.key` + `parent.fields.summary`
- 按 bug 数降序排列
- 每个 Parent 统计 CONFIRM / FIXED / Cancel / Open 数量

#### 维度2: Leak Bug
- 字段 `customfield_10224` 为数组，值包含 `{"value": "Leak Bug"}` 时为线上问题
- **注意**：首次使用时需通过 `/rest/api/3/field` 接口确认字段 ID（搜索 "leak"）
- 统计 Leak 占总 bug 比例，并标注未设置该字段的 bug 数量

#### 维度3: 月度趋势
- 新增：按 `created` 月份分组计数
- 关闭：按 `resolutiondate` 月份分组计数（需额外查询 `resolved >= start AND resolved <= end`）
- 净增 = 新增 - 关闭，负数表示收敛

#### 维度4: Bug 生命周期
- 已解决：`resolutiondate - created` = 修复天数
- 时长分段：当天 / 1天 / 2-3天 / 4-7天 / 1-2周 / 2周-1月 / 超1月
- 未关闭：`today - created` = 已挂天数，按挂起时长降序排列

#### 维度5: P1 Bug
- 筛选 `priority in (High, Highest)`
- 列出完整明细，含修复时长或已挂天数
- 标记仍未关闭的 P1 bug 为风险项

> 完整计算公式和边界处理见 [reference.md §2](references/reference.md#2-分析维度计算规则)

### Step 4: 生成 HTML 报告

输出文件：`{output_dir}/{period}-bug-report.html`（如 `q1-bug-report.html`）

**报告结构**：

1. **顶部 Summary Cards** — 6 个关键指标卡片：总 bug 数、关闭数、P1 数、Leak 数、平均修复天数、未关闭数
2. **维度一：Parent 项目表格** — 按 bug 数降序，含状态列
3. **维度二：Leak Bug** — 明细表格 + 未设置字段的警告
4. **维度三：月度趋势** — 柱状图（新增 vs 关闭）+ 趋势表格
5. **维度四：生命周期** — 修复时长分布条 + 柱状图 + 最慢 Top 10 + 未关闭列表
6. **维度五：P1 Bug** — 完整明细表，含 Jira 链接

**HTML 规范**：
- 每个 Bug Key 链接到 Jira：`https://{domain}/browse/{key}`
- 优先级和状态使用彩色 badge
- 响应式布局，最大宽度 1200px
- 纯静态 HTML + 内联 CSS，无外部依赖

> HTML 模板、样式变量、配色方案见 [reference.md §3](references/reference.md#3-html-报告模板与样式)

### Step 5: 交付

1. 生成 HTML 文件并自动在浏览器中打开（`open` 命令）
2. 输出交付说明：
```
报告已生成：{path}
- 浏览器中 Cmd+A 全选 → Cmd+C 复制 → 粘贴到 Lark/邮件
- Bug Key 可直接点击跳转 Jira
```

## 自定义字段发现

首次使用或字段名不确定时，通过以下 API 查找字段 ID：

```
GET /rest/api/3/field
→ 搜索关键词（如 "leak", "bug type"）匹配 field name
→ 记录 customfield_xxxxx ID
```

## 扩展维度

用户可以要求追加以下分析维度（按需实现）：

| 维度 | 字段依赖 | 说明 |
|------|---------|------|
| 按负责人 | `assignee` | 每人 bug 数 + 修复率 |
| 按报告人 | `reporter` | 每人提 bug 数 + 有效率 |
| 按 Bug Type | `customfield_10461` | bug 类型分布 |
| 按端/模块 | `summary` 中的【】标签 | 正则提取模块标签 |
| Reopen 率 | changelog | 状态变更历史分析 |
| Cancel 率 | `status` | 按项目看无效 bug 占比 |

## 快速口诀

| 维度 | 口诀 |
|------|------|
| **API 版本** | v3 POST `/search/jql`，不用 GET（已废弃） |
| **分页** | `maxResults: 500` + `nextPageToken`，循环到 `isLast: true` |
| **Parent** | `parent.key` + `parent.fields.summary`，不是 project |
| **Leak Bug** | `customfield_10224` 是数组，匹配 `value: "Leak Bug"` |
| **趋势** | 新增用 `created`，关闭用 `resolved` 单独查 |
| **输出** | 纯静态 HTML，内联 CSS，Key 带 Jira 链接 |
