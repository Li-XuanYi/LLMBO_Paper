# Region-Lift 双模型验证方案

## 要验证的核心命题

当前恢复的是基于后验协方差的 Region-Lift，而不是简单地把采集点强行移进 LLM 给出的区域。LLM 只提供一个带置信度的偏好区域；算法从该区域选取锚点，并通过 GP 后验协方差把锚点偏好平滑传播到候选点的采集值。离锚点相关性越高，提升越大；相关性弱或置信度不足时，影响会衰减或完全回退到普通 EI。

这套说法对应代码中的 `posterior_covariance` shift source。它保留原 GP 的预测均值和不确定度，改变的是采集决策中的偏好项，因此不应描述成“修改了 GP 后验”或“直接改变协方差矩阵”。

## 配对实验

每个模型分别运行同一组种子 `8409–8413`，每次均为 3 个 LLM warm-start 点、3 个随机初始点和 50 次 BO 迭代。相同种子下复用同一 warm-start 缓存，确保四个实验臂从同一批初始观测出发。

实验臂：

1. `warmstart_plain_ei`：不使用 Region-Lift，是主要基线。
2. `warmstart_region_lgbo_proposition1`：真实语义区域 + 后验协方差传播，是目标方法。
3. `sham_region_lgbo_proposition1`：保留调用次数、区域形状和置信度，但确定性移动区域，用于排除“多调用一次 LLM”或“任意局部框”带来的效果。
4. `random_region_lgbo_proposition1`：固定随机区域 + 相同协方差传播，用于检验收益是否来自语义信息，而不只是协方差偏置本身。

先对两个种子各运行 12 次 BO 迭代作为 pilot；只有通过 runner 内置门槛才继续完整的五种子、50 迭代实验。这能在模型/端点不兼容或 Region 实际未生效时及时停止消耗。

## 主要比较与报告口径

- 主效应：目标方法减去 plain EI，做种子内配对比较。
- 语义有效性：目标方法减去 sham control。
- 机制有效性：目标方法减去 random-region control。
- 最终性能：第 56 次总评估后的 canonical hypervolume。
- 早期性能：pilot 结束（总评估数 18）时的 hypervolume，以及完整轨迹。
- 机制审计：Region 接受率、acquisition lift 实际启用率、相对 plain EI 的选点变化率、fallback 原因。

`deepseek-v4-flash` 与 `deepseek-v4-pro` 的结果应先各自作为独立的稳健性实验报告。若直接比较模型优劣，需说明两种模型可能同时改变 warm-start 和 Region 建议，因而该差异不是纯粹的 Region 推理能力效应。

## 安全启动

只允许使用通用、按量计费的 Ark API Key 和通用端点 `https://ark.cn-beijing.volces.com/api/v3`。Coding Plan 专用凭证及 `/api/coding/v3` 端点不用于这一非编程 API 批处理实验。

在新 PowerShell 会话中临时设置环境变量后运行：

```powershell
$env:ARK_API_KEY = "<general-ark-api-key>"
& ".\scripts\run_region_lift_ark.ps1" -ConfirmGeneralArkKey
Remove-Item Env:ARK_API_KEY
```

脚本不会把密钥写入文件或命令行参数；它只在当前进程中映射给现有实验 runner，并在结束后恢复环境。
