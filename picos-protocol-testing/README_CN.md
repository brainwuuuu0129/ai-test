# PicOS 网络协议测试用例生成器

基于 AI 的 Pica8 PicOS 交换机网络协议功能测试用例自动生成项目。

## 项目简介

本项目使用 AI（Cursor Agent + 自定义 Skill）自动生成 PicOS 网络协议的全面、可执行功能测试用例。测试用例通过交叉参考 **RFC 标准** 与 **PicOS 厂商文档** 生成，既保证协议合规性，又确保 CLI 命令的准确性。

测试用例采用 **FS.COM 表格格式** 输出，包含拓扑图、前置条件、完整 CLI 配置、测试步骤和预期结果，可直接用于手工执行或自动化脚本开发。

## 协议覆盖状态

| 协议 | RFC/标准 | PicOS 文档 | CLI 参考 | 测试用例数 | 状态 |
|------|---------|-----------|---------|-----------|------|
| **OSPFv2** | RFC 2328 | ✅ | ✅ | 49 条（6 模块） | **已完成** |
| BGP-4 | RFC 4271 | — | — | — | 规划中 |
| STP/RSTP | IEEE 802.1D | — | — | — | 规划中 |
| VXLAN | RFC 7348 | — | — | — | 规划中 |
| OSPFv3 | RFC 5340 | — | — | — | 规划中 |

## 项目结构

```
picos-protocol-testing/
├── .cursor/
│   ├── skills/generate-protocol-test-cases/
│   │   ├── SKILL.md                    # 核心 AI Skill（4 阶段生成流程）
│   │   └── references/
│   │       ├── picos-cli-reference/    # 各协议 CLI 速查手册
│   │       │   └── ospf.md             # OSPF CLI 命令参考
│   │       └── test-case-examples.md   # FS.COM 格式示例
│   └── rules/
│       └── protocol-test-case-format.mdc  # 输出格式强制规范
│
├── docs/
│   ├── rfcs/                           # RFC 标准文档
│   │   └── rfc2328.txt                 # OSPFv2
│   └── picos/                          # PicOS 厂商配置指南
│       └── ospf-config-guide.md
│
├── test-cases/                         # 生成的测试用例（按协议分目录）
│   ├── ospf/
│   │   ├── ospf-functional-test-cases-mod1-3.md  # 24 条用例（模块 1-3）
│   │   └── ospf-functional-test-cases-mod4-6.md  # 25 条用例（模块 4-6）
│   ├── bgp/
│   ├── stp/
│   └── vxlan/
│
├── scripts/                            # 工具脚本
│   ├── fetch_picos_docs.py             # 自动抓取 PicOS Wiki 文档
│   ├── md2pdf.py                       # Markdown 转 PDF
│   ├── merge_test_cases.py             # 合并多模块用例为单文件
│   └── requirements.txt
│
└── reports/                            # 质量门检查报告
    └── ospf/
        └── ospf-test-quality-gate-report.md
```

## 快速开始

### 环境要求

- [Cursor IDE](https://cursor.sh)（需要 Agent 模式）
- Python 3.9+
- 网络访问（用于抓取 PicOS Wiki 文档）

### 为新协议生成测试用例

**第一步：准备文档**

```bash
# 自动抓取 PicOS Wiki 文档（保存到 docs/picos/）
python scripts/fetch_picos_docs.py --protocol bgp --version 4.6

# 或手动放置：
# RFC 文档 → docs/rfcs/
# PicOS 配置指南 → docs/picos/
```

**第二步：在 Cursor Agent 模式下生成用例**

```
@generate-protocol-test-cases

Protocol: BGP
RFC: docs/rfcs/rfc4271.txt
Vendor Guide: docs/picos/bgp-config-guide.md
Platform: PicOS 4.6
Test Type: Functional
Output Language: English
```

**第三步：导出 PDF**

```bash
python scripts/md2pdf.py test-cases/bgp/bgp-functional-test-cases.md
```

## 测试用例生成流程

AI Skill 按照 4 个阶段自动执行：

```
第 1 阶段：协议理解与功能模块映射
    ↓ 读取 RFC + PicOS 文档 → 构建功能-模块对照表
第 2 阶段：测试点提取
    ↓ FSM 状态机 / 报文字段 / 消息时序 / 协议特性 建模
第 3 阶段：测试用例生成
    ↓ FS.COM 表格格式 + 真实 PicOS CLI 命令
第 4 阶段：覆盖度验证与补充
    ↓ 覆盖矩阵检查 + 自动补充缺失用例
```

## 测试用例输出格式（FS.COM 表格）

每条测试用例采用竖向表格，包含 13 个字段：

| 字段 | 说明 |
|------|------|
| Test Name | 模块编号 + 序号 + 标题 |
| Purpose Of The Test | 验证目标（含 RFC 引用） |
| Test Topo & Precondition | 拓扑图 + 前置条件 + 完整 CLI 配置 |
| Test Procedure | 分步操作（仅使用动作动词） |
| Expected Results | 可观察的预期结果（show 命令输出 / 状态变化） |
| Automated or Not | 自动化状态 |
| Related Scripts | 自动化脚本路径 |
| Level | 优先级 P0 / P1 / P2 |
| Hardware Model | 目标交换机型号 |
| Version | PicOS 软件版本 |
| Actual Results | 执行时填写 |
| Test Results | Pass / Fail（执行时填写） |
| Remark | RFC 引用及附加说明 |

## OSPF 覆盖情况（49 条用例）

| 模块 | 功能特性 | P0 | P1 | 合计 |
|------|---------|----|----|------|
| MOD1 | 邻居发现与邻接关系 | 10 | 0 | 10 |
| MOD2 | 区域类型（Stub/NSSA/Normal） | 0 | 8 | 8 |
| MOD3 | 路由重分发与路由策略 | 0 | 6 | 6 |
| MOD4 | SPF 计算与路由学习 | 10 | 0 | 10 |
| MOD5 | 平滑重启（RFC 3623） | 0 | 7 | 7 |
| MOD6 | 接口参数与认证 | 0 | 8 | 8 |
| **合计** | | **20** | **29** | **49** |

## 工具脚本说明

### fetch_picos_docs.py — 文档抓取

从 Pica8 Wiki 自动获取配置指南并保存到本地。

```bash
python scripts/fetch_picos_docs.py --protocol ospf --version 4.6
python scripts/fetch_picos_docs.py --all --version 4.6   # 抓取全部协议
```

### md2pdf.py — PDF 导出

将 Markdown 测试用例文档转换为带样式的 PDF。

```bash
# 需先安装依赖
pip install markdown weasyprint
brew install pango glib   # macOS

python scripts/md2pdf.py test-cases/ospf/ospf-functional-test-cases-mod1-3.md
```

### merge_test_cases.py — 用例合并

将多个模块文件合并为单一完整文档。

```bash
python scripts/merge_test_cases.py --protocol ospf
# 输出：test-cases/ospf/ospf-functional-test-cases-complete.md
```

## 设计方法论

本项目的测试设计方法参考了 **NeTestLLM** 多智能体网络协议测试框架：

1. **分层协议理解** — 将 RFC 拆解为功能模块，逐层分析
2. **多模型测试点提取** — 状态机（FSM）、报文字段、消息时序、协议特性 四类建模方式
3. **厂商 CLI 绑定** — 每条命令均来源于真实 PicOS 文档，禁止猜测或虚构
4. **质量门验证** — 三级检查机制（可执行性、覆盖度、可维护性）

## 许可

仅限内部使用 — Pica8 QA Team。
