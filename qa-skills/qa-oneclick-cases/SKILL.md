---
name: qa-oneclick-cases
description: Generate test cases in JSON with 3 auto-detected paths (PRD+TD/TP+TI/PRD-only). Use when user needs test cases or mentions 一键生成用例, 用例生成.
---

# 一键生成测试用例

## 适用场景

用户提供PRD/TD/TP/TI任意组合，需要生成结构化JSON测试用例集

## 规则依赖

开始执行前读取 `.cursor/skills/_shared/core-rules.md`

## 三条路径（自动识别）

| 路径 | 输入 | 执行方式 | 适用场景 |
|------|------|---------|---------|
| **A** | PRD+TD | 完整分析 → 生成用例 | 从零开始完整覆盖 |
| **B** | 已有TP/TI | 直接展开 → 生成用例 | 复用分析⭐推荐 |
| **C** | 仅PRD | 快速分析 → 技术点标记【缺少TD】 | 快速启动⭐常用 |

**路径识别**：
- 有TP-xxx/TI-xxx编号（≥3个）→ 路径B
- 有TP-xxx/TI-xxx编号（1-2个）→ 同时有TD则路径A，仅PRD则路径C；提示"已有TP/TI数量不足，将重新完整分析"
- 有PRD+TD章节 → 路径A  
- 仅PRD章节 → 路径C

> 详细识别规则、异常处理见 [reference.md §1](references/reference.md#1-三条路径详细流程)

## 执行流程

**5步完成**：
1. **路径识别** → 校验输入 → 输出"✓ 检测到路径X"
2. **执行分析** → 路径A调用`@qa-prd-analysis`+`@qa-td-analysis` | 路径B读取TP/TI | 路径C调用`@qa-prd-analysis`
3. **生成用例** → 按 [reference.md §6](references/reference.md#6-tptc-系统展开矩阵) 逐维度展开TC（正向/异常/边界/权限/并发），按 [reference.md §7](references/reference.md#7-用例内容质量规范) 规范title/步骤/期望结果，确保9字段齐全、期望多层可判定、冒烟准确
4. **自检验证** → 12项检查 → 评分 → **修复循环**（见 [reference.md §4.4](references/reference.md#44-修复循环规则)）：
   - 评分 ≥ 90 → 进入步骤5
   - 评分 < 90 → 自动修复可修复问题 → 重新自检（最多2轮）
   - 2轮后仍 < 90 → 进入步骤5，待澄清列出所有无法自动修复的问题
5. **输出结果** → 将完整JSON写入文件，当前窗口仅输出摘要+自检结果+待澄清（见 [reference.md §5](references/reference.md#5-输出规则)）

## 快速口诀

| 维度 | 口诀 |
|------|------|
| **路径选择** | ≥3个TP/TI→B \| PRD+TD→A \| 仅PRD→C |
| **用例必备** | 9字段+4类前置+期望多层可判定（响应+数据层，禁止"正常""成功"） |
| **展开策略** | 逐维度：正向/参数变体/异常/边界/等价类/权限/并发/兼容/可观测 |
| **标题规范** | 动作+条件→期望摘要（禁止"验证...功能"等笼统写法） |
| **冒烟公式** | P0 ∩ 主路径正向，5-15% |
| **自检门槛** | ≥90分可交付，阻塞级问题必须先修复 |
| **路径C提示** | 技术验证点标【缺少TD】，额外输出待补充清单 |

## 核心要求

用例必须符合 [core-rules.md](../_shared/core-rules.md) 的基础规范：
- **§4.1**: 9字段必填（禁止留空/TBD）
- **§4.2**: 前置条件4类（账号/配置/数据/环境）
- **§4.3**: 期望结果多层可判定（响应层+数据层+副作用层，禁止模糊词）→ 分层框架见 [reference.md §7.3](references/reference.md#73-期望结果分层框架)
- **§2**: 冒烟标记规则（P0 ∩ 主路径正向，5-15%，排除异常/边界/权限/并发）

用例内容质量必须符合 [reference.md §7](references/reference.md#7-用例内容质量规范)：
- **title**: 【动作/场景特征】+【关键条件】→【期望摘要】，禁止"验证...功能"/"测试...流程"等笼统写法
- **步骤**: 1步=1操作，包含具体值（"输入test@example.com"而非"输入账号"），不写占位符
- **展开策略**: 按 [reference.md §6展开矩阵](references/reference.md#6-tptc-系统展开矩阵) 逐维度覆盖，不凭直觉生成

## JSON最小结构

```json
{
  "modules": [{
    "name": "用户模块",
    "functions": [{
      "name": "登录功能",
      "test_points": [{
        "id": "TP-001",
        "name": "验证用户名密码登录",
        "priority": "P0",
        "source": "REQ-001",
        "cases": [{
          "id": "TC-001",
          "title": "使用正确邮箱密码登录→成功跳转/home、右上角显示用户名'test'",
          "优先级": "P0",
          "用例类型": "功能-正向",
          "执行端": "Web",
          "前置条件": [
            "1. 账号/权限：test@example.com / Pass123456",
            "2. 配置/开关：login_feature=on",
            "3. 数据准备：用户已注册且状态为active",
            "4. 环境依赖：认证服务正常"
          ],
          "测试步骤": [
            "1. 打开登录页面",
            "2. 输入用户名test@example.com",
            "3. 输入密码Pass123456",
            "4. 点击登录按钮"
          ],
          "期望结果": [
            "1. 接口返回200",
            "2. 响应包含token字段",
            "3. 页面跳转到/home",
            "4. 右上角显示用户名'test'"
          ],
          "冒烟标记": "是"
        }]
      }]
    }]
  }]
}
```

> 完整JSON示例、特殊标记（路径C缺少TD）见 [reference.md §2](references/reference.md#2-json格式规范)

## 自检机制（12项）

生成后自动执行：

**覆盖率维度（50分）**
1. ✓ 需求覆盖率（≥95%，15分）
2. ✓ 风险场景覆盖（100%适用项，8分）
3. ✓ 异常用例占比（20-35%，7分）
4. ✓ 边界值覆盖（关键字段全覆盖，8分）
5. ✓ 状态流转覆盖（合法+非法，7分）
6. ✓ 权限角色覆盖（核心操作×角色，5分）

**质量维度（30分）**
7. ✓ 9字段完整率（100%，15分）
8. ✓ 期望多层覆盖（响应+数据层，无模糊词，10分）
9. ✓ 前置条件4类完整（账号/配置/数据/环境，5分）

**追溯维度（20分）**
10. ✓ 无孤儿REQ/TD（7分）
11. ✓ 无孤儿TP/TI（7分）
12. ✓ 冒烟规则正确（P0∩主路径，5-15%，6分）

**交付门槛**：≥90分可交付 | 评分细则见 [reference.md §4.2](references/reference.md#42-自检评分细则90分可交付) | 修复循环规则见 [reference.md §4.4](references/reference.md#44-修复循环规则)

## 参考资源

- [reference.md](references/reference.md) - 路径决策树、完整JSON示例、质量门槛
- [core-rules.md](../_shared/core-rules.md) - 优先级判定、冒烟规则、字段规范
- 导出：使用 `@export-case` 导出为 FreeMind/Markdown/Excel
