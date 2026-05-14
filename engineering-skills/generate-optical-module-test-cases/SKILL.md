---
name: generate-optical-module-test-cases
description: 根据光模块规格书 + 平台 CLI 手册，生成兼容性/DDM监控/链路性能/热插拔4类测试用例（15字段竖向表格）
---

## 适用场景

用户提供光模块规格书（或参数摘录）+ 目标平台 CLI 手册，需要生成覆盖兼容性、DDM 监控、链路性能、热插拔 & 异常四个维度的功能测试用例。

## 规则依赖

执行前读取 `references/reference.md`，重点关注 §2（维度测试点展开）、§3（DDM 指标规范）、§5（优先级判定）。

---

## 执行流程

### Stage 1 — 模块理解 & 特性映射

读取输入文档，构建两张映射表：

**模块特性表**（从规格书提取）

| 字段 | 内容 |
|---|---|
| Form Factor | SFP / SFP+ / QSFP28 / QSFP-DD / AOC / DAC |
| Speed | 1G / 10G / 25G / 40G / 100G / 400G |
| Wavelength | 850nm / 1310nm / 1550nm / CWDM / DWDM |
| Connector | LC / MPO / RJ45 / DAC copper |
| DDM Support | Yes / No |
| Temp Range | 商业级 0~70℃ / 工业级 -40~85℃ |
| TX Power Range | Min ~ Max (dBm) |
| RX Power Range | Min ~ Max (dBm) |
| Alarm Thresholds | High Warn / High Alarm / Low Warn / Low Alarm（每项指标）|

**平台 CLI 映射表**（从 CLI 手册提取）

| 操作 | CLI 命令（真实，来自手册）|
|---|---|
| 查看端口光模块信息 | `<从手册提取>` |
| 查看 DDM 实时数据 | `<从手册提取>` |
| 查看端口状态 | `<从手册提取>` |
| 查看告警日志 | `<从手册提取>` |
| 配置告警阈值 | `<从手册提取，若支持>` |

> **严禁虚构命令**：若手册中无对应命令，在测试步骤中标注 `[需厂商确认CLI]`。

---

### Stage 2 — 测试点提取

按 4 个维度展开，详细规则见 `references/reference.md §2`：

| 维度 | 核心测试点 | P0 最小数 | P1 最小数 |
|---|---|---|---|
| 兼容性 | 识别、链路 UP、端口状态、speed/duplex 协商 | 4 | 2 |
| DDM 监控 | 温度/电压/TX功率/RX功率/偏置电流读数 + 告警阈值触发 | 5 | 4 |
| 链路性能 | 误码率、错误帧计数、光功率预算、最大传输距离 | 0 | 4 |
| 热插拔 & 异常 | 热插/热拔/非法模块拒绝/告警恢复 | 3 | 2 |

---

### Stage 3 — 测试用例生成

每条测试用例输出为 **15 字段竖向 Markdown 表格**：

```
| 字段 | 内容 |
|---|---|
| Test Name | [维度缩写]-[序号] [标题] |
| Purpose of Test | 验证目标 + 规格书条款引用 |
| Test Environment & Precondition | 平台型号/固件版本/模块型号/光纤类型 + 完整初始化 CLI |
| Test Procedure | 纯动作步骤（配置/执行/等待/拔插），禁止"验证/确认" |
| Expected Results | show 命令输出 / 数值范围 / 日志关键字 |
| Module Type | SFP / SFP+ / QSFP28 / QSFP-DD / AOC / DAC |
| Wavelength / Speed | 例：1310nm / 10G |
| DDM Required | Yes / No |
| Automated or Not | Manual / Automated |
| Related Scripts | 脚本路径或 N/A |
| Level | P0 / P1 / P2 |
| Hardware Model | 目标交换机型号 |
| Firmware Version | 固件版本 |
| Actual Results | （执行时填写）|
| Remark | 规格书页码引用 / 注意事项 |
```

**命名规范**：
- `COMPAT-001` 兼容性
- `DDM-001` DDM 监控
- `PERF-001` 链路性能
- `HOTSWAP-001` 热插拔 & 异常

**测试步骤动词规范**（只允许）：
配置 / 执行 / 等待 / 插入 / 拔出 / 重启 / 断开 / 连接 / 运行 / 记录

---

### Stage 4 — 覆盖验证 & 汇总

检查以下覆盖项，缺失则补充用例：

- [ ] 每个维度至少 1 个 P0
- [ ] 正常路径 + 异常路径 + 边界值均覆盖
- [ ] DDM 5 项指标全部出现（若模块支持 DDM）
- [ ] 热插/热拔两个动作各有独立用例
- [ ] 所有 CLI 命令来自输入手册（无虚构命令）
- [ ] AOC/DAC 无 DDM 时已标注跳过（见 `references/reference.md §6`）

输出汇总表：

```
| 维度 | P0 | P1 | P2 | 合计 |
|---|---|---|---|---|
| 兼容性 | x | x | x | x |
| DDM 监控 | x | x | x | x |
| 链路性能 | x | x | x | x |
| 热插拔 & 异常 | x | x | x | x |
| 合计 | x | x | x | x |
```

---

## 快速口诀

| 维度 | 口诀 |
|---|---|
| 命令来源 | 手册先行：先找命令再写步骤，无命令则标 `[需厂商确认CLI]` |
| DDM 阈值 | 规格书给阈值→用规格书；规格书无阈值→见 §3 典型值范围 |
| AOC/DAC | 无 DDM → DDM 维度用例全部标 `N/A (无DDM支持)` |
| 优先级 | 链路UP + DDM读数 + 热插拔 = P0；阈值告警 + 性能 = P1；极端边界 = P2 |
| 步骤动词 | 动作动词，不含"验证/确认/检查"——结果判断放 Expected Results |

---

## 核心示例

**输入**：
```
模块：FS SFP-10G-SR，10GBASE-SR，850nm，DDM支持，LC接口
平台CLI（示例）：
  show interface ethernet1/1 transceiver
  show interface ethernet1/1 transceiver detail
```

**Stage 1 输出（模块特性表摘要）**：
- Form Factor: SFP+，Speed: 10G，Wavelength: 850nm，DDM: Yes
- CLI 映射：识别 → `show interface ethernet1/1 transceiver`

**Stage 3 输出（用例示例）**：

| 字段 | 内容 |
|---|---|
| Test Name | COMPAT-001 SFP+ 10G 模块识别与链路建立 |
| Purpose of Test | 验证 SFP+ 10G SR 模块插入后平台正确识别型号、供应商、序列号，端口链路 UP |
| Test Environment & Precondition | 平台：[硬件型号]，固件：[版本]；模块：FS SFP-10G-SR；双端通过 OM3 多模光纤直连；初始状态：端口 shutdown |
| Test Procedure | 1. 将模块插入 ethernet1/1<br>2. 执行 `no shutdown` 启用端口<br>3. 等待 30s<br>4. 执行 `show interface ethernet1/1 transceiver`<br>5. 执行 `show interface ethernet1/1 status` |
| Expected Results | transceiver 输出显示：Vendor Name = FS，Part Number = SFP-10G-SR，Connector = LC；端口状态 = up/up |
| Module Type | SFP+ |
| Wavelength / Speed | 850nm / 10G |
| DDM Required | Yes |
| Automated or Not | Manual |
| Related Scripts | N/A |
| Level | P0 |
| Hardware Model | [填写] |
| Firmware Version | [填写] |
| Actual Results | （执行时填写）|
| Remark | 规格书第2页：Vendor PN = SFP-10G-SR |

---

## 参考资源

- [reference.md](references/reference.md) — 维度测试点展开、DDM指标规范、CLI模板、优先级规则、FAQ
