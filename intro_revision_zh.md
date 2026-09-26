# 引言中文译文

对应 `sections/introduction.tex`。文献编号与本次编译后的英文论文一致；译文供审阅，不插入英文正文。

锂离子电池快充需要在充电速度、热应力和老化之间取得平衡。对于给定的充电量，缩短充电时间意味着提高平均充电电流。然而，高倍率充电会加剧极化和产热，并可能促进电池老化，其影响取决于温度和荷电状态（SOC）等条件 [1]。因此，充电协议设计需要确定各充电阶段的电流变化方式，在满足规定的电流、电压和温度限制的同时达到目标 SOC。充电时间、热响应和电池健康之间存在相互竞争的目标，因此可将其表述为受约束的多目标优化问题，为不同运行偏好提供可供选择的充电协议 [2,3]。

评估这些权衡需要付出较高成本。实体电池的充电与老化试验需要消耗电芯和实验时间，尤其是直接测量循环寿命可能需要数月 [4]。电池模型能够通过仿真评估候选协议，从而减少设计阶段对实物试验的依赖。不过，电化学模型仍需要反复数值求解耦合的传输与反应方程，并且通常还需考虑热过程和老化动态。因此，以仿真替代实验虽然降低了单次评估的成本，却并未消除在大量候选协议中搜索所带来的计算负担 [5,6]。减少仿真器的评估次数，因而成为充电协议优化中的一个重要目标。

贝叶斯优化（BO）通过序贯代理建模和基于采集函数的采样来应对这一评估成本。概率代理模型通常采用高斯过程（GP），利用已评估的候选方案估计目标函数值及其预测不确定性。采集函数结合这两类估计选择下一个候选方案，使优化器能够先借助计算成本较低的代理模型比较大量候选方案，再调用电池仿真器评估选出的协议 [7]。在这一设置中，BO 将仿真器视为黑箱评估器，而不是替代底层电化学模型。

已有研究表明 BO 适用于快充设计。Attia 等将循环寿命早期预测与 BO 相结合，通过实验优化快充协议，同时减少测试持续时间和测试次数 [4]。Jiang 等研究了满足老化相关约束的最短时间充电 BO 方法，并比较了多阶段充电协议下不同采集函数的表现 [5]。Wang 和 Jiang 随后采用切比雪夫标量化与约束 BO，将这一思路拓展到充电时间与循环寿命的权衡 [6]。近期，Zhu 等将老化早期预测与多目标 BO 结合，同时考虑老化轨迹膝点处的容量和循环寿命 [8]。此外，GP 辅助的进化充电设计也在减少仿真需求的同时考虑了多种用户偏好 [3]。这些研究为在有限观测条件下评估充电性能权衡奠定了基础。

进一步的改进机会，是在决定评估哪些候选协议时利用电池领域知识。在新的优化运行尚未积累大量观测之前，充电阶段、热响应与老化之间的关系就能够提供定性指导。这类信息可以补充用于拟合代理模型的数值输入—输出数据。已有研究将先验引导的 BO 用于电池充电：Jeong 等引入简化老化模型，引导兼顾电池健康的充电协议搜索 [9]。这一工作引出了一个互补问题：如何使通过充电变量含义与运行要求表达的定性知识，能够被多目标采集策略实际利用？

大语言模型（LLM）提供了一种理解上述描述，并结合优化上下文提出候选方案的途径。Liu 等提出 LLAMBO，研究了基于 LLM 的热启动、代理建模和候选采样，并在超参数优化任务中开展了实证评估 [10]。在电池领域，Kuai 等将 LLM 增强的 BO 用于电化学参数辨识 [11]。这些结果为研究 LLM 辅助充电设计提供了动机。在充电设计中，决策变量定义的是运行协议，优化目标则是在充电时间、温升和老化之间获得一组可行的权衡方案。

在仿真预算较少时，引入这类知识需要考虑两个方面。第一，仅根据变量边界构建的初始设计，并没有显式利用充电知识来选择最先评估的协议。引入这些知识时，需要兼顾 LLM 建议的预期质量与初始设计的多样性。第二，在序贯优化过程中，对某个区域的定性偏好需要同时联系当前强调的目标权衡，以及由已有观测训练得到的 GP。有效的融合机制应将这种偏好转化为对采集函数排序的调整，并在语言先验不可靠时限制其影响。这两个要求分别对应初始化阶段和后续候选选择阶段对额外先验信息的利用。

本文提出面向多阶段电池充电的大语言模型引导多目标贝叶斯优化方法（LLMBO-MO）。该方法在基于分解的 BO 框架中，将 LLM 引导的初始化与基于后验协方差的 Region-Lift 机制相结合。LLM 提供候选充电协议和区域偏好，电池仿真器则确定目标函数值与可行性。本文的主要贡献如下：

1. 提出一种 LLM 引导的初始化策略，利用充电变量定义、运行约束和电池领域知识生成初始协议建议。通过候选筛选、考虑多样性的选择以及随机有效协议的补充，构建初始仿真设计。
2. 提出基于后验协方差的 Region-Lift 机制，使用锚点表示 LLM 建议的区域，并利用 GP 后验交叉协方差，在当前目标权重下调整期望改进采集函数的候选排序。调整幅度受到限制，并在早期迭代中逐渐衰减；当区域偏好无法使用时，方法回退为标准期望改进。
3. 在有限仿真预算下，使用 Chen2020 和 Ecker2015 两组电池参数评估 LLMBO-MO。通过与 BO 及其他多目标优化器的比较、初始化实验、系统层面的消融实验和充电轨迹分析，评估优化性能以及 LLM 辅助的实际作用。

本文其余部分安排如下：第二节和第三节分别介绍充电问题与电池模型；第四节介绍 LLMBO-MO；第五节报告实验结果；第六节总结全文。

## 译文引用的文献

1. Tomaszewska et al., *eTransportation*, 2019. [Lithium-ion battery fast charging: A review](https://doi.org/10.1016/j.etran.2019.100011)
2. Liu et al., *IEEE Transactions on Industrial Informatics*, 2018. [Charging pattern optimization for lithium-ion batteries with an electrothermal-aging model](https://doi.org/10.1109/TII.2018.2866493)
3. Wang et al., *IEEE Transactions on Industrial Informatics*, 2024. [Gaussian process-accelerated multiobjective evolutionary design of charging process considering multiple user preferences](https://doi.org/10.1109/TII.2024.3388602)
4. Attia et al., *Nature*, 2020. [Closed-loop optimization of fast-charging protocols for batteries with machine learning](https://doi.org/10.1038/s41586-020-1994-5)
5. Jiang et al., *Applied Energy*, 2022. [Fast charging design for lithium-ion batteries via Bayesian optimization](https://doi.org/10.1016/j.apenergy.2021.118244)
6. Wang and Jiang, *Journal of Power Sources*, 2023. [Multi-objective optimization for fast charging design of lithium-ion batteries using constrained Bayesian optimization](https://doi.org/10.1016/j.jpowsour.2023.233602)
7. Shahriari et al., *Proceedings of the IEEE*, 2016. [Taking the human out of the loop: A review of Bayesian optimization](https://doi.org/10.1109/JPROC.2015.2494218)
8. Zhu et al., *IEEE Transactions on Transportation Electrification*, 2025. [Fast-charging protocols design of lithium-ion battery: A multiple-objective Bayesian optimization perspective](https://doi.org/10.1109/TTE.2025.3539853)
9. Jeong et al., *Journal of Energy Storage*, 2026. [Health-conscious charging of lithium-ion batteries using Bayesian optimization guided by a semi-empirical aging model](https://doi.org/10.1016/j.est.2025.119348)
10. Liu et al., *ICLR*, 2024. [Large language models to enhance Bayesian optimization](https://proceedings.iclr.cc/paper_files/paper/2024/file/84b8d9fcb4e262fcd429544697e1e720-Paper-Conference.pdf)
11. Kuai et al., *Journal of Energy Storage*, 2025. [Large language model-enhanced Bayesian optimization for parameter identification of lithium-ion batteries](https://doi.org/10.1016/j.est.2025.118198)
