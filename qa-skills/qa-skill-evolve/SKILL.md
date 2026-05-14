---
name: qa-skill-evolve
description: 读取反馈日志，汇总 QA skill 的真实使用问题，准备好上下文后移交 skill-creator 执行改进循环。当用户说"进化skill"、"优化skill"、"skill有问题"，或反馈日志达到阈值提示后使用。
---

# QA Skill 进化入口

## 职责定位

本 skill 不自己做改动，而是做两件事：
1. **汇总** `_feedback/feedback-log.jsonl` 中积累的真实使用反馈
2. **组织上下文** 后移交 skill-creator 执行有验证保障的改进循环

> skill-creator 有完整的 eval 运行 → 人工评审 → 改动 → 回归测试流程，自己重复实现只会更脆弱。

---

## 执行流程

### Step 1: 读取并汇总反馈日志

读取 `_feedback/feedback-log.jsonl`，筛选 `evolved: false` 条目，按 skill 分组统计：

```
qa-prd-analysis (5条，均值 3.0)
  tag 频率：漏重要场景×3  追溯断链×2  优先级不准×1
  comments：
    - "漏了第三方回调场景"
    - "TP来源没有追溯到REQ编号"
    - （空）

qa-td-analysis (2条，均值 4.0)
  tag 频率：格式问题×1
  comments：（空）
```

若无待处理反馈：`✅ 暂无积压反馈` 并结束。

### Step 2: 判断处理方式

根据反馈量和信号质量给出建议：

| 情况 | 建议 |
|------|------|
| 某 tag 出现 ≥3 次 + 有具体 comment | → 信号足够，适合直接启动 skill-creator 改进 |
| 反馈量足够但 comment 大多为空 | → 先向用户追问，补充上下文再启动 |
| 反馈量少（1-2条）且信号弱 | → 继续积累，暂不进化 |
| 用户说"我就是想现在改" | → 直接启动，把反馈作为参考输入 |

**Comment 为空时的追问**（不要瞎猜根因）：
```
反馈 #3 标记了「漏重要场景」但没有描述具体场景。
能补充一下当时漏了什么吗？或者把原始 PRD 重新发我，
我们直接对比输出差异来定位问题。
```

### Step 3: 移交 skill-creator

确认启动后，先用 Glob 定位 skill-creator 的实际路径（版本 hash 可能随插件更新变化）：

```
Glob 模式：~/.claude/plugins/cache/claude-plugins-official/skill-creator/**/skills/skill-creator/SKILL.md
取第一个匹配结果，读取并执行。
```

向 skill-creator 提供以下上下文（作为"已有一个草稿需要改进"场景进入）：

```
目标 skill：qa-prd-analysis
当前 SKILL.md 路径：.cursor/skills/qa-prd-analysis/SKILL.md
改进依据（真实使用反馈）：
  - 漏重要场景×3："漏了第三方回调场景"、"漏了状态回滚路径"
  - 追溯断链×2："TP来源字段没追溯到具体REQ编号"

建议的测试用例：
  - 包含第三方回调的支付 PRD（可重现漏测场景）
  - 含多角色权限的 PRD（验证追溯链路）
```

skill-creator 会接管后续：运行 eval、生成 baseline 对比、人工评审、迭代改进。

### Step 4: 标记反馈为已移交

进化完成后（skill-creator 流程跑完、用户确认满意），将处理过的条目标记为 `evolved: true`：

```bash
python3 -c "
import json, os
log_path = os.path.join(os.getcwd(), '_feedback/feedback-log.jsonl')
lines = open(log_path).readlines()
result = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    entry = json.loads(line)
    if entry['skill'] == '<target_skill>' and not entry['evolved']:
        entry['evolved'] = True
    result.append(json.dumps(entry, ensure_ascii=False))
open(log_path, 'w').write('\n'.join(result) + '\n')
print('Done:', len(result), 'entries')
"
```

---

## 快捷触发语

- `进化 qa-prd-analysis` → 直接汇总该 skill 反馈并启动 skill-creator
- `看看反馈日志` → 只展示统计，不启动进化
- `全部进化` → 依次处理所有达到阈值的 skill
- `重置反馈 <skill名>` → 将该 skill 所有反馈标记 `evolved: true`（清空积压）
