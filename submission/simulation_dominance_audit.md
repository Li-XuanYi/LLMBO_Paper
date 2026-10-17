# 仿真支配关系核验（2026-10-17）

**结论：用于真机验证的所选 LLMBO-MO 协议，在仿真存档中严格优于所选
ParEGO 协议的三个目标；完整算法前沿之间不存在 LLMBO-MO 对 ParEGO 的整体支配。**

本次读取 `D:/Users/aa133/Desktop/BO_Multi_12_20/New_LLMBO` 的原始
`database.json` 和 `summary.json`，没有运行新仿真或调用 LLM。

## 所选协议：严格支配成立

两组来自 `Compare_Exp/experiment_records/seed8409_llmbo_vs_parego_50iter/seed8409/`。
两组配置均为 Chen2020、SOC 0 到 0.8，共 56 次评估。以下序号从 1 开始计数。

| 项目 | LLMBO-MO | ParEGO | LLMBO-MO 相对降低 |
|---|---:|---:|---:|
| 观测序号 | 7 | 52 | — |
| BO 迭代 | 1 | 46 | — |
| 充电时间（s） | 3883 | 4060 | 4.36% |
| 温升目标（K） | 4.5546980037 | 4.9989536406 | 8.89% |
| 老化指标 | 0.8897015906 | 0.9262181664 | 3.94% |
| 可行性标志 | true | true | — |
| 属于各自最终前沿 | 是 | 是 | — |

原始决策变量依次为 `[I1, I2, I3, dSOC1, dSOC2]`：

- LLMBO-MO：`[3.9004013729715443, 3.758672557096327, 3.0, 0.4, 0.2999756044248352]`。
- ParEGO：`[3.39711737007188, 4.788830209898036, 2.9916543657045156, 0.11476043063261704, 0.2972314382949903]`。

三个目标都要求最小化，因此这两个具体向量满足逐项严格小于。
老化值是模型给出的指标，不能解释为真机测得的容量损失。
结论针对原始未取整决策变量及存档结果；本次没有重跑硬件取整参数。

直接证据：

- [LLMBO-MO 第 7 条观测](D:/Users/aa133/Desktop/BO_Multi_12_20/New_LLMBO/Compare_Exp/experiment_records/seed8409_llmbo_vs_parego_50iter/seed8409/llmbo_mo/database.json:181)
- [ParEGO 第 52 条观测](D:/Users/aa133/Desktop/BO_Multi_12_20/New_LLMBO/Compare_Exp/experiment_records/seed8409_llmbo_vs_parego_50iter/seed8409/parego_matlab_reference/database.json:1846)
- [模拟器目标定义](D:/Users/aa133/Desktop/BO_Multi_12_20/New_LLMBO/pybamm_simulator.py:9)
- [模拟器约束检查及目标提取](D:/Users/aa133/Desktop/BO_Multi_12_20/New_LLMBO/pybamm_simulator.py:481)

## 完整前沿：整体支配不成立

仅使用可行且目标值有限的观测；删除完全相同的目标向量；重新计算最小化的非支配前沿。
点支配条件为所有目标不大于对方，且至少一个目标严格小于对方。

| 归档种子 | LLMBO-MO 前沿点数 | ParEGO 前沿点数 | 被 LLMBO-MO 支配的 ParEGO 点数 | 被 ParEGO 支配的 LLMBO-MO 点数 |
|---|---:|---:|---:|---:|
| 8409 | 37 | 45 | 1 | 4 |
| 8410 | 41 | 46 | 2 | 5 |
| 8411 | 47 | 48 | 3 | 1 |
| 8412 | 44 | 43 | 0 | 3 |
| 8413 | 42 | 48 | 2 | 2 |

没有一个种子满足“每个 ParEGO 前沿点均被至少一个 LLMBO-MO 点支配”。
seed 8409 中，所选 ParEGO 协议恰好是被 LLMBO-MO 支配的那个前沿点。
因此论文需要清楚说明统一的协议选取规则，不能用该配对代表整个前沿。

反例也直接存在：seed 8409 的 ParEGO 第 17 条观测
`[4161, 4.0139869587, 0.9238691088]`，在三个目标上都严格优于
LLMBO-MO 第 5 条观测 `[4226, 4.2448062591, 0.9562381509]`。
两条记录均位于各自算法的最终前沿。

## HV 口径需要核对

从论文结果清单指向的五个原始 `summary.json` 读取 `canonical_hv`：

| 种子 | LLMBO-MO HV | ParEGO HV |
|---|---:|---:|
| 8409 | 0.3848255592 | 0.3523110937 |
| 8410 | 0.3826048883 | 0.3760978309 |
| 8411 | 0.3939151243 | 0.3994554478 |
| 8412 | 0.3886212393 | 0.3792976103 |
| 8413 | 0.3741890250 | 0.3820582168 |

这组归档的均值是 **0.3848311672 对 0.3778440399**，相对差约 **1.85%**。
LLMBO-MO 的 HV 在其中三个种子上更高，在另外两个种子上更低。
论文当前的“ParEGO 五种子均值 0.3520、提升 9.3%”不能由这五份归档支持；
0.3523110937 实际对应这里的 seed 8409 单次结果。
若论文采用另一批实验，需要更新原始数据映射后重新计算。
这五份文件是历史归档组合，本次不据此声称统计显著性。

## 建议论文表述

> For the selected protocol pair from the Chen2020 seed-8409 archives, the
> LLMBO-MO protocol strictly Pareto-dominated the ParEGO protocol, reducing
> charging time, temperature rise, and the aging indicator by 4.36%, 8.89%,
> and 3.94%, respectively.

当前限定了 `selected ... protocol` 的句子有原始记录支持。
应避免将其改写为“LLMBO-MO 严格支配 ParEGO”或“LLMBO-MO 的整个前沿支配 ParEGO”。

可复算结果见 `simulation_dominance_audit.json`，复算脚本为
`analyze_simulation_dominance.py`：

```powershell
python submission/analyze_simulation_dominance.py --experiment-root D:/Users/aa133/Desktop/BO_Multi_12_20/New_LLMBO --output submission/simulation_dominance_audit.json
```
