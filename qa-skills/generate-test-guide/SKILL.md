---
name: generate-test-guide
description: 根据 PRD、技术设计文档和测试用例生成标准化测试指南文档。Use when user needs to generate test guide, test wiki, or mentions 生成测试指南, 测试文档, test guide.
---

# 生成测试指南（Test Guide Generation）

## 适用场景

- 用户需要为某模块生成测试指南、测试文档或测试 Wiki
- 用户提供 PRD、技术设计或测试用例链接（如飞书/Lark Wiki）
- 用户需要整合测试知识用于回归测试或工作交接

## 规则依赖

**本skill为文档生成工具**，基于 PRD + 技术设计 + 测试用例，产出标准化 7 章节测试指南。

**输入要求**：
- PRD（飞书 Wiki URL 或文档）
- 技术设计文档（飞书 Wiki URL 或文档）
- 测试用例（思维导图 .mm / 飞书 Wiki / 结构化文档）

**输出**：标准化测试指南（7 章节：业务背景、业务流程、实现逻辑、API、数据结构、测试用例、典型问题）

## 执行流程（AI必读）

**开始执行前，必须先读取详细指南**：[reference.md](references/reference.md)

详细指南包含完整的：
- 输出结构（7 个章节的详细定义）
- 执行步骤（Step 1 ~ Step 9）
- 格式规范（语言、章节编号、表格、流程图）
- 质量检查清单
- 示例提示词和响应
- 文件命名规范

### 快速流程概览

1. **收集文档** - 通过 MCP 工具获取 PRD / TD / 测试用例内容
2. **逐章节生成** - 按 7 个章节顺序生成，每章节提交用户审核
3. **最终检查** - 按质量检查清单验证完整性

### MCP 工具依赖

| 工具 | 用途 |
|------|------|
| `wiki_v2_space_getNode` | 获取飞书 Wiki 节点信息和文档 token |
| `docx_v1_document_rawContent` | 从飞书文档提取文本内容 |
| `Read` | 读取本地文件（如 .mm 思维导图） |
| `Write` | 保存生成的 Markdown 文档 |
| `GenerateImage` | 按需生成 PNG 流程图 |

---

## 参考资源

- [reference.md](references/reference.md) - 完整执行指南、输出模板、格式规范、质量检查清单
