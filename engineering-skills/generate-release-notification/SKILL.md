---
name: generate-release-notification
description: Generate weekly release notifications from PRD documents. Use when user needs release notification, release summary, release notes, or mentions 上线通知, 发布通知, release notification, weekly release.
---

# 生成周上线通知

用户提供小组名称和本周的 PRD（一份或多份），自动汇总生成该小组本周完整的上线通知文档。

## 执行流程

### Step 1: 收集输入

通过 `AskQuestion` 或对话确认以下信息：

| 字段 | 必填 | 说明 |
|------|------|------|
| 小组名称 | 是 | 如 Marketplace Team |
| 上线周期 | 是 | 本周起止日期，如 Mar 31 ~ Apr 4, 2026 |
| 上线日期 | 否 | 默认取周期结束日 |
| PRD 内容 | 是 | 支持：上传文件 / 粘贴文字 / 截图 / URL（可提供多份） |
| 语言 | 否 | 默认英文，用户可指定中文 |
| 输出格式 | 否 | 默认 Markdown，可选 Word (.docx) 或纯文本 (.txt) |

### Step 2: 逐份 PRD 提取变更项

对每份 PRD 执行：

1. 阅读全部内容，如包含流程图/画布，先还原为节点 + 流转条件的文字结构
2. 识别所有独立的功能变更，每个变更拆分为一个 Release Item
3. 为每个 Item 判定类型：New Feature / Enhancement / Bug Fix / Config Change
4. 按 Section 2.x 格式填充 Type、Overview、Key Changes、Impact Scope

### Step 3: 合并生成完整文档

1. 将所有 PRD 提取的 Release Items 统一编号（2.1, 2.2, 2.3...）
2. 填充 Section 1（Release Overview）：团队、周期、日期、条目总数
3. 填充 Section 3（Outstanding Issues）：如用户未提供，写 "No outstanding issues"
4. 填充 Section 4（Notes）：如用户未提供，写 "N/A"

> 文档结构、字段格式、写作规则见 [reference.md](references/reference.md)

### Step 4: 输出

| 格式 | 操作 |
|------|------|
| Markdown | 直接在对话中输出完整文档 |
| Word | 使用 python-docx 生成 .docx 文件，样式规范见 [reference.md §5](references/reference.md#5-word-文档生成) |
| 纯文本 | 生成 .txt 文件 |

### Step 5: 交付确认

1. 输出完整文档（或告知文件路径）
2. 列出本次提取的所有 Release Items 标题清单，请用户确认是否有遗漏或需要调整

## 编写约束

- 全文英文（除非用户要求中文）
- 不写负责人姓名（除非用户要求）
- 不写测试细节、回滚方案、Jira ID、QA 评级
- 每个 bullet point 一句话，描述用户可感知的变化，不写内部实现
- Key Changes 控制在 3-5 条，按用户操作顺序排列，相关细节合并不拆散
- 多份 PRD 的 Items 合并到同一份文档，统一编号

## 参考资源

- [reference.md](references/reference.md) — 完整模板（中英文）、示例、写作规则、Word 样式规范
