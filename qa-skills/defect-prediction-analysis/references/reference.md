# 缺陷预测分析参考手册

> **主文件**：执行流程和输出结构见 [SKILL.md](../SKILL.md)

---

## 1. 数据采集详细规则

### 1.0 MCP 工具速查

**Jira（必须）**：

| 工具 | 用途 |
|------|------|
| `getAccessibleAtlassianResources` | 获取 cloudId |
| `searchJiraIssuesUsingJql` | 查询 Bug（当前项目 + 跨项目） |
| `lookupJiraAccountId` | 查找用户 accountId（用于 reporter 查询） |
| `getJiraIssue` | 获取单个 Bug 详情（如需查看 Description） |

**Lark（可选）**：

| 工具 | 用途 |
|------|------|
| `docx_v1_document_rawContent` | 读取飞书 PRD/TD |
| `wiki_v2_space_getNode` | 获取飞书 Wiki 节点 |

### 1.1 JQL 查询模板

**优先方案（parent 查询）：**
```
JQL: issuetype = Bug AND parent = {EPIC_KEY} ORDER BY created ASC
Fields: summary, status, priority, created, resolution, resolutiondate, assignee, labels, components
```

**备选方案：**
```
JQL: issuetype = Bug AND "Epic Link" = {EPIC_KEY}
JQL: issuetype = Bug AND project = {PROJECT_KEY} AND created >= "{start}" AND created <= "{end}"
```

### 1.2 跨项目 Bug 查询

```
1. 调用 lookupJiraAccountId 查找用户 accountId
2. JQL: issuetype = Bug AND reporter = "{accountId}" ORDER BY created DESC
3. maxResults: 100
4. Fields: summary, status, priority, created, project, parent, labels
```

**截断处理**：若返回恰好 100 条，提示用户可能存在截断，建议缩小时间范围或分页查询。

---

## 2. Bug 标题解析规则

### 2.1 六维度提取方法

Bug 标题是**唯一可靠的信息源**（Description 通常为 null，Labels/Components 通常为空）。

| 维度 | 提取方法 | 示例 |
|------|---------|------|
| **端/平台** | 【app】【h5】【web】等方括号标注；无标注时从内容推断 | 【app】→ App端 |
| **模块** | 【promotion】【alipay】等方括号标注；或从关键词推断 | "购物车" → Cart模块 |
| **现象类型** | 从动词/描述词提取（见下方分类表） | "计算错" → 金额计算错误 |
| **触发条件** | 从条件描述中提取 | "金额>item价值时" → 边界条件 |
| **是否历史问题** | 包含"历史遗留""历史issue" | "历史issue【promotion】..." → 是 |
| **交互模块** | 标题中出现的其他模块 | "promotion+webucks" → Promotion ∩ WeBucks |

### 2.2 现象类型分类表

| 现象类型 | 关键词匹配 |
|---------|-----------|
| **金额计算错误** | 计算错、金额、抵扣、折扣、支付金额、剩余、0.01 |
| **UI/样式问题** | 样式、遮挡、错位、未对齐、图片比例、分辨率、隐藏、显示 |
| **状态管理问题** | 未刷新、未更新、丢失、清除、未记忆、未保持、未生效 |
| **时间/日期错误** | 时间、日期、过期、当天、时区、start date、expiration |
| **接口/请求错误** | 报错、request error、接口、404、loading、加载 |
| **业务规则违反** | 应该、不应该、应互斥、不允许、默认值错、未过滤 |
| **组件加载失败** | 加载不出、不稳定、卡住、转圈、弹窗、组件 |
| **权限/可见性** | 不可见、被屏蔽、无权限、不显示、应隐藏 |

---

## 3. 缺陷模式分析模板

### 3.1 当前项目聚类模板

```markdown
### 按现象类型分布
| 现象类型 | Bug 数量 | 占比 | Bug Keys |
|---------|----------|------|----------|

### 按模块分布
| 模块 | Bug 数量 | 占比 | Bug Keys |
|------|----------|------|----------|

### 按端/平台分布
| 端 | Bug 数量 | 占比 | Bug Keys |
|----|----------|------|----------|

### 交互模块热力图
| 模块 A | 模块 B | Bug 数量 | 典型 Bug |
|--------|--------|----------|---------|
```

### 3.2 跨项目关联模板

```markdown
### 跨项目缺陷模式
| 缺陷模式 | 出现次数 | 涉及 Epic | 典型 Bug | 系统性风险等级 |
|---------|----------|-----------|---------|--------------|
| WeBucks 金额计算组合 | 5 | AliPay, Promotions | SEG-xxxx | 🔴 高 |
```

### 3.3 缺陷 DNA 画像格式

```markdown
### 系统缺陷 DNA 画像

按历史概率排序，以下是本系统最容易出现的 Bug 类型：

1. 🔴 [模式名称] — X 次 / Y 个 Epic — 具体描述
2. 🟡 [模式名称] — ...
3. 🟢 [模式名称] — ...
```

---

## 4. 覆盖差距分析模板

### 4.1 覆盖差距矩阵

```markdown
| 缺陷模式 | 风险等级 | 测试用例覆盖 | 覆盖状态 | 差距描述 |
|---------|---------|------------|---------|---------|
| WeBucks+Promotion 组合计算 | 🔴 高 | 有 2 条用例 | ⚠️ 不足 | 缺少三重组合场景 |
| App 侧滑行为 | 🟡 中 | 无用例覆盖 | ❌ 缺失 | App 端无侧滑测试 |
```

### 4.2 PRD 功能节点风险映射

```markdown
| PRD 功能节点 | 已有 Bug | 匹配缺陷模式 | 测试覆盖 | 预测风险 |
|-------------|---------|-------------|---------|---------|
| 自动选择优惠券 | SEG-9325 | 业务规则逻辑 | 8 条用例 | 🟡 中 |
| Alipay+Promotion 支付 | 无 | 金额计算组合(跨项目) | 0 条用例 | 🔴 极高 |
```

---

## 5. 风险评分规则

### 5.1 评分公式

```
风险分 = 缺陷模式匹配度(0-3) + 跨项目出现频次(0-3) + 覆盖缺口(0-3) + 功能复杂度(0-1)
```

### 5.2 评分细则

| 维度 | 3 分 | 2 分 | 1 分 | 0 分 |
|------|------|------|------|------|
| 缺陷模式匹配度 | 当前项目已有同类 Bug | 跨项目有同类 | 仅理论推断 | 无关联 |
| 跨项目出现频次 | 3+ Epic 出过 | 2 个 Epic | 1 个 Epic | 0 个 |
| 覆盖缺口 | 无用例覆盖 | 用例不足 | 有用例未覆盖边界 | 充分覆盖 |
| 功能复杂度 | - | - | 多模块交互 | 单模块 |

### 5.3 等级映射

| 分数范围 | 等级 | 行动建议 |
|---------|------|---------|
| 8-10 | 🔴 极高风险 | 必须补充测试 |
| 5-7 | 🟠 高风险 | 强烈建议补充 |
| 3-4 | 🟡 中风险 | 建议关注 |
| 0-2 | 🟢 低风险 | 正常关注 |

---

## 6. 注意事项与分析限制

### Bug 数据现实

- **Description 通常为 null** — 不要依赖 Bug 描述字段
- **Labels/Components 通常为空** — 不要依赖结构化分类字段
- **Summary（标题）是唯一可靠信息源** — 所有分析基于标题关键词提取
- **中文标题为主** — 关键词匹配需支持中文

### 分析限制

- 无代码访问权限 — 只能从业务角度推断
- Bug 标题信息有限 — 提取结果需 QA 人工验证
- 跨项目关联是概率推断 — 不同项目同名模块可能实现不同

### 质量保障

- 每个风险预测必须标注**依据来源**（Bug Key / Epic / 用例编号）
- 不做绝对陈述，使用"可能""建议关注"
- 最终结果需 QA 人工审核确认

---

## 7. 实际案例

### 案例：Promotion Upgrade Stage 1

**输入**：Epic SEG-8987（10 Bugs）+ 跨项目 100 Bugs / 12 Epics + 1506 行测试用例 + PRD

**Phase 2 解析结果（10 个 Bug）**：

| Bug Key | 端 | 模块 | 现象类型 | 触发条件 | 历史 | 交互模块 |
|---------|-----|------|---------|---------|------|---------|
| SEG-9299 | App | Cart | 业务规则违反 | 支付方式互斥 | 是 | WeBucks |
| SEG-9310 | App | WeBucks | 组件加载失败 | 充值弹窗 | 是 | - |
| SEG-9311 | 后端 | Promotion | 时间日期错误 | 过期=当天 | 否 | - |
| SEG-9313 | 后端 | Promotion | 金额计算错误 | +WeBucks 组合 | 是 | WeBucks |
| SEG-9314 | 后端 | Promotion | 金额计算错误 | 固定折扣>item价 | 是 | Payment |
| SEG-9317 | 后端 | Promotion | 时间日期错误 | start date=明天 | 否 | - |
| SEG-9318 | 后端 | Promotion | 金额计算错误 | 精度0.01残留 | 是 | - |
| SEG-9324 | App | WeBucks | 权限/可见性 | 报错时隐藏入口 | 是 | Promotion |
| SEG-9325 | 后端 | Promotion | 业务规则违反 | unpaid订单占用 | 是 | Order |
| SEG-9337 | 后端 | Promotion | 金额计算错误 | self-pay+非self | 是 | Payment |

**Phase 3 聚类**：
- 金额计算错误：4 个（40%）
- 时间日期错误：2 个（20%）
- 业务规则违反：2 个（20%）
- 组件加载/可见性：2 个（20%）
- 交互模块热点：WeBucks（3 次）、Payment（2 次）

**Phase 5 预测 Top 3**：
1. 🔴 Promotion + Alipay 支付组合（9/10）— 跨项目强关联 + 0 用例覆盖
2. 🔴 h5/App 响应式下 Promotion 组件适配（8/10）— Item Card 有 14 个同类 Bug
3. 🟠 购物车状态变更后 Promotion 丢失（7/10）— Filter/Banner 有同类模式
