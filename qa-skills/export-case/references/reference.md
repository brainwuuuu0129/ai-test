# 导出用例参考手册

## 1. FreeMind格式

**层级**：测试用例集 → 模块 → 功能 → 测试点(TP-xxx) → 用例(TC-xxx [P0][冒烟])

**颜色**：P0红色(#FF0000) / P1橙色(#FF6600) / P2蓝色(#0066FF)

**模板**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0.1">
  <node TEXT="测试用例集">
    <node TEXT="用户管理">
      <node TEXT="用户登录">
        <node TEXT="TP-001: 验证登录">
          <node TEXT="TC-001: 正确登录 [P0][冒烟]" COLOR="#FF0000">
            <node TEXT="前置条件: ..." />
            <node TEXT="测试步骤: ..." />
            <node TEXT="期望结果: ..." />
          </node>
        </node>
      </node>
    </node>
  </node>
</map>
```

## 2. Markdown格式

**层级**：# 用例集 → ## 模块 → ### 功能 → #### 测试点 → **用例（P0，冒烟）**

**模板**：
```markdown
# 测试用例

## 用户管理

### 用户登录

#### TP-001：验证登录

**TC-001：正确登录（P0，冒烟）**
- 前置条件：...
- 测试步骤：1. ... 2. ... 3. ...
- 期望结果：...
```

## 3. Excel格式

**表头（12列）**：模块/功能/测试点/用例ID/标题/优先级/类型/执行端/冒烟/前置/步骤/期望

**数组字段处理**：使用换行符`\n`分隔

```python
前置条件 = "\n".join([
    "账号/角色权限：...",
    "配置/灰度开关：...",
    "数据准备：...",
    "环境依赖：..."
])
```

## 4. 特殊字符转义

**FreeMind XML**：
- `<` → `&lt;` / `>` → `&gt;` / `&` → `&amp;` / `"` → `&quot;` / `'` → `&apos;`
- 或使用CDATA：`<![CDATA[...]]>`

**Markdown**：
- `*` → `\*` / `_` → `\_` / `[` → `\[` / `#` → `\#`
- 或使用代码块：`` `user_id=10001` ``

**Excel**：无需转义

## 5. 大型用例集处理

| 规模 | 策略 | 命令 |
|------|------|------|
| ≤200 | AI直接生成 | - |
| >200 | 分批导出 | `--split-by module` |
| >1000 | Python脚本 | `python scripts/export_case.py` |

**文件命名**：`{项目}_{模块}_测试用例_{日期}.{格式}`

## 6. 脚本使用

```bash
pip install openpyxl markdown xlsxwriter

python scripts/export_case.py \
  --format freemind \
  --input cases.json \
  --output test.mm \
  --split-by module
```

**参数**：`--format` (格式) / `--input` (输入) / `--output` (输出) / `--split-by` (分割)

## 7. 常见问题FAQ

| 问题 | 解决方式 |
|-----|---------|
| **FreeMind乱码** | 确保UTF-8编码，XML声明`encoding="UTF-8"` |
| **FreeMind打不开** | 检查特殊字符转义，标签闭合 |
| **Markdown层级错乱** | 检查#数量（模块##/功能###/测试点####） |
| **Excel列宽不够** | 选中列→双击边界自动调整 |
| **导出过慢** | 使用`--split-by`分批导出 |
| **Excel导入平台失败** | 检查表头顺序和字段名称是否与平台一致 |
