# Codex 额外点数余额：任务栏显示设计

本设计从 `codex/upstream-appearance-pr` 分支创建。已选择 B 方案并接入运行时界面。效果图中的 `939.7` 是示例数值。

| 方案 | 效果图 | 使用方式 | 代价 |
| --- | --- | --- | --- |
| A 行内数字 | [PNG](codex-credit-option-a.png) | 现有两行右侧追加“点数 939.7” | 语义清楚，占用少量宽度 |
| B 双行余额 | [PNG](codex-credit-option-b.png) | 右侧上下排“额外点数”和余额 | 最易扫读，占用更多宽度 |
| C 紧凑入口 | [PNG](codex-credit-option-c.png) | 任务栏放 `+ 939.7`，点开看详情 | 任务栏较窄，需新增交互 |

数据设计：沿用现有 `wham/usage` 请求中的 `credits.balance`，不增加新的登录方式或请求。显示开关位于“显示用量”子菜单，默认关闭并保存到 `settings.json`。开启后，仅当 `has_credits` 为真、`unlimited` 为假且余额有效时显示；余额未知时不显示数字。点数余额没有可用于进度条的固定总上限，因此不绘制进度条。余额保留一位小数，较大数值使用 `k` 或 `M` 缩写。
