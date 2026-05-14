# 周上线通知 — 详细参考

## 1. 文档模板（英文）

```
Weekly Release Notification — {Team Name}

1. Release Overview
   • Team: {Team Name}
   • Release Period: {Start Date} ~ {End Date}
   • Release Date: {YYYY/MM/DD}
   • Total Items Released: {number}

2. Release Items

2.1 {Feature / Change Title A}
   • Type: New Feature / Enhancement / Bug Fix / Config Change
   • Owner: {optional, fill in if required}
   • Overview:
     ◦ {1-2 sentences describing the background and objective}
   • Key Changes:
     ◦ {Specific change point 1}
     ◦ {Specific change point 2}
     ◦ {Specific change point 3}
   • Impact Scope:
     ◦ Platforms: {Web / H5 / Android / iOS / All}
     ◦ User-facing: {Yes / No}

2.2 {Feature / Change Title B}
   • Type: Enhancement
   • Overview:
     ◦ {1-2 sentences describing the background and objective}
   • Key Changes:
     ◦ {Specific change point 1}
     ◦ {Specific change point 2}
   • Impact Scope:
     ◦ Platforms: {Web}
     ◦ User-facing: {Yes}

2.3 {Bug Fix Title C}
   • Type: Bug Fix
   • Overview:
     ◦ {What was the issue and how it was fixed}
   • Key Changes:
     ◦ {Fix detail 1}
     ◦ {Fix detail 2}
   • Impact Scope:
     ◦ Platforms: {iOS / Android}
     ◦ User-facing: {Yes}

(Continue numbering 2.4, 2.5... for additional items)

3. Outstanding Issues & Known Limitations
   • {Issue description 1} — {Impact & workaround if any}
   • {Issue description 2} — {Impact & workaround if any}
   • (If none, write: No outstanding issues for this release.)

4. Notes
   • {Any additional context, rollout plan, feature flag status, or follow-up items}
   • (If none, write: N/A)
```

## 2. 文档模板（中文）

```
周上线通知 — {团队名称}

1. 版本信息
   • 团队：{团队名称}
   • 上线周期：{开始日期} ~ {结束日期}
   • 上线日期：{YYYY/MM/DD}
   • 上线条目总数：{数量}

2. 上线条目

2.1 {功能/变更标题 A}
   • 类型：新功能 / 功能优化 / 缺陷修复 / 配置变更
   • 负责人：{可选，需要时填写}
   • 概述：
     ◦ {1-2 句话描述变更的背景和目标}
   • 主要变更：
     ◦ {具体变更点 1}
     ◦ {具体变更点 2}
     ◦ {具体变更点 3}
   • 影响范围：
     ◦ 平台：{Web / H5 / Android / iOS / 全部}
     ◦ 用户可感知：{是 / 否}

2.2 {功能/变更标题 B}
   • 类型：功能优化
   • 概述：
     ◦ {1-2 句话描述变更的背景和目标}
   • 主要变更：
     ◦ {具体变更点 1}
     ◦ {具体变更点 2}
   • 影响范围：
     ◦ 平台：{Web}
     ◦ 用户可感知：{是}

2.3 {缺陷修复标题 C}
   • 类型：缺陷修复
   • 概述：
     ◦ {问题是什么，如何修复的}
   • 主要变更：
     ◦ {修复细节 1}
     ◦ {修复细节 2}
   • 影响范围：
     ◦ 平台：{iOS / Android}
     ◦ 用户可感知：{是}

（继续编号 2.4、2.5... 添加更多条目）

3. 遗留问题与已知限制
   • {问题描述 1} — {影响及临时方案}
   • {问题描述 2} — {影响及临时方案}
   • （如无，填写：本次上线无遗留问题。）

4. 备注
   • {补充说明、灰度计划、Feature Flag 状态或后续跟进事项}
   • （如无，填写：无）
```

## 3. 完整示例

```
Weekly Release Notification — Marketplace Team

1. Release Overview
   • Team: Marketplace Team
   • Release Period: Mar 31 ~ Apr 4, 2026
   • Release Date: 2026/04/04
   • Total Items Released: 3

2. Release Items

2.1 Skip FTUE Optimization
   • Type: Enhancement
   • Overview:
     ◦ Based on customer feedback, the FTUE flow was too lengthy and causing new user drop-off. We now allow users to skip the last two steps instead of requiring mandatory completion.
   • Key Changes:
     ◦ The last two FTUE steps are now optional; users can tap Skip to go directly to the homepage.
     ◦ All existing step functionalities remain unchanged; only the mandatory restriction is removed.
     ◦ Users who skip can still configure related settings later from their account page.
   • Impact Scope:
     ◦ Platforms: Web / H5
     ◦ User-facing: Yes

2.2 Cart Price Display Fix
   • Type: Bug Fix
   • Overview:
     ◦ Fixed an issue where the cart total did not update correctly when switching between shipping time slots.
   • Key Changes:
     ◦ Cart total now recalculates immediately when the user changes the shipping date or time slot.
     ◦ A loading indicator is displayed during recalculation to prevent user confusion.
   • Impact Scope:
     ◦ Platforms: All
     ◦ User-facing: Yes

2.3 Promotion Auto-Apply Enhancement
   • Type: Enhancement
   • Overview:
     ◦ Improved the auto-apply logic to handle edge cases when multiple promotions share the same expiration date.
   • Key Changes:
     ◦ When multiple auto-applicable promotions share the same expiration date, the one with the higher discount value is now prioritized.
     ◦ If both expiration date and discount value are identical, one is randomly selected.
     ◦ Auto-apply judgment is based on order time, not the selected shipping date.
   • Impact Scope:
     ◦ Platforms: All
     ◦ User-facing: Yes

3. Outstanding Issues & Known Limitations
   • No outstanding issues for this release.

4. Notes
   • N/A
```

## 4. 编写规则详细说明

### 4.1 变更分类定义

| 类型 | 英文 | 适用场景 |
|------|------|----------|
| 新功能 | New Feature | 全新的功能模块，之前不存在 |
| 功能优化 | Enhancement | 对已有功能的改进、体验优化 |
| 缺陷修复 | Bug Fix | 修复已知的功能缺陷 |
| 配置变更 | Config Change | 系统配置、参数调整，无代码逻辑变更 |

### 4.2 Overview 写作规则

- 1-2 句话，不超过 50 词
- 第一句说背景（为什么做）：客户反馈 / 业务需求 / 体验问题
- 第二句说目标（做了什么）：解决什么问题 / 达到什么效果
- 不要重复 Key Changes 的内容

### 4.3 Key Changes 写作规则

- 每条一个具体变更点，描述用户可感知的行为变化，不描述内部实现
- **总数控制在 3-5 条**，超过时将逻辑相关的细节合并为一条
- **按用户操作顺序排列**：先写触发条件/入口变化，再写核心行为变化，最后写兜底/边界说明
- 同一个操作的多个细节合并为一条（如"用户跳过后可在账户页补充设置"不单独列条，并入主变更）
- 如果现有行为未变，明确说明（如 "All existing functionalities remain unchanged"）放在最后一条
- 一条一个动作，不要用分号连接多个变更

**判断是否过散的标准**：如果相邻两条描述的是同一个用户动作的不同阶段，合并为一条。

### 4.4 不要包含的内容

- 负责人姓名（除非用户要求）
- 测试情况、回滚方案等技术细节（属于 Test Report）
- Jira ticket 编号或链接
- QA 评级或缺陷统计（属于 Test Report）
- Affected Platforms 单独章节（融入各条目的 Impact Scope）

## 5. Word 文档生成

如用户需要 Word 格式，使用 python-docx 生成：

```python
# 依赖：pip install python-docx
# 样式规范：
# - 大标题：Arial 18pt, 蓝色 #1F4E79, 居中
# - 章节标题：Arial 14pt, 蓝色 #2E74B5
# - 子章节标题：Arial 12pt, 深灰 #333333
# - 正文：Arial 11pt
# - 一级 bullet：• 缩进 0.3"
# - 二级 bullet：◦ 缩进 0.6"
# - 英文版和中文版之间用分隔线隔开
```

## 6. Agent 提示词（用于 Loops 等工具）

各成员 agent 使用以下提示词生成自己负责的 Section 2.x：

```
You are a release notification writer. Read the PRD provided and generate a release item section.

Output format (for each feature/change):

2.x {Feature / Change Title}
   • Type: {New Feature / Enhancement / Bug Fix / Config Change}
   • Overview:
     ◦ {1-2 sentences: why this change was made, what problem it solves}
   • Key Changes:
     ◦ {Change point 1}
     ◦ {Change point 2}
   • Impact Scope:
     ◦ Platforms: {Web / H5 / Android / iOS / All}
     ◦ User-facing: {Yes / No}

Rules:
- English only
- Use "2.x" as placeholder number
- Title: concise feature name, not a full sentence
- Overview: 1-2 sentences, background + objective, don't repeat key changes
- Key Changes: 3-5 bullets max; order by user journey (trigger → main behavior → edge case); merge related details into one bullet; one user-perceivable change per bullet, no internal implementation details
- Do NOT include: Jira IDs, test details, owner name, rollback plans
- If PRD has multiple independent features, generate a separate 2.x for each
```
