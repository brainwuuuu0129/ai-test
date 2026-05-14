# 光模块自动化回归测试 — 技术设计文档

**版本**：v0.1（待补齐信息后转 v1.0）  
**目标**：每次固件版本发布后，自动验证光模块识别/链路/DDM/告警四项核心功能，生成 HTML 报告。

---

## 一、整体架构

```
测试触发（手动 or CI/CD）
        ↓
  pytest 测试框架
        ↓
  netmiko SSH 连接层
        ↓
  目标交换机（一台或多台）
        ↓
  执行 show 命令 → 解析输出
        ↓
  对比 baseline 预期值
        ↓
  生成 HTML 报告 + 控制台输出
```

**技术栈选型**

| 组件 | 选型 | 理由 |
|---|---|---|
| 测试框架 | pytest | Python 生态最主流，插件丰富，CI 友好 |
| SSH 连接 | netmiko | 专为网络设备设计，支持 100+ 平台，自动处理分页 |
| 输出解析 | 正则表达式 / TextFSM | 轻量，无需安装额外平台依赖 |
| 报告生成 | pytest-html | 一行命令生成 HTML 报告 |
| 配置管理 | YAML | 人类可读，方便维护设备列表和预期值 |

---

## 二、目录结构

```
optical-module-regression/
│
├── config.yaml            # 设备连接信息 + 测试端口列表          ← 待填写
├── baseline.yaml          # 每个端口的预期值                    ← 待填写
│
├── conftest.py            # pytest fixtures（SSH 连接管理）
├── requirements.txt       # Python 依赖
├── run.sh                 # 一键运行脚本
│
├── tests/
│   ├── test_identity.py   # 测试项1：模块识别
│   ├── test_link.py       # 测试项2：链路状态
│   ├── test_ddm.py        # 测试项3：DDM 数据范围
│   └── test_alarms.py     # 测试项4：告警状态
│
├── parsers/
│   └── parser.py          # show 命令输出解析器                  ← 待适配平台
│
└── reports/               # 自动生成，无需手动创建
```

---

## 三、待填写信息清单

在开始写代码前，需要补齐以下信息：

### 3.1 设备信息

```yaml
# config.yaml 模板（填写后直接可用）
devices:
  - name: "sw-lab-01"           # ← 改为实际设备名
    host: "192.168.1.1"         # ← 改为实际 IP
    username: "admin"           # ← 改为实际用户名
    password: "xxxx"            # ← 改为实际密码
    platform: "linux"           # ← 见下方平台对照表
    ports:                      # ← 填写需要测试的端口名
      - "ethernet1/1"
      - "ethernet1/2"
```

**平台对照表（netmiko device_type 字段）**

| 交换机系统 | device_type 值 |
|---|---|
| PicOS (Pica8) | `linux` 或 `cisco_ios`（视 CLI 风格而定）|
| SONiC | `linux` |
| Cisco IOS | `cisco_ios` |
| Cisco NX-OS | `cisco_nxos` |
| Arista EOS | `arista_eos` |
| Juniper JunOS | `juniper_junos` |
| H3C Comware | `hp_comware` |
| Huawei VRP | `huawei` |

> **待确认**：你的平台用哪个 device_type？运行 `netmiko --list-platforms` 可查完整列表。

---

### 3.2 Show 命令

需要收集以下四类 show 命令的**真实输出样本**，用于编写解析器：

| 测试项 | 需要的命令 | 状态 |
|---|---|---|
| 模块识别 | 查看光模块厂商/型号/序列号的命令 | ⬜ 待确认 |
| 链路状态 | 查看端口 UP/DOWN 状态的命令 | ⬜ 待确认 |
| DDM 数据 | 查看温度/电压/TX功率/RX功率/偏置电流的命令 | ⬜ 待确认 |
| 告警状态 | 查看光模块相关告警的命令 | ⬜ 待确认 |

**收集方法**：在交换机上执行命令，把完整输出贴到 `parsers/samples/` 目录下，一个命令一个文件。解析器将基于这些样本编写。

---

### 3.3 Baseline 预期值

baseline 是回归测试的判断依据。每个端口需要定义：

```yaml
# baseline.yaml 模板
ports:
  ethernet1/1:
    identity:
      vendor_name: "FINISAR CORP"     # ← 填写预期厂商名
      part_number: "FTLX8571D3BCL"    # ← 填写预期料号
      # serial_number 通常不做固定检查（每根模块不同）

    link:
      expected_status: "up"           # ← up 或 down

    ddm:
      temperature:
        min: 0                        # ← 单位 ℃，来自规格书
        max: 70
      voltage:
        min: 3.0                      # ← 单位 V
        max: 3.6
      tx_power:
        min: -8.2                     # ← 单位 dBm，来自规格书 TX range
        max: 0.5
      rx_power:
        min: -14.4                    # ← 单位 dBm，来自规格书 RX range
        max: 0.5
      bias_current:
        min: 2                        # ← 单位 mA
        max: 100

    alarms:
      expected_count: 0              # ← 正常状态应有 0 个告警
```

---

## 四、四项测试逻辑说明

### 4.1 模块识别（test_identity）

**逻辑**：
1. SSH 连接交换机
2. 执行"查看模块信息"命令
3. 解析 Vendor Name、Part Number
4. 与 baseline.yaml 中预期值对比
5. 完全匹配 → PASS；不匹配 → FAIL（附实际值 vs 预期值）

**PASS 标准**：Vendor Name 和 Part Number 与 baseline 完全一致

---

### 4.2 链路状态（test_link）

**逻辑**：
1. 执行"查看端口状态"命令
2. 解析端口 UP/DOWN 状态
3. 与 baseline 中 expected_status 对比

**PASS 标准**：端口状态与预期一致

---

### 4.3 DDM 数据（test_ddm）

**逻辑**：
1. 执行"查看 DDM"命令
2. 解析 5 项指标数值（温度/电压/TX功率/RX功率/偏置电流）
3. 每项数值与 baseline 中 min/max 范围对比

**PASS 标准**：所有 5 项指标均在 baseline 定义的 [min, max] 范围内

**注意**：
- 若模块不支持 DDM（AOC/DAC），该测试项自动标记 SKIP
- DDM 范围来自模块规格书，首次运行前需填写 baseline

---

### 4.4 告警状态（test_alarms）

**逻辑**：
1. 执行"查看告警"命令
2. 解析与光模块相关的告警条目数
3. 与 baseline 中 expected_count 对比

**PASS 标准**：告警数量 ≤ expected_count（通常为 0）

---

## 五、报告格式

运行后自动生成 `reports/report_<日期>.html`，包含：

- 测试时间 + 设备信息 + 固件版本（手动填入或从设备读取）
- 每个端口 × 每项测试的 PASS / FAIL / SKIP 状态
- FAIL 项附详情：预期值 vs 实际值
- 汇总：总数 / 通过数 / 失败数 / 跳过数

示例：

```
固件版本：v4.6.1（回归）  测试时间：2026-05-14 10:30
设备：sw-lab-01 (192.168.1.1)

端口          模块识别   链路状态   DDM数据   告警状态
ethernet1/1   ✅ PASS    ✅ PASS    ✅ PASS   ✅ PASS
ethernet1/2   ✅ PASS    ✅ PASS    ❌ FAIL   ✅ PASS
                                   RX功率: -15.2dBm，超出范围 [-14.4, 0.5]

总计：7/8 通过，1 失败
```

---

## 六、实施步骤

补齐信息后，按以下顺序实施：

```
Step 1  填写 config.yaml（设备 IP / 账号 / 端口列表）
Step 2  在交换机上执行 show 命令，保存输出到 parsers/samples/
Step 3  根据样本输出，编写 parsers/parser.py 解析函数
Step 4  填写 baseline.yaml（第一次从设备读取实际值作为 baseline）
Step 5  运行 pytest，验证所有 PASS
Step 6  接入 CI/CD（可选）：每次固件发版后自动触发
```

---

## 七、依赖安装

```bash
pip install netmiko pytest pytest-html pyyaml
```

---

## 八、遗留问题（需确认后关闭）

| # | 问题 | 负责人 | 状态 |
|---|---|---|---|
| Q1 | 交换机平台类型（netmiko device_type）| | ⬜ 待确认 |
| Q2 | 查看模块识别信息的 show 命令 | | ⬜ 待确认 |
| Q3 | 查看 DDM 数据的 show 命令 | | ⬜ 待确认 |
| Q4 | 查看告警的 show 命令 | | ⬜ 待确认 |
| Q5 | 测试设备数量和端口数量 | | ⬜ 待确认 |
| Q6 | 是否需要接 CI/CD（Jenkins/GitLab）| | ⬜ 待确认 |
| Q7 | 报告是否需要发邮件通知 | | ⬜ 待确认 |
