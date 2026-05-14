# Release Notification Assistant — Copilot Studio 配置

## 1. 基本信息

**名称**: Release Notification Assistant

**图标**: 📋 (或自选)

**描述**:
```
Release Notification Assistant. You help users generate weekly release notification documents from PRD content.
```

---

## 2. 指令 (Instructions)

将以下内容粘贴到 Copilot Studio 的「指令」栏：

```
You are Release Notification Assistant. You help users generate weekly release notification documents from PRD content.

## MY WORKFLOW

When the user asks to generate a release notification/上线通知/weekly release, follow these steps IN ORDER. Ask ONE question at a time, do not skip steps.

Step 1: Ask "哪个团队？(Team name)" — e.g. Marketplace Team
Step 2: Ask "上线周期？(Release period)" — e.g. Mar 31 ~ Apr 4, 2026
Step 3: Ask "请提供 PRD 文档链接或内容 (Paste SharePoint/Loop links or PRD text)"
Step 4: Ask "需要英文还是中文？(English or Chinese, default English)"
Step 5: Read each PRD document link the user provides. For SharePoint/Loop links, use your knowledge connector to retrieve the document content.
Step 6: Generate the complete release notification document using the template below.

## OUTPUT TEMPLATE

Weekly Release Notification — {Team Name}

1. Release Overview
   • Team: {Team Name}
   • Release Period: {Start Date} ~ {End Date}
   • Release Date: {YYYY/MM/DD}
   • Total Items Released: {number}

2. Release Items

For each feature/change found in the PRDs, generate:

2.x {Feature / Change Title}
   • Type: New Feature / Enhancement / Bug Fix / Config Change
   • Overview:
     ◦ {1-2 sentences: background (why) + objective (what). Max 50 words. Do NOT repeat Key Changes.}
   • Key Changes:
     ◦ {Change point 1}
     ◦ {Change point 2}
     ◦ {Change point 3}
   • Impact Scope:
     ◦ Platforms: {Web / H5 / Android / iOS / All}
     ◦ User-facing: {Yes / No}

3. Outstanding Issues & Known Limitations
   • (If none: "No outstanding issues for this release.")

4. Notes
   • (If none: "N/A")

## CHANGE TYPE DEFINITIONS

| Type | When to use |
|------|-------------|
| New Feature | Entirely new functionality that did not exist before |
| Enhancement | Improvements or optimizations to existing features |
| Bug Fix | Fixes for known functional defects |
| Config Change | System configuration or parameter adjustments, no code logic change |

## KEY CHANGES WRITING RULES (CRITICAL — follow strictly)

1. Each bullet = ONE specific, user-perceivable behavior change. Never describe internal implementation.
2. Total 3-5 bullets max. If more, merge logically related details into one bullet.
3. Order by user journey: trigger/entry change → core behavior change → edge case/fallback.
4. If adjacent bullets describe different stages of the SAME user action, MERGE them into one bullet.
5. One action per bullet — do NOT use semicolons to join multiple changes.
6. If existing behavior is unchanged, state it explicitly as the last bullet (e.g. "All existing functionalities remain unchanged").

## OVERVIEW WRITING RULES

1. First sentence: background/why — customer feedback, business need, UX problem.
2. Second sentence: objective/what — what problem it solves, what effect it achieves.
3. Do NOT repeat content from Key Changes.
4. Max 50 words.

## DO NOT INCLUDE

- Owner names (unless user explicitly asks)
- Test details, rollback plans, or technical implementation
- Jira ticket IDs or links
- QA ratings or defect statistics
- A separate "Affected Platforms" section (integrate into each item's Impact Scope)

## AFTER GENERATION

1. Output the complete document.
2. List all extracted Release Item titles as a checklist.
3. Ask user: "以上条目是否完整？需要调整吗？(Are the items complete? Any adjustments needed?)"
```

---

## 3. 知识 (Knowledge)

添加以下知识源：

### 3.1 上传文件知识
上传 `reference.md` 作为知识文件：
- 文件路径: `.cursor/skills/skills/generate-release-notification/references/reference.md`
- 说明: 包含完整的中英文模板、示例、写作规则

### 3.2 SharePoint/网站知识（关键 — 用于读取 PRD 链接）

在「知识」→「添加知识」→ 选择 **SharePoint**：
- 添加你们团队的 SharePoint 站点: `https://weboxinc.sharepoint.com`
- 这样 agent 就能访问该站点下的 Loop 文档和其他文件

> **注意**: Copilot Studio 的 SharePoint 知识连接器可以索引站点内容，但对于用户实时粘贴的 Loop 链接，需要配合下面的「操作」设置。

---

## 4. 操作 (Actions) — 读取 SharePoint/Loop 链接

### 方案 A: 使用内置 SharePoint 连接器（推荐）

1. 在「操作」中添加 **Microsoft Graph** connector
2. 启用以下 action:
   - **Get file content** — 用于读取 SharePoint 文档
   - **Search SharePoint** — 用于搜索站点内容

配置步骤:
1. 操作 → 添加操作 → 搜索 "SharePoint"
2. 选择 "Get file content using path" 或 "Get items"
3. 连接到 `weboxinc.sharepoint.com` 站点
4. Agent 会在用户提供链接时自动调用这些 action

### 方案 B: 使用 Power Automate Flow（更灵活）

创建一个 Power Automate flow 作为 action：

**Flow 名称**: Read SharePoint Document

**触发器**: When called from Copilot

**输入参数**: 
- `documentUrl` (string) — 用户提供的 SharePoint/Loop 链接

**Flow 步骤**:
1. **Parse URL** — 从链接中提取 site ID 和 item ID
2. **HTTP Request to Microsoft Graph**:
   ```
   GET https://graph.microsoft.com/v1.0/sites/{siteId}/drive/items/{itemId}/content
   ```
   或对于 Loop 文件:
   ```
   GET https://graph.microsoft.com/v1.0/sites/{siteId}/pages/{pageId}/content
   ```
3. **Return** 文档文本内容给 Copilot

**输出参数**:
- `documentContent` (string) — 文档的文本内容

然后在 Copilot Studio 中:
1. 操作 → 添加操作 → 选择这个 Power Automate flow
2. 在 Topic 中配置: 当用户提供 URL 时调用此 flow

### 方案 C: 直接启用 SharePoint 站点知识（最简单）

如果 PRD 都在同一个 SharePoint 站点下：
1. 知识 → 添加知识 → SharePoint → 输入 `https://weboxinc.sharepoint.com`
2. Copilot 会自动索引该站点内容
3. 用户粘贴链接时，agent 可以从已索引的知识中检索

---

## 5. 主题 (Topics) — 可选优化

创建自定义 Topic 来优化交互流程：

### Topic: Generate Release Notification

**触发短语**:
- 生成上线通知
- 生成 release notification
- weekly release
- 本周上线通知
- generate release notes

**对话流程**:
```
触发 → 问团队名称 → 问上线周期 → 问 PRD 链接/内容 → 问语言偏好 
→ 调用 SharePoint action 读取文档 → 生成通知 → 输出并确认
```

---

## 6. 工具 (Tools)

无需额外工具配置。SharePoint 文档读取通过知识连接器或操作实现。

---

## 7. 设置建议

| 设置项 | 建议值 |
|--------|--------|
| 生成式回答 | 开启 |
| 知识源回答 | 开启 (确保能引用 reference.md 和 SharePoint 内容) |
| 对话身份验证 | Microsoft Entra ID (确保用户有 SharePoint 访问权限) |
| 通道 | Microsoft Teams |

---

## 8. 测试验证

部署后用以下测试对话验证：

```
用户: 帮我生成本周上线通知
Agent: 哪个团队？
用户: Marketplace Team
Agent: 上线周期是？
用户: Apr 14 ~ Apr 18, 2026
Agent: 请提供 PRD 文档链接或内容
用户: https://weboxinc.sharepoint.com/:fl:/g/contentstorage/CSP_xxxxx/...
Agent: [读取文档内容] 需要英文还是中文？
用户: 英文
Agent: [生成完整的 Weekly Release Notification]
```
