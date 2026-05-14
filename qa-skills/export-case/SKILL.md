---
name: export-case
description: Export test cases to FreeMind (.mm), Markdown (.md), or Excel (.xlsx). Use when user needs to export or mentions 导出用例, 导出FreeMind.
---

# 导出用例

## 适用场景

用户有结构化的测试用例（4层：模块→功能→测试点→用例），需要导出为FreeMind/Markdown/Excel格式。

## 规则依赖

**本skill为格式转换工具**，不涉及测试分析逻辑，无需读取core-rules.md。

**职责**：将标准JSON格式用例转换为FreeMind/Markdown/Excel格式。

## 格式选择

| 格式 | 用途 | 特点 | 何时使用 |
|------|------|------|---------|
| **FreeMind** | 评审/演示 | 层级可视化，思维导图形式 | 评审会议、方案演示、脑图整理 |
| **Markdown** | 文档沉淀 | 易阅读编辑，版本管理友好 | Wiki文档、GitHub、Confluence |
| **Excel** | 平台导入 | 批量操作，表格化管理 | 测试平台导入、数据分析、批量编辑 |

**核心要求**：
- ✓ 层级结构正确：4层(modules→functions→test_points→cases)不丢失
- ✓ 信息完整：用例ID、优先级、冒烟标记必须保留
- ✓ 格式合规：UTF-8编码、特殊字符正确转义

> 详细格式模板、转义规则见 [reference.md §1-3](references/reference.md#1-FreeMind格式)

## 使用方法

### 方法1：AI直接生成（推荐，≤200用例）

将用例JSON提供给AI，指定导出格式：
```
"请将这些用例导出为FreeMind格式"
"导出为Excel表格，包含所有9字段"
```

### 方法2：Python脚本（大型用例集）

用例数量>200或需批量导出时：

```bash
pip install -r scripts/requirements.txt
python scripts/export_case.py --format freemind --input cases.json --output test.mm
```

**支持参数**：
- `--format`：freemind / markdown / excel
- `--input`：JSON用例文件路径
- `--output`：导出文件路径

> 脚本使用详见 [reference.md §5](references/reference.md#6-脚本使用)

## 参考资源

- [reference.md](references/reference.md) - 格式规范、转义规则、常见问题
- scripts/export_case.py - 转换脚本
