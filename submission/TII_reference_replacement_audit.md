# TTE → TII 引用替换记录

核验日期：2026-10-17。修改对象为 `LLMBO_MO/IEEE_TII/main.tex`。

六篇替换文献均在 Crossref 的出版商登记记录中查到完整作者、题名、TII
刊名、正式卷期、页码、出版年及 DOI。原有 28 个引用键和排列顺序保留，
实验数据、模型公式、算法章节和结论未改动。

## 一一对应关系

| 编号／原引用用途 | 新的真实 TII 文献 | 与正文的对应处理 |
|---|---|---|
| [2] Tu：快充背景、热与老化风险 | Y. Gao et al., “Health-Aware Multiobjective Optimal Charging Strategy With Coupled Electrochemical-Thermal-Aging Model for Lithium-Ion Battery,” 16(5), 3417–3429, 2020. [DOI](https://doi.org/10.1109/TII.2019.2935326) | 保持“充电速度、热应力与老化之间存在权衡”的引用用途。新文献是耦合模型和健康感知快充研究，不称其为综述。 |
| [4] Fan：多目标充电与运行偏好 | Q. Ouyang, J. Chen, J. Zheng, and H. Fang, “Optimal Multiobjective Charging for Lithium-Ion Battery Packs: A Hierarchical Control Approach,” 14(9), 4243–4253, 2018. [DOI](https://doi.org/10.1109/TII.2018.2825245) | 支撑用户需求、温度和运行约束下的多目标充电。该文研究电池组，正文保持一般性的充电设计表述。 |
| [5] Hu：约束下的最优充电控制 | N. Tian, H. Fang, and Y. Wang, “Real-Time Optimal Lithium-Ion Battery Charging Based on Explicit Model Predictive Control,” 17(2), 1318–1330, 2021. [DOI](https://doi.org/10.1109/TII.2020.2983176) | 保持约束充电设计、速度与健康保护的用途，不把该文描述为 NCA 多阶段电化学模型研究。 |
| [11] Dong：安全约束下的快充优化 | G. Dong, Z. Zhu, Y. Lou, J. Yu, L. Wu, and J. Wei, “Optimal Charging of Lithium-Ion Battery Using Distributionally Robust Model Predictive Control With Wasserstein Metric,” 20(5), 7630–7640, 2024. [DOI](https://doi.org/10.1109/TII.2024.3363079) | 研究对象仍为锂电池充电，保留第一作者 Dong；对应句改为 Wasserstein 分布鲁棒 MPC，避免沿用原来的 BO 方法描述。 |
| [12] Zhu：兼顾老化与评估成本的快充设计 | Y. Hao, Q. Lu, X. Wang, and B. Jiang, “Adaptive Model-Based Reinforcement Learning for Fast-Charging Optimization of Lithium-Ion Batteries,” 20(1), 127–137, 2024. [DOI](https://doi.org/10.1109/TII.2023.3257299) | 对应句改为微分 GP 代理与自适应模型强化学习、老化及电压温度约束。保留快充、老化和样本效率的主题，不保留原文献特有的 BO、容量拐点描述。 |
| [18] Bian：LLM 电池 SOC 估计 | L. Hou, Y. Shang, T. Qiu, X. Zhang, Y. Zhu, and X. Gu, “Prompt-Driven Fine-Tuning Large Language Model for Multistate Coestimation of Lithium-Ion Batteries,” 22(8), 6647–6658, 2026. [DOI](https://doi.org/10.1109/TII.2025.3631017) | 改为 Hou 等人的提示驱动微调和 SOC/SOH 联合估计，保持 LLM 用于电池状态估计这一直接对应关系。 |

## 正文衔接

BO 的基础研究仍由 Attia、Jiang、Wang 和 Jiang 等原有文献支撑。
新增的 MPC 和强化学习工作用 `Complementary approaches` 引入；
关于主要依赖数值观测的总结明确限定到 BO 方法。
LLM 状态估计文献作为相关电池应用实例，而不是当前优化方法有效性的证明。

## 内容核验来源

- [Ouyang 等人的作者稿](https://www.issl.space/uploads/2/5/6/5/25657441/tii-2018-multi-objective-charging.pdf)：摘要和引言说明多目标调度、用户需求、温度、运行约束及电池组范围。
- [Tian 等人的作者机构记录及摘要](https://www.merl.com/publications/TR2020-090)：说明显式 MPC、约束优化、健康感知充电及实时实现。
- [Dong 作者实验室发表清单](https://dib-lab.com/publications/)：确认同一作者的 TII 分布鲁棒 MPC 论文及其正式出版信息。
- [Hao 等人的 IEEE 论文页](https://ieeexplore.ieee.org/document/10070849/)：摘要说明微分 GP、自适应模型强化学习、老化及电压温度约束。
- [Hou 等人的 IEEE 论文页](https://ieeexplore.ieee.org/document/11573808/)：摘要说明预训练语言模型、数值文本融合、SOC/SOH 联合估计及参数高效微调。
- Gao 等人的题名、期刊与出版信息由 [Crossref 出版商登记记录](https://api.crossref.org/works/10.1109/TII.2019.2935326)核验，引用用途限定为健康感知、电化学热老化耦合的多目标充电背景。

## 可复核文件

- `tii_replacement_crossref.json`：六条原始 Crossref 返回记录。
- `tii_replacement_verified.bib`：依据 API 元数据生成的完整 BibTeX。
- `tii_replacement_validation.json`：citation-management 校验结果，6 条有效，0 错误、0 警告、0 重复。
- `fetch_tii_references.py` 和 `tii_replacement_dois.txt`：公开 DOI 的元数据获取脚本与清单。

BibTeX 文件是核验与复用材料；正式论文仍使用主稿中的 `thebibliography`。
原来的引用键保留为兼容标识，不代表替换后论文的作者或方法名称。
