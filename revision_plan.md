# LLMBO-MO 审稿批注修复计划

## 1. 批注读取结论

可以读取。已用 PyMuPDF 检查原始 PDF，结果如下：

| 项目 | 结果 |
|---|---|
| 文件页数 | 12 页 |
| 批注总数 | 27 条 |
| 批注类型 | 全部为下划线文字批注 |
| 批注分布 | 第 1、2、3、5、7、11 页 |
| 正文是否被编辑 | 否，批注为独立注释层 |
| 加密/密码阻挡 | 无 |
| 空批注 | 1 条，位于第 5 页公式 (8) 处，只有下划线，没有文字 |

因此可以将这 27 条批注全部纳入修订计划。

## 2. 总体判断

| 项目 | 结论 |
|---|---|
| 建议处理等级 | Major Revision / Revise and Resubmit |
| 主要问题 | 研究定位不清、动机链不完整、实验设计逻辑需要重组、图表可读性不足 |
| 修订工作量 | Substantial |
| 优先策略 | 先重写定位与 Introduction，再调整实验设计，最后统一图表和语言 |

## 3. 核心问题与修复动作

### P1：必须修复

#### P1-1 重构论文定位和研究动机

审稿人多次指出，当前论文没有说清楚“到底是在什么基础上改进什么”。

建议把定位收敛为一条主线：

> 在 ParEGO 这类 scalarization-based multiobjective BO 的 early-search 阶段，利用 LLM 的 battery-domain textual knowledge 做 knowledge-informed warm start 和 bounded regional guidance；LLM 只提供搜索偏好，数值证据仍由 battery simulator 唯一生成。

不要同时宣称：

- 在现有 MOBO 上做 knowledge-informed initialization；
- 在现有 LLM-assisted BO 上改进 prior utilization；
- 提出全新的多目标分解或 Pareto 搜索机制。

这三者现在是并列、模糊的。修订时应明确：

1. 问题：battery fast-charging 仿真昂贵，BO cold-start 数据稀缺。
2. 技术瓶颈：现有 BO 早期初始化依赖 random/LHS，现有 LLM-BO 又容易把 LLM 输出当成 observation。
3. 现有路线为何不足：数值先验不总能获得；LLM 先验有用，但不能进入 evidence chain。
4. 本文切入点：在 warm start 和 early acquisition guidance 两个 LLM touchpoint 上引入 bounded, simulator-grounded guidance。

#### P1-2 重写 Abstract

当前 Abstract 被批注指出存在定位、语言、结果呈现三类问题。建议按以下结构重写：

1. 第一句先讲行业问题：电动车/储能对快充的需求，以及快充时间、温升、老化之间的冲突。
2. 点出 constrained multiobjective optimization，但不要过度强调本文改进了多目标机制。
3. 用自然语言说明 BO 因 sample efficiency 被广泛使用。
4. 清楚提出两个真实问题：
   - BO 在 limited budget 下 early search 对 initial design 敏感；
   - 现有 LLM-BO 方法可能把 LLM-generated values 当作 objective evidence。
5. 用一句或两句说明解决思路：
   - 本文把 search guidance 和 optimization evidence 分离；
   - LLM 只建议搜索位置，simulator 负责 objective/feasibility/GP/Pareto。
6. 结果只保留概括性收益，不写实验分析：
   - Chen2020 上相对 ParEGO 的平均 HV 优势；
   - Ecker2015 上的一致性；
   - warm-start controlled study 的主要提升。

需要删除 Abstract 中的：

- seed-8409 trajectory 的 9.2% 对比；
- p = 0.005859；
- 三-seed ablation 的 mean、dispersion、two of three seeds；
- “All optimization evidence remains simulator grounded”这类容易让读者困惑的收尾。

#### P1-3 重写 Introduction 的逻辑链

审稿人对 Introduction 的主要意见是“问题不明确、综述不聚焦、层次混乱、重复”。建议改成以下顺序：

1. 电池快充的重要性。
2. 快充协议设计为什么是 constrained multiobjective problem。
3. 评价目标为什么昂贵：battery model 是 SPMe/电化学-热耦合 PDE，求解本身昂贵；若加上物理实验或长循环老化，评价成本更高。
4. BO 为什么适合这个问题，以及 early-search cold-start 的不足。
5. 已有 battery charging 优化研究如何改进 BO，但主要依赖 numerical priors。
6. LLM 能提供 textual/qualitative battery knowledge，但现有 LLM-BO 对 LLM output 的 evidence status 处理不清。
7. 本文方法：两个 bounded LLM touchpoints，simulator 仍为唯一 evidence source。
8. 贡献。

需要修正的具体句子：

- “Model-based optimization”要区分是 data-driven surrogate model 还是物理电池模型。审稿人认为当前语境更像 physical model。
- “Nevertheless, long charging time and charging-induced degradation remain two major obstacles...”这句话表意不清，需要改写为“快充会缩短时间，但会加剧温升和老化”。
- “One challenge...”前缺少“多目标问题本身也是挑战”或“为什么先讲评价成本”的过渡。
- 不要重复解释 BO 的原理，除非第一次引入。

#### P1-4 重组 Literature Review

审稿人明确说“综述怎么还分两层”，建议改为两个并列块，而不是电池/更广泛两层嵌套：

**Block 1：先验嵌入方式与 battery BO 改进**

- 各类 numerical prior 如何改进 battery fast-charging BO；
- 这些方法的优点；
- 它们仍依赖 calibrated models/measurements/historical data，不能普遍获得。

**Block 2：LLM-assisted BO 与 textual prior**

- LLAMBO、LABO、preference-guided LLM-BO、battery-specific LLM-BO；
- 它们的贡献；
- 但现有方法对 LLM output 是否应作为 objective/observation 的问题没有明确处理；
- 本文的切入点。

最后用“问题驱动”的句子衔接方法：

1. 因 expensive simulation + scarce early data；
2. 因 battery-domain textual knowledge 可用但 LLM output 不是 evidence；
3. 本文提出 LLMBO-MO；
4. 两句方法概述；
5. 贡献。

#### P1-5 强化多目标问题的数学表达

审稿人指出 Section II 标题下没有立即看到数学形式。修订时建议：

- 在 Section II 开头明确写“Problem Formulation”；
- 尽早给出 decision vector、objective vector、constraints 的完整数学定义；
- 保持 equation (1)-(2)，但增加简短的 notation table；
- 明确哪些是 box constraints，哪些是 simulator-checked path constraints；
- 明确 Pareto set 的定义，并说明 scalarization-based MOBO 如何获得近似 Pareto front。

#### P1-6 重新设计 Figure 2

当前 Figure 2 被审稿人认为“放这个干嘛、图不好”。建议重画为一个清晰的方法框架：

- 左侧：constrained warm start；
- 中间：numerical multiobjective BO loop；
- 右侧：bounded early regional guidance；
- 明确所有箭头最终回到 simulator evaluation；
- 明确 gate 的作用是 domain admissibility，不是 simulator feasibility；
- 用不同颜色区分 LLM guidance 和 simulator evidence。

#### P1-7 重新设计实验逻辑与 baseline

审稿人质疑：

- 为什么要比较这些算法；
- 为什么没有最基础的 MOBO；
- 为什么比较 normalization methods；
- 为什么不比较不同 LLM；
- EIMO/Ecker2015 是否只是应审稿人要求补做。

建议实验逻辑改成：

1. **主实验**：LLMBO-MO vs ParEGO，因为两者共享 scalarization-GP backbone，能隔离 warm start/guidance 的作用。
2. **MOBO baseline 补强**：至少加入一个非 scalarization 的 multiobjective BO baseline，例如 EHVI/qNEHVI，或引用 battery charging 中已有的 MOBO 方法，说明“基础 MOBO”已有覆盖。
3. **算法对比**：保留 NSGA-II、DISK、PIMD，但说明它们回答的是 fixed-budget 下不同优化范式的问题，不是核心机制证据。
4. **机制实验**：
   - controlled prompt study 保留；
   - matched short-budget ablation 保留；
   - objective-scaling sensitivity 和 archive growth 移到 Appendix。
5. **LLM 因素**：要么增加 LLM backend/prompt 的 controlled comparison，要么在 Discussion/Limitations 明确说明这是 future work，并解释为什么当前没有做。
6. **Ecker2015/EIMO 澄清**：当前正文没有 EIMO，只有 Ecker2015。需要与审稿人/作者确认 EIMO 是否指 Ecker2015。若是历史审稿人要求补做的内容，应明确其作用是 robustness case，而不是主结果；若对方法机制无贡献，移到 Appendix 或说明理由。

#### P1-8 结果表述收敛

建议统一结果表述：

- 主结果只报告 fixed-budget final HV；
- 5-run endpoint 是 descriptive，不要与 inferential 混用；
- 显著性只放在 controlled prompt/component studies；
- seed-level trajectory gap 不要在 Abstract 和 Conclusion 中当成主要卖点；
- 所有 percentage advantage 要注明是相对差还是绝对差，避免误读。

### P2：应当修复

#### P2-1 表 I 内容调整

审稿人意见：

- “列参数信息，不要列实验信息”；
- “正文不要列这个”。

修订动作：

- Table I 只保留参数信息：battery parameterizations、protocol bounds、initialization calls、BO iterations、GP kernel、acquisition、scalarization、guidance horizon、anchors、LLM model version。
- 将 seeds、run IDs、seed ranges、batch 信息移到 reproducibility appendix 或 supplementary。
- 正文中删除 `Chen2020 seeds 8409–8413 Ecker2015 seeds 8409–8413` 这类纯运行记录。

#### P2-2 图表字体和尺寸统一

审稿人指出：

- Figure 1 字太小；
- Figure 6/7 字看不清；
- 图表字体和大小参考 EIMO。

修订动作：

- 统一所有 figure 的 axis label、tick、legend、caption 字号；
- Figure 1 的流程文字放大到与正文相近；
- Figure 6 和 7 的坐标轴、图例、标注重新排版；
- 检查 Table II-V 的表格字距和列宽。

#### P2-3 清除不自然的术语和表达

需要替换的表达：

| 原表达 | 建议 |
|---|---|
| physical evidence | simulator-validated evidence / simulator-validated observation |
| small initial design | small initial observation set / scarce cold-start data |
| optimization evidence | objective evidence chain |
| 令人困惑的 “In both cases...” | 改成明确的 evidence boundary 说明 |

#### P2-4 处理意义不明的句子

以下批注需要逐句澄清：

- “the simulator remains the sole objective oracle and only evaluated protocols are used...”需要改写为“LLM 不生成 observation；只有 simulator-evaluated protocol 进入 GP/Pareto”。
- “Nevertheless, long charging time...”需改成明确因果关系。
- “For example,”如无必要删除。

### P3：可考虑

- 删除重复的 BO 原理说明。
- 检查 Section II 的 equation numbering 和符号定义是否完整。
- 第 5 页公式 (8) 处只有空白下划线，无文字。建议检查该公式的变量定义是否清晰；如无法确认审稿人意图，可在 Response Letter 中说明已重新核对公式。
- 检查全文是否存在未定义缩写，如 SOC、MCC、SPMe、GP、EI、HV。

## 4. 批注逐条映射表

| 编号 | 页码 | 批注涉及内容 | 审稿意见摘要 | 修复动作 | 优先级 |
|---|---|---|---|---|---|
| A1 | 1 | 标题/Abstract | 方法定位不清晰，两个并列研究目标难放一篇论文 | P1-1 重构定位 | P1 |
| A2 | 1 | Abstract 首句 | 不要过度强化多目标；首句讲行业重要性 | P1-2 重写 Abstract | P1 |
| A3 | 1 | Abstract BO 句 | 改为 BO 因某特点而广泛使用 | P1-2/P2-3 | P2 |
| A4 | 1 | Abstract 两个问题 | 两个问题表述不清，用词不当 | P1-2/P2-3 | P1 |
| A5 | 1 | Abstract “multiobjective” | 如果不针对多目标改进，就不要强化约束表述 | P1-2/P1-5 | P1 |
| A6 | 1 | Abstract “evidence.” | 只写“？”，含义不明 | P2-4 澄清 | P2 |
| A7 | 1 | Abstract 方法句 | 应写解决思路，不是机械列方法 | P1-2 | P1 |
| A8 | 1 | Abstract oracle 句 | 意义不明 | P1-2/P2-4 | P1 |
| A9 | 1 | Abstract 结果段 | 不应在 Abstract 分析实验 | P1-2/P1-8 | P1 |
| A10 | 1 | Intro 首段长句 | 句意不清 | P1-3/P2-4 | P2 |
| A11 | 1 | Intro 首段前半句 | “？什么意思” | P1-3/P2-4 | P2 |
| A12 | 1 | Abstract/Intro 长段 | 冗长，未写清研究电池快充优化的重要性 | P1-2/P1-3 | P1 |
| A13 | 1 | Intro challenge 句 | 逻辑跳跃，应先讲 PDE/物理实验昂贵 | P1-3 | P1 |
| A14 | 1 | Intro “Model-based optimization” | 需区分 data-driven surrogate 与 physical model | P1-3 | P1 |
| A15 | 1 | Intro previous studies | 应另起一段，并说明这些方法优点 | P1-4 | P2 |
| A16 | 1 | “For example,” | 没必要 | P2-4 | P3 |
| A17 | 1 | BO 原理段 | 与前面重复 | P1-3 | P2 |
| A18 | 1 | BO early stage 段 | 又提出一个问题，逻辑重复 | P1-3/P1-4 | P1 |
| A19 | 1 | Recent charging studies | 文献综述不聚焦 | P1-4 | P1 |
| A20 | 1 | Beyond battery charging | 综述分两层，且出发点没讲清 | P1-4 | P1 |
| A21 | 2 | Section II 标题 | 没有立即给出数学形式 | P1-5 | P1 |
| A22 | 3 | Figure 1 | 图字太小 | P2-2 | P2 |
| A23 | 5 | Figure 2 | 方法框架不清晰，图不好 | P1-6 | P1 |
| A24 | 5 | 公式 (8) | 空白下划线，无文字 | 检查公式定义并回复 | P3 |
| A25 | 7 | seeds 列表 | 正文不要列 seeds | P2-1 | P2 |
| A26 | 7 | Table I | 列参数信息，不列实验信息 | P2-1 | P2 |
| A27 | 11 | Figure 6/7 | 字体和大小不清楚，参考 EIMO | P2-2 | P2 |

## 5. 建议修订顺序

### Pass 1：重写叙事

1. 重写 Abstract。
2. 重写 Introduction 的问题链。
3. 重组 Literature Review。
4. 重写 Contributions，去掉实验细节。

### Pass 2：强化方法

5. 强化 Section II 的数学 formulation。
6. 重画 Figure 2。
7. 统一 evidence boundary 的术语。

### Pass 3：调整实验

8. 增加基础 MOBO baseline。
9. 重排 Table I，把实验运行信息移到 appendix。
10. 将 objective-scaling 和 archive-growth 等外围诊断移到 appendix。
11. 澄清 Ecker2015/EIMO 和 LLM backend 比较。

### Pass 4：图表和语言

12. 统一 Figure 1、2、3、4、5、6、7 的字体和尺寸。
13. 清理 unclear sentences 和术语。
14. 删除重复 BO 原理说明。

### Pass 5：验证

15. 用 Response Letter 逐条回复 A1-A27。
16. 重新运行 citation check。
17. 核对所有公式和符号定义。

## 6. 修订完成检查清单

- [ ] 所有 27 条批注都有对应动作。
- [ ] Abstract 不再分析实验细节。
- [ ] Introduction 只有一条清晰的问题链。
- [ ] Literature Review 是两大块，不是两层嵌套。
- [ ] 论文只声明一个明确的技术改进方向。
- [ ] Section II 有完整的数学 formulation。
- [ ] Figure 2 是清晰的方法框架。
- [ ] Table I 只列参数信息。
- [ ] 所有实验运行信息在正文外可见。
- [ ] 所有图表字号清晰可读。
- [ ] 所有 unclear sentences 已改写。
- [ ] Response Letter 覆盖全部批注。
