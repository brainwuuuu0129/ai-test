---
name: generate-test-report
description: Generate standardized test reports for feature releases. Use when user needs test report, release summary, QA sign-off, or mentions 测试报告, test report, 发布报告.
---

# 生成测试报告

## 适用场景

用户需要为需求/功能发布生成标准化测试报告，适用于邮件发送和 Lark 文档发布。

**触发示例**：
- "帮我写一份 XXX 的测试报告"
- "生成这个功能的测试报告"
- "I need to submit a test report for XXX"

## 规则依赖

**本 skill 使用以下外部工具**：
- Jira MCP（Bug 自动查询）
- Lark MCP（文档发布）
- matplotlib（图表生成）

**读取时机**：执行前读取 [reference.md](references/reference.md) 获取详细规则

## 执行流程（AI必读）

### Step 1: 收集基本信息

通过 `AskQuestion` 或对话方式收集必要输入：

| 分类 | 必填项 |
|------|--------|
| **发布信息** | 需求标题、类型（Enhancement/New Feature/Bug Fix）、Epic/Story 链接 |
| **测试信息** | 测试负责人、用例统计（总数/通过/失败/阻塞） |
| **环境信息** | 平台（web/h5/app）、OS/浏览器/设备 |
| **Jira Key** | Epic Key 或项目 Key（用于自动查询 Bug） |

**关键规则**：日期（发布日期、测试周期）从 Jira 子任务自动推导，不要手动询问用户

> 完整输入字段表见 [reference.md §1](references/reference.md#1-输入字段完整表)

### Step 2: Jira 自动查询

1. 调用 `getAccessibleAtlassianResources` 获取 cloudId
2. 查找 Epic → 查询所有子任务 → 从测试任务推导日期
3. 查询 Bug：优先 `parent = EPIC_KEY`，回退 `Epic Link`，最后按日期范围
4. 聚合统计：按优先级/状态分组，生成缺陷分布表和趋势表

> JQL 详细语句、日期推导逻辑、Bug 聚合规则见 [reference.md §2](references/reference.md#2-jira-查询与日期推导)

### Step 3: 计算指标与质量评级

```
执行率 = (已执行 / 总数) × 100%
通过率 = (通过 / 总数) × 100%
```

**质量评级（短板原则：最终等级 = 三维度最低值）**：

| 等级 | 用例通过率 | P0 & P1 缺陷 | 新增 Bug 数 |
|------|:----------:|:------------:|:-----------:|
| **A** | ≥ 95% | P0=P1=0 | ≤ 10 |
| **B** | 90%~95% | P0=0, P1≤2 | (10, 20] |
| **C** | 85%~90% | P0=0, P1≤5 | (21, 40] |
| **D** | < 85% | P0>0 或 P1>5 | > 40 |

**发布门禁（覆盖评级结果）**：

| 门禁结果 | 处理方式 |
|----------|----------|
| 全部达标 | 维持当前等级 |
| ≥1项不达标 | 最高只能评 B |
| ≥2项不达标 | 降一级 |
| 存在核心体验风险 | 直接评 D |

**发布建议**：A/B → Go Live | C → Fix Before Release | D → Do Not Release

> 门禁检查项、评级详细规则见 [reference.md §3](references/reference.md#3-质量评级详细规则)

### Step 4: 生成图表

使用 matplotlib 生成两张图：
- **缺陷分布饼图**：`docs/{feature}-defect-statistics.png`
- **缺陷趋势图**（柱状+折线）：`docs/{feature}-defect-trend.png`

> 配色、样式、代码模板见 [reference.md §4](references/reference.md#4-图表生成规则)

### Step 5: 生成报告

**输出格式为 HTML**（用于粘贴到 Lark 邮件，保留富文本格式）

1. 生成 `docs/{feature}-test-report.html`
2. 同时保留 `.md` 版本供本地参考
3. 自动在浏览器中打开 HTML

> HTML 模板、样式规则见 [reference.md §5](references/reference.md#5-html-报告模板)

### Step 6: 交付用户

**必须展示以下操作指引**：
```
报告已生成，请按以下步骤操作：
1. 在浏览器中 Cmd+A 全选 → Cmd+C 复制
2. 粘贴到 Lark 邮件中
3. ⚠️ 请手动将以下图片拖入邮件中对应的占位位置：
   - docs/{feature}-defect-statistics.png（缺陷分布饼图 → 替换 4.1 位置）
   - docs/{feature}-defect-trend.png（缺陷趋势图 → 替换 4.2 位置）
```

## 快速口诀

| 维度 | 口诀 |
|------|------|
| **日期来源** | 从 Jira 子任务推导，不问用户 |
| **Bug 查询** | parent → Epic Link → 日期范围（三级回退） |
| **质量评级** | 短板原则：通过率 × P0P1 × Bug数 取最低 |
| **门禁覆盖** | 核心体验风险 → 直接 D |
| **输出格式** | HTML（邮件粘贴）+ MD（本地参考）+ 2张 PNG |

## 输出结构

报告固定 6 章节：

1. **发布信息** — 需求标题/Epic链接/类型/发布日期/测试负责人/测试周期
2. **测试范围** — 功能范围（覆盖/未覆盖）+ 平台/环境
3. **用例执行概况** — 总数/已执行/通过/失败/阻塞/执行率/通过率
4. **缺陷分析** — 4.1 缺陷分布（饼图+表格）+ 4.2 缺陷趋势（柱状图+表格）
5. **遗留问题与风险** — 未关闭缺陷列表 + 潜在风险
6. **测试结论** — 质量评级/是否达标/发布建议

> 完整 Markdown 报告模板见 [reference.md §6](references/reference.md#6-报告-markdown-模板)

---

## 信息缺失处理

| 缺失项 | 处理方式 |
|--------|----------|
| 用例统计 | 直接询问 总数/通过/失败/阻塞 |
| 环境信息 | 提供常见默认值，请用户确认 |
| Bug 数据 | 有 Jira Key → 自动查询；无 → 询问用户 |
| 日期信息 | 有 Epic → 从子任务推导；无 → 询问用户 |
| 风险信息 | 默认"无风险"，但需用户确认 |

---

## 参考资源

- [reference.md](references/reference.md) — JQL 查询、HTML 模板、图表规则、完整示例
- Jira MCP 工具：`getAccessibleAtlassianResources` / `searchJiraIssuesUsingJql` / `getJiraIssue`
- Lark MCP 工具：`docx_builtin_import` / `drive_v1_permissionMember_create`
