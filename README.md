# brain0129

个人测试工程能力沉淀，涵盖从需求分析到测试报告的完整 QA 工作流。

---

## 测试工作流总览

```
需求/设计输入 → 测试分析 → 用例生成 → 用例评审 → 测试执行 → 缺陷分析 → 测试报告 → 发版通知
```

---

## 1. 测试分析（需求 & 设计 → 测试点）

将 PRD 和技术设计文档转化为可追溯的测试点。

| Skill | 说明 | 路径 |
|---|---|---|
| qa-prd-analysis | PRD → 测试点（TP-xxx），含优先级与风险标注 | `qa-skills/qa-prd-analysis/` |
| qa-td-analysis | 技术设计 → 测试入口（TI-xxx），关注接口与状态变更 | `qa-skills/qa-td-analysis/` |
| defect-prediction-analysis | 基于历史数据预测高风险模块 | `qa-skills/defect-prediction-analysis/` |

## 2. 用例生成（测试点 → 测试用例）

从测试点自动生成结构化、可执行的测试用例。

| Skill | 说明 | 路径 |
|---|---|---|
| qa-oneclick-cases | TP/TI → TC-xxx 一键生成，含前置条件/步骤/预期结果 | `qa-skills/qa-oneclick-cases/` |
| generate-test-cases | 通用测试用例生成（不依赖 QA 工作流） | `engineering-skills/generate-test-cases/` |
| generate-protocol-test-cases | 网络协议测试用例（OSPF/BGP/STP/VXLAN），FS.COM 13字段格式 | `engineering-skills/generate-protocol-test-cases/` |

## 3. 用例评审 & 导出

对已有用例进行质量检查，并支持多格式导出。

| Skill | 说明 | 路径 |
|---|---|---|
| qa-case-review | 用例评审：检查可追溯性、可执行性、可判定性 | `qa-skills/qa-case-review/` |
| export-case | 用例导出（CSV/Excel/飞书脑图等格式） | `qa-skills/export-case/` |

## 4. 测试执行辅助

测试指南生成，指导手工/自动化测试执行。

| Skill | 说明 | 路径 |
|---|---|---|
| generate-test-guide | 生成测试指南文档（范围/策略/环境/排期） | `qa-skills/generate-test-guide/` |

## 5. 缺陷分析 & 质量度量

从 Jira Bug 数据进行多维度质量分析。

| Skill | 说明 | 路径 |
|---|---|---|
| jira-bug-quality-report | Jira Bug 多维度质量报告（模块/严重度/趋势/根因） | `qa-skills/jira-bug-quality-report/` |

## 6. 测试报告

自动生成结构化测试报告。

| Skill | 说明 | 路径 |
|---|---|---|
| generate-test-report (QA) | 测试报告生成（含缺陷统计图表） | `qa-skills/generate-test-report/` |
| generate-test-report (Eng) | 测试报告（工程变体，侧重技术指标） | `engineering-skills/generate-test-report/` |

## 7. 发版通知

生成面向团队的发版通知。

| Skill | 说明 | 路径 |
|---|---|---|
| generate-release-notification | 发版通知（纯文本） | `engineering-skills/generate-release-notification/` |
| generate-release-notification-html | 发版通知（HTML，含截图） | `engineering-skills/generate-release-notification-html/` |

## 8. Skill 自进化

持续改进 Skill 质量的反馈闭环。

| Skill | 说明 | 路径 |
|---|---|---|
| qa-skill-evolve | Skill 自进化引擎，基于使用反馈迭代优化 | `qa-skills/qa-skill-evolve/` |

---

## 协议测试用例库

独立的网络协议测试项目，AI 驱动生成。

| 协议 | 用例数 | 路径 |
|---|---|---|
| OSPFv2 | 49 cases（6 模块） | `picos-protocol-testing/test-cases/ospf/` |
| BGP-EVPN | 多模块 | `picos-protocol-testing/test-cases/bgp-evpn/` |
| Stacking | 多模块 | `picos-protocol-testing/test-cases/stacking/` |

详见 [picos-protocol-testing/README.md](picos-protocol-testing/README.md)

---

## 目录结构

```
brain0129/
├── qa-skills/                          # QA 工作流 Skills
│   ├── qa-prd-analysis/                # 需求分析
│   ├── qa-td-analysis/                 # 技术设计分析
│   ├── defect-prediction-analysis/     # 缺陷预测
│   ├── qa-oneclick-cases/              # 一键生成用例
│   ├── qa-case-review/                 # 用例评审
│   ├── export-case/                    # 用例导出
│   ├── generate-test-guide/            # 测试指南
│   ├── generate-test-report/           # 测试报告
│   ├── jira-bug-quality-report/        # Bug 质量报告
│   └── qa-skill-evolve/               # Skill 自进化
├── engineering-skills/                 # 工程 Skills
│   ├── generate-test-cases/            # 通用用例生成
│   ├── generate-protocol-test-cases/   # 协议用例生成
│   ├── generate-test-report/           # 测试报告（工程版）
│   ├── generate-release-notification/  # 发版通知
│   └── generate-release-notification-html/  # HTML 发版通知
└── picos-protocol-testing/             # 协议测试用例库
    ├── docs/                           # RFC & 厂商文档
    ├── test-cases/                     # OSPF / BGP-EVPN / Stacking
    ├── scripts/                        # 工具脚本
    └── reports/                        # 质量门禁报告
```
