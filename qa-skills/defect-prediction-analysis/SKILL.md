---
name: defect-prediction-analysis
description: 基于已有缺陷（Jira Bug）、PRD、技术设计文档和测试用例，分析缺陷模式并预测潜在缺陷区域。用于用户要求做缺陷预测、Bug 分析、风险区域识别、或提供 Jira Epic 要求分析时。
---

# 缺陷预测分析

## 适用场景

用户提供 Jira Epic/Bug 数据 + PRD/TD/测试用例，需要产出缺陷模式画像、风险区域排序和补充测试建议。

## 规则依赖

**本 skill 为独立分析工具**，不依赖 `core-rules.md`，使用独立评分模型。

**MCP 前置**：需配置 Atlassian MCP（Jira 查询）。未配置时用户可手动提供 Bug 列表，跳过 Phase 1。Lark MCP 可选。

## 输入要求

| 输入 | 必须 | 来源 |
|------|------|------|
| Jira Bug 列表 | ✅ | Jira MCP 查询 / 用户提供 CSV（至少 Summary + Priority + Created） |
| PRD | ✅ | 用户提供链接或文件 |
| Test Cases | ✅ | 用户提供文件 |
| TD（技术设计） | 推荐 | 用户提供 |
| 跨项目 Bug 历史 | 推荐 | Jira MCP 查询 reporter 全量 Bug |

## 执行流程（AI必读）

### Phase 1: 数据采集
1. 调用 `getAccessibleAtlassianResources` 获取 cloudId
2. 查询当前项目 Bug（优先 `parent = {EPIC_KEY}`，备选 `"Epic Link"`）
3. 查询跨项目 Bug（`reporter = "{accountId}"`，maxResults: 100）

> JQL 模板、备选方案、截断处理见 [reference.md §1](references/reference.md#1-数据采集详细规则)

### Phase 2: Bug 标题解析
Bug 标题是**唯一可靠信息源**（Description/Labels/Components 通常为空）。

**从每个标题提取 6 维度**：端/平台、模块、现象类型、触发条件、是否历史问题、交互模块

> 6 维度提取方法、现象类型分类表见 [reference.md §2](references/reference.md#2-bug-标题解析规则)

### Phase 3: 缺陷模式分析
1. **当前项目聚类**：按 现象类型 / 模块 / 端 三维统计 + 交互模块热力图
2. **跨项目关联**（如有）：按 Epic 分组，识别跨 Epic 重复缺陷模式
3. **缺陷 DNA 画像**：综合排名系统最易出现的 Bug 类型（🔴高 / 🟡中 / 🟢低）

> 聚类模板、DNA 画像格式见 [reference.md §3](references/reference.md#3-缺陷模式分析模板)

### Phase 4: 覆盖差距分析
1. **提取测试用例覆盖范围**：功能模块 / 端 / 业务场景 / 边界条件 / 异常场景
2. **覆盖差距矩阵**：缺陷模式 vs 用例覆盖（✅充分 / ⚠️不足 / ❌缺失）
3. **PRD 功能节点风险映射**：已出 Bug → 加强回归；模式相似未出过 → 高预测风险

> 矩阵模板、PRD 映射表见 [reference.md §4](references/reference.md#4-覆盖差距分析模板)

### Phase 5: 风险预测与建议
**风险评分**（0-10 分）= 缺陷模式匹配度(0-3) + 跨项目频次(0-3) + 覆盖缺口(0-3) + 功能复杂度(0-1)

**等级映射**：8-10 🔴极高 / 5-7 🟠高 / 3-4 🟡中 / 0-2 🟢低

> 评分细则见 [reference.md §5](references/reference.md#5-风险评分规则)

## 快速口诀

| 维度 | 口诀 |
|------|------|
| **数据源** | Bug 标题是唯一可靠信息源，不依赖 Description/Labels |
| **解析6维** | 端 / 模块 / 现象类型 / 触发条件 / 历史问题 / 交互模块 |
| **分析3层** | 当前聚类 → 跨项目关联 → 缺陷 DNA 画像 |
| **评分4项** | 模式匹配度 + 跨项目频次 + 覆盖缺口 + 功能复杂度 |
| **不做假设** | 每个预测标注依据来源，不做绝对陈述 |

**质量门槛**：
- ✓ 每个风险预测标注依据来源（Bug Key / Epic / 用例编号）
- ✓ 不做"一定会出 Bug"的绝对陈述，使用"可能""建议关注"
- ✓ 最终结果需 QA 人工审核确认

## 输出结构

按以下 6 个章节输出缺陷预测分析报告：

1. **数据概览** — 当前项目 Bug 数量 / 跨项目 Bug 数量 / Epic 数量 / 测试用例总数
2. **Bug 标题解析表** — Phase 2 的 6 维度解析结果
3. **缺陷模式分析** — 3.1 当前项目聚类 / 3.2 跨项目关联 / 3.3 系统缺陷 DNA
4. **覆盖差距分析** — 4.1 覆盖差距矩阵 / 4.2 PRD 功能节点映射
5. **风险预测结果** — 风险区域排序表 + 建议补充测试方向表
6. **总结** — 极高/高风险区域数 + 建议补充用例数 + 关键发现

> 各章节详细表格模板见 [reference.md §3-4](references/reference.md#3-缺陷模式分析模板)

## 核心示例

**输入**：Epic SEG-8987（10 Bugs）

**Phase 2 解析（摘要）**：

| Bug Key | 端 | 模块 | 现象类型 | 触发条件 | 历史 | 交互模块 |
|---------|-----|------|---------|---------|------|---------|
| SEG-9313 | 后端 | Promotion | 金额计算错误 | +WeBucks 组合 | 是 | WeBucks |
| SEG-9314 | 后端 | Promotion | 金额计算错误 | 固定折扣>item价 | 是 | Payment |
| SEG-9311 | 后端 | Promotion | 时间日期错误 | 过期=当天 | 否 | - |

**Phase 3 聚类**：金额计算错误 4 个（40%）、交互模块热点 WeBucks（3 次）

**Phase 5 预测 Top 1**：
🔴 Promotion + Alipay 支付组合（9/10）— 跨项目强关联 + 0 用例覆盖 → 建议补充组合计算测试

> 完整案例见 [reference.md §7](references/reference.md#7-实际案例)

## 参考资源

- [reference.md](references/reference.md) — 解析规则、评分模型、输出模板、实际案例
- [core-rules.md](../_shared/core-rules.md) — QA 共享规范（本 skill 不依赖，可作风险维度参考）
