# generate-test-report 详细参考

> 本文档为 SKILL.md 的详细补充，包含完整输入字段、JQL 查询、模板、图表规则和示例。

---

## 1. 输入字段完整表

### 必填项

| 字段 | 说明 | 示例 |
|------|------|------|
| **需求标题** | 功能/需求名称 | Promotion Upgrade stage 1 |
| **Epic/Story 链接** | Jira 或项目管理链接 | https://jira.example.com/PROJ-123 |
| **类型** | Enhancement / New Feature / Bug Fix / Refactoring | Enhancement |
| **发布日期** | 计划发布日期（优先从 Jira 推导） | 2025/2/3 |
| **测试负责人** | QA 负责人 | @Brain Wu |
| **测试周期** | 测试起止日期（优先从 Jira 推导） | 2025/2/4 ~ 2025/2/9 |
| **功能范围** | 本次覆盖的功能描述 | 简要描述 |
| **未覆盖功能** | 不在范围内的功能及原因 | N/A 或列表 |
| **平台** | web / h5 / app / all | web/h5/app |
| **测试环境** | OS、浏览器、设备、网络 | 见模板 |
| **用例统计** | 总数/已执行/通过/失败/阻塞 | 53 / 53 / 48 / 5 / 0 |
| **Jira Epic Key** | Jira Epic 或项目 Key | PROJ-123 |
| **Bug 数量与严重性** | 从 Jira 自动获取或手动输入 | 10 bugs found |
| **Bug 趋势** | 从 Jira 自动获取或手动输入 | Feb 4-8, 10 bugs |
| **未解决缺陷** | 从 Jira 自动获取或手动输入 | N/A 或列表 |
| **潜在风险** | 已知发布风险 | 无风险 / 风险列表 |
| **质量评级** | 自动计算或手动覆盖 | A |
| **发布建议** | 自动判定或手动覆盖 | Go Live |

### 可选项

| 字段 | 说明 |
|------|------|
| **缺陷统计图** | Bug 严重性分布图 |
| **缺陷趋势图** | Bug 趋势图 |
| **Lark Base/Sheet 链接** | 用例管理表链接 |
| **用例文档链接** | 详细用例文档链接 |

---

## 2. Jira 查询与日期推导

### 2.1 获取 Atlassian Cloud ID

```
1. 调用 getAccessibleAtlassianResources 获取 cloudId
2. 缓存 cloudId 供后续所有 Jira 调用使用
```

### 2.2 查找 Epic 并从子任务推导日期

**重要：Epic 的 due date 不可靠，必须从子任务推导日期。**

```
1. 查找 Epic：
   JQL: issuetype in (Epic, 长篇故事) AND summary ~ "{feature_name}"
   → 获取 EPIC_KEY（如 SEG-8987）

2. 查询 Epic 下所有子任务（不限于当前用户）：
   JQL: parent = {EPIC_KEY} AND issuetype != Bug ORDER BY duedate DESC
   Fields: summary, duedate, customfield_10015 (start date), status, assignee

3. 识别任务类型：
   - 测试任务：summary 包含 "test" / "测试" / "QA"
   - 开发任务：summary 包含 "develop" / "开发" / "self-testing" / "联调"
   - 评审任务：summary 包含 "review" / "评审"
   - 发布任务：summary 包含 "release" / "deploy" / "上线" / "发布"

4. 从任务推导日期（不要用 Bug 日期）：
   - 测试周期开始 = 测试任务的 start date (customfield_10015)
   - 测试周期结束 = 测试任务的 duedate - 1 天（或 duedate 前最后一个工作日）
   - 发布日期 = 测试任务的 duedate
   - 测试负责人 = 分配给用户的测试任务的 assignee

   **禁止用 Bug 的 created/resolved 日期来判定测试周期。**
   **Bug 可能不在测试首日/末日产生，任务日期才是真实来源。**

5. 交叉参考其他任务：
   - 开发完成日期 = 开发任务中最晚的 duedate
   - 自测完成 = 开发自测任务的 duedate
   - 提测日期 = 评审/提测任务的日期
   - 若测试任务无 start date，用提测日期或开发自测 duedate + 1 天
```

### 2.3 查询 Epic 下所有 Bug

**始终用 `parent = {EPIC_KEY}` 查询 Bug，不要用 summary 文本搜索。**

**主要方式（parent）：**
```
JQL: issuetype = Bug AND parent = {EPIC_KEY}
Fields: summary, status, priority, created, resolution, resolutiondate, assignee
```

**回退方式（Epic Link）：**
```
JQL: issuetype = Bug AND "Epic Link" = {EPIC_KEY}
Fields: summary, status, priority, created, resolution, resolutiondate, assignee
```

**兜底方式（日期范围）：**
```
JQL: issuetype = Bug AND project = {PROJECT_KEY}
     AND created >= "{start_date}" AND created <= "{end_date}"
Fields: summary, status, priority, created, resolution, resolutiondate, assignee
```

### 2.4 Bug 统计聚合

从查询结果中计算：

```
1. Bug 总数
2. 按优先级分组：
   - P0 (Highest/Blocker): count
   - P1 (High/Critical): count
   - P2 (Medium/Major): count
   - P3 (Low/Minor): count
   - P4 (Trivial): count
3. 按状态分组：
   - Open / To Do: count
   - In Progress: count
   - Resolved / Done: count
   - Closed: count
4. 未解决 Bug 列表：
   - 每条: Key | Summary | Priority | Status | Assignee
5. 按创建日期的 Bug 趋势：
   - 按日聚合，展示每日新增趋势
```

### 2.5 缺陷分布表（报告 4.1 节）

```markdown
| 优先级 | 数量 | 已解决 | 未解决 | 解决率 |
|--------|:----:|:------:|:------:|:------:|
| P0 (Blocker) | x | x | x | xx% |
| P1 (Critical) | x | x | x | xx% |
| P2 (Major) | x | x | x | xx% |
| P3 (Minor) | x | x | x | xx% |
| **合计** | **x** | **x** | **x** | **xx%** |
```

### 2.6 Bug 趋势表（报告 4.2 节）

```markdown
| 日期 | 新增 | 已解决 | 剩余未关闭 |
|------|:----:|:------:|:----------:|
| Feb 4 | 3 | 0 | 3 |
| Feb 5 | 2 | 1 | 4 |
| ... | ... | ... | ... |
```

### 2.7 未解决缺陷列表（报告第 5 节）

```markdown
| # | Jira Key | Summary | Priority | Status |
|---|----------|---------|----------|--------|
| 1 | PROJ-456 | Description... | P1 | Open |
| 2 | PROJ-789 | Description... | P2 | In Progress |
```

无未关闭 Bug 时输出 "N/A"。

---

## 3. 质量评级详细规则

**参考来源**：[Test Report Template](https://webox-inc.sg.larksuite.com/wiki/CTGbwOBbfijQizkfmSoloUKHgJh)

### 3.1 结果指标（短板原则：最终等级 = 三维度最低值）

| 等级 | 用例通过率 | P0 & P1 缺陷 | 新增 Bug 数 | 描述 |
|------|:----------:|:------------:|:-----------:|------|
| **A（优秀）** | ≥ 95% | P0=P1=0 | ≤ 10 | 质量高，稳定，无关键问题 |
| **B（良好）** | 90%~95% | P0=0, P1≤2 | (10, 20] | 基本稳定，少量关键问题有规避方案 |
| **C（一般）** | 85%~90% | P0=0, P1≤5 | (21, 40] | 存在质量风险，多个关键问题需改进 |
| **D（差）** | < 85% | P0>0 或 P1>5 | > 40 | 不可接受，应阻止发布 |

### 3.2 发布门禁检查项

| 门禁项 | 不达标标准 |
|--------|-----------|
| 核心用户流程体验 | 核心用户流程存在明显体验缺陷 |
| 性能与稳定性 | 存在明显性能下降或稳定性风险 |
| 高频场景覆盖 | 高频场景未覆盖或无法回归 |
| 已知风险缓解 | 已知风险无缓解或回退方案 |

### 3.3 门禁应用规则

| 门禁结果 | 等级处理 |
|----------|----------|
| 全部达标 | 维持当前等级 |
| ≥1项不达标 | 最高可评 B |
| ≥2项不达标 | 降一级 |
| 存在核心体验风险 | 直接评 D |

### 3.4 发布建议逻辑

| 等级 | 建议 |
|------|------|
| A 或 B | **Go Live** |
| C | **Fix Before Release**（列出待修复项） |
| D | **Do Not Release** |

### 3.5 计算流程

```
1. 执行率 = (已执行 / 总数) × 100
2. 通过率 = (通过 / 总数) × 100
3. 从 Jira 数据获取：
   - 测试周期内发现的 Bug 总数
   - 按优先级统计未关闭 Bug（P0=Highest, P1=High）
   - 总体解决率

4. 质量评级计算（短板原则）：
   维度1：用例通过率 → A/B/C/D
   维度2：P0 & P1 缺陷 → A/B/C/D
   维度3：新增 Bug 数 → A/B/C/D
   结果等级 = min(维度1, 维度2, 维度3)

5. 发布门禁检查（覆盖结果等级）：
   对 4 项门禁逐项评估 → 应用覆盖规则
   最终等级 = 门禁覆盖后的结果

6. 发布建议：
   A/B → Go Live | C → Fix Before Release | D → Do Not Release
```

---

## 4. 图表生成规则

使用 matplotlib（通过 python venv）生成两张图：

### 环境准备

```bash
python3 -m venv /tmp/chart-venv
source /tmp/chart-venv/bin/activate && pip install matplotlib
```

### 图表 1：缺陷分布饼图

- **文件**：`docs/{feature-name}-defect-statistics.png`
- **数据**：按严重性的 Bug 数量（Highest / High / Medium / Low）
- **样式**：饼图
- **配色**：`#FF4D4F`（Highest）、`#FFA940`（High）、`#FADB14`（Medium）、`#52C41A`（Low）
- 仅显示非零切片
- 包含百分比标签和汇总文本

### 图表 2：缺陷趋势柱状+折线图

- **文件**：`docs/{feature-name}-defect-trend.png`
- **数据**：每日新增 Bug（红色柱状）、已解决 Bug（绿色柱状）、累计未关闭（蓝色折线）
- **X 轴**：测试周期内的日期
- 柱状和折线点包含数值标签
- **标题**：`"Defect Trend ({start_date} - {end_date})"`

---

## 5. HTML 报告模板

**输出格式为 HTML**（用于粘贴到 Lark 邮件，保留富文本格式）。

### 使用方式

1. 生成 HTML 文件：`docs/{feature-name}-test-report.html`
2. 使用语义化 HTML：`<h1>`, `<h2>`, `<h3>`, `<p>`, `<table>`, `<a>`
3. 图表位置：使用占位文本 `[插入xxx图 filename.png]`
4. 用户手动将生成的 PNG 文件拖入邮件
5. 同时保留 `.md` 版本供本地参考
6. 自动在浏览器中打开：`open docs/{feature-name}-test-report.html`

### HTML 模板

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
    font-size: 14px; color: #333; line-height: 1.6;
    max-width: 800px; margin: 20px auto;
  }
  h1 { font-size: 20px; font-weight: bold; margin-bottom: 4px; }
  h2 { font-size: 16px; font-weight: bold; margin-top: 16px; margin-bottom: 4px; }
  h3 { font-size: 14px; font-weight: bold; margin-top: 12px; margin-bottom: 4px; }
  p { margin: 2px 0; }
  table { border-collapse: collapse; margin: 8px 0; }
  th, td { border: 1px solid #d9d9d9; padding: 6px 12px; text-align: center; font-size: 14px; }
  th { background-color: #f5f5f5; font-weight: bold; }
  a { color: #1677ff; text-decoration: none; }
  .placeholder { color: #999; font-style: italic; margin: 8px 0; }
</style>
</head>
<body>
  <h1>{Title} Test Report</h1>
  <p>Hello Tech Infrastructure Team Members,</p>
  <p>This email serves as the test report for "{Title}",
     with relevant information outlined below:</p>

  <h2>1. Release Information</h2>
  <!-- 发布信息表格：需求标题/Epic链接/类型/发布日期/测试负责人/测试周期 -->

  <h2>2. Test Scope</h2>
  <h3>2.1 Functional Scope</h3>
  <!-- 功能范围 + 未覆盖功能 -->
  <h3>2.2 Platform / Environment Scope</h3>
  <!-- 平台 + 测试环境详情 -->

  <h2>3. Test Case Execution Summary</h2>
  <!-- 用例统计表：总数/已执行/通过/失败/阻塞/执行率/通过率 -->

  <h2>4. Defect Analysis</h2>
  <h3>4.1 Defect Statistics</h3>
  <p class="placeholder">[插入缺陷分布饼图 {feature}-defect-statistics.png]</p>
  <!-- 缺陷分布表格 -->
  <h3>4.2 Defect Trend &amp; Concentration</h3>
  <p class="placeholder">[插入缺陷趋势图 {feature}-defect-trend.png]</p>
  <!-- 缺陷趋势表格 + 描述 -->

  <h2>5. Outstanding Issues &amp; Risks</h2>
  <!-- 未解决缺陷列表 + 潜在风险 -->

  <h2>6. Test Conclusion</h2>
  <!-- 质量评级 / 是否达标 / 发布建议 -->
</body>
</html>
```

---

## 6. 报告 Markdown 模板

```markdown
# {需求标题} Test Report

Hello Tech Infrastructure Team Members,

This email serves as the test report for "{需求标题}",
with relevant information outlined below:

## 1. Release Information

| Item | Detail |
|------|--------|
| **Requirement Title** | {title} |
| **Epic/Story Link** | {link} |
| **Type** | {type} |
| **Release Date** | {date} |
| **Test Owner** | {owner} |
| **Test Period** | {start} ~ {end} |

## 2. Test Scope

### 2.1 Functional Scope

**Features covered in this release:**
{functional_description}

**Features not covered (with reasons):**
{not_covered_or_NA}

### 2.2 Platform / Environment Scope

**Platforms:** {platforms}

**Test Environment:**
- OS: {os_version}
- Browser / App Version: {browser_version}
- Hardware / Network: {hardware_details}

## 3. Test Case Execution Summary

| Total Cases | Executed | Passed | Failed | Blocked | Execution Rate | Pass Rate |
|:-----------:|:--------:|:------:|:------:|:-------:|:--------------:|:---------:|
| {total} | {executed} | {passed} | {failed} | {blocked} | {exec_rate}% | {pass_rate}% |

## 4. Defect Analysis

### 4.1 Defect Statistics

{defect_statistics_description_or_image}

### 4.2 Defect Trend & Concentration

{defect_trend_description}

During the test from {start_date} to {end_date}, {bug_count} bugs were found.

## 5. Outstanding Issues & Risks

**Unresolved Defects:**
{unresolved_defects_or_NA}

**Potential Risks:**
{risks_or_no_risk}

## 6. Test Conclusion

| Item | Result |
|------|--------|
| **Quality Rating** | {rating} |
| **Meets Release Criteria** | {yes_or_no} |
| **Release Recommendation** | {recommendation} |
```

---

## 7. MCP 工具速查

### Jira（Atlassian）— Bug 查询

| 工具 | 用途 |
|------|------|
| `getAccessibleAtlassianResources` | 获取 Atlassian cloudId（所有 Jira 调用前必须先执行） |
| `searchJiraIssuesUsingJql` | 按 Epic、标签、日期范围或 Sprint 查询 Bug |
| `getJiraIssue` | 获取单个 Bug 的详细信息 |
| `getVisibleJiraProjects` | 列出项目，帮助用户确认正确的项目 Key |

### Lark — 文档发布

| 工具 | 用途 |
|------|------|
| `docx_builtin_import` | 将报告发布为 Lark 文档 |
| `docx_v1_document_rawContent` | 读取 Lark 上已有的测试报告 |
| `drive_v1_permissionMember_create` | 与团队成员共享报告 |
| `bitable_v1_appTableRecord_search` | 从 Lark Base 获取用例统计 |

### 通用

| 工具 | 用途 |
|------|------|
| `AskQuestion` | 结构化收集用户输入 |

---

## 8. 典型场景示例

### 示例 1：Jira 全自动

```
用户：帮我写 Promotion Upgrade 的测试报告，Epic 是 PROJ-123

AI 执行：
1. getAccessibleAtlassianResources → 获取 cloudId
2. searchJiraIssuesUsingJql:
   JQL: issuetype = Bug AND parent = PROJ-123
   fields: summary, status, priority, created, resolution, resolutiondate
3. 聚合：10 bugs，8 resolved，2 open，P0:0, P1:2, P2:5, P3:3
4. 询问用户：用例统计、环境信息
5. 计算指标 + 质量评级
6. 生成完整报告（含 Jira 数据的缺陷表格）
7. 保存至 docs/ 并在浏览器中打开
```

### 示例 2：手动数据

```
用户：我要提交 Promotion 功能的测试报告
     53 条用例，48 通过，5 失败，Feb 4-8 发现 10 个 bug

AI 执行：
1. 计算：执行率 = 100%，通过率 = 90.56%
2. 询问："有 Jira Epic Key 吗？我可以自动查询 bug 详情。"
3. 有 → 查询 Jira 获取详细 bug 分布
4. 无 → 使用手动提供的 "10 bugs" 数量
5. 生成完整报告
```

### 示例 3：日期范围查询

```
用户：生成 Sprint 42 测试报告，项目 Key 是 WEBOX，测试周期 Feb 1-14

AI 执行：
1. 获取 cloudId
2. JQL: issuetype = Bug AND project = WEBOX
        AND created >= "2025-02-01" AND created <= "2025-02-14"
3. 聚合 bug 统计
4. 结合用户提供的用例数据
5. 生成报告
```

---

## 9. 交付质量检查清单

交付报告前逐项验证：

- [ ] 6 个章节全部存在且填充完整
- [ ] 用例统计数据正确（通过+失败+阻塞=总数）
- [ ] 执行率和通过率计算正确
- [ ] 质量评级与评级标准表一致
- [ ] 发布建议与评级和未关闭缺陷一致
- [ ] 环境详情包含所有已测平台
- [ ] 缺陷分析章节有趋势描述
- [ ] 遗留问题准确反映当前 Bug 状态
- [ ] 报告语言全文一致
