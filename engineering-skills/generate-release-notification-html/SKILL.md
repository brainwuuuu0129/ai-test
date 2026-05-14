---
name: generate-release-notification-html
description: Generate HTML release notifications with embedded screenshots for sales and cross-functional teams. Use when user mentions HTML上线通知, HTML release notification, 可视化发布通知, release notification with screenshots.
---

# 生成 HTML 格式上线通知

用户提供改动信息和截图，生成自包含的 HTML 上线通知文档，面向销售和非技术部门，内嵌截图，可直接在浏览器查看或通过飞书/邮件发送。

## 适用场景

- 需要带截图的可视化上线通知
- 发送给销售、运营等非技术同事
- 需要单文件自包含（base64 内嵌图片），无外部依赖

## 不适用场景

- 纯文本 / Markdown / Word 格式通知 → 使用 `generate-release-notification`
- 内部技术文档 / Test Report → 使用 `generate-test-report`

## 执行流程

### Step 1: 收集输入

通过对话确认以下信息：

| 字段 | 必填 | 说明 |
|------|------|------|
| 团队名称 | 是 | 如 Marketplace Team |
| 上线日期 | 是 | 如 2026/05/14 |
| 背景说明 | 否 | 本次上线的背景和目标（1-2 句） |
| 改动条目 | 是 | 每个改动的标题、类型、描述、Key Changes |
| 截图文件 | 否 | 本地图片路径，用于内嵌到对应条目 |
| Outstanding Issues | 否 | 遗留问题及预计修复时间 |
| Notes | 否 | 补充说明，如切换方式、鼓励体验等 |
| 语言 | 否 | 默认英文 |

### Step 2: 收集截图

1. 询问用户是否有截图需要嵌入
2. 如有，让用户将截图保存到项目目录
3. 使用 `Glob` 扫描目录找到新增图片文件
4. 用 `Read` 工具逐张确认图片内容，与改动条目建立对应关系
5. 与用户确认图片 ↔ 条目的映射关系

### Step 3: 生成 HTML

1. 基于模板结构生成完整 HTML，样式内嵌（见 [reference.md](references/reference.md)）
2. 文档结构：
   - **Header**: 蓝色渐变横幅，团队名 + 日期
   - **Section 1 Release Overview**: 2×2 网格卡片
   - **Background**: 蓝色信息卡片（如有背景说明）
   - **Section 2 Release Items**: 每个条目一张卡片，含类型标签 + 截图
   - **Section 3 Outstanding Issues**: 橙色警告卡片
   - **Section 4 Notes**: 绿色提示卡片
   - **Footer**: 团队签名
3. 类型标签颜色：
   - New Feature → 绿色 `.badge-new-feature`
   - Enhancement → 蓝色 `.badge-enhancement`
   - Bug Fix → 橙色 `.badge-bug-fix`
   - Config Change → 灰色 `.badge-config-change`

### Step 4: 嵌入截图

使用 Python 脚本将截图转为 base64 嵌入 HTML：

```python
import base64

with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

# 插入到对应条目的 screenshot-gallery 中
# <img src="data:image/png;base64,{b64}" alt="description">
```

**注意事项**：
- 图片嵌入后 HTML 文件会很大（每张图 300KB-800KB base64）
- 修改 HTML 时不能用 Read/Edit 工具（文件超 token 限制），必须用 Python 脚本操作
- 截图默认 `max-height: 620px`，可根据用户反馈调整

### Step 5: 输出与交付

1. 在浏览器中打开预览：`open {file_path}`
2. 如用户指定，复制到桌面或其他目录
3. 询问用户：
   - 图片大小是否合适
   - 内容是否有遗漏
   - 是否需要补发群聊文案

### Step 6: 生成群聊文案（可选）

如用户需要配套的群聊发送文案，生成简短通知，包含：
- 核心改动一句话总结
- 重要注意事项（如切换方式、兼容性说明）
- 已知问题修复时间
- 引导查看附件

## 编写约束

- 继承 `generate-release-notification` 的全部写作规则
- 全文英文（除非用户要求中文）
- 不写负责人姓名、测试细节、Jira ID
- Key Changes 3-5 条，按用户操作顺序排列
- 面向非技术受众：突出用户可感知的变化，避免技术术语
- HTML 必须自包含：所有 CSS 内嵌，所有图片 base64 编码，无外部依赖

## 开发文件审查（可选）

如用户提供开发的文件改动清单，对比已有 Release Items 检查是否有遗漏：

1. 逐模块扫描文件改动
2. 识别用户可感知的功能变更
3. 对比已有条目，列出可能遗漏的改动
4. 建议：新增为独立条目 / 合并到现有条目的 Key Changes / 放入 Notes

## 参考资源

- [reference.md](references/reference.md) — HTML 模板结构、CSS 样式规范、完整示例
- [generate-release-notification/reference.md](../generate-release-notification/references/reference.md) — 写作规则、变更分类定义、Key Changes 写法
