# Peer Review Report — Domain Reviewer (R2)

## Manuscript Information
- **Title**: Battery Fast-Charging Protocol Design via Large Language Model-Guided Multiobjective Bayesian Optimization
- **Review Date**: 2026-08-27
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 — Domain

### Reviewer Identity
Battery charging design and battery management domain expert, with publications on electrochemical-thermal modeling (SPMe, P2D, single-particle), aging proxies, and CC-CV / multistage constant-current protocols. Has worked on both model-based and data-driven optimization for fast-charging protocol design.

### Review Focus
1. SPMe simulation setup in Chen2020 / Ecker2015: are the parameters, boundary conditions, and constraints reasonable?
2. $D_{\mathrm{chg}}$ as a control-oriented proxy: is its construction and physical interpretation defensible?
3. LLM-BO + fast-charging literature: are LLAMBO 2024, LABO 2024, SoberLLMBO 2024, EIMO, and the recent B.-C. Wang group papers (GPA-MOBO) positioned correctly?
4. The representative protocol analysis: are the trade-offs and physical interpretations correct?

### Will particularly care about
The gap between the manuscript's $D_{\mathrm{chg}}$ proxy and a real capacity-fade endpoint, and whether the manuscript's claims about "first LLM-BO for fast charging" are defensible against the B.-C. Wang group's existing EIMO and GPA-MOBO work.

### Possible blind spots
Will not deep-dive the GP/EI math (defer to Reviewer 1).

---

## Overall Assessment

### Recommendation
**Major Revision**

### Confidence Score
5 (Completely within my area of expertise.)

### Summary Assessment
The manuscript is a competent engineering paper on LLM-guided MOBO for battery fast-charging protocol design. The SPMe simulation, the multistage constant-current protocol, the Chen2020 / Ecker2015 parameterization, and the $D_{\mathrm{chg}}$ proxy construction are all defensible. The 5-seed main comparison and the 10-seed prompt study provide reasonable evidence for the LLM-informed initialization component. However, four domain-level concerns require attention: (i) the **novelty claim against the B.-C. Wang group's existing EIMO and GPA-MOBO papers is under-articulated** — both papers cover the same target application (lithium-ion battery fast charging) and the same core technique (decomposition-based MOBO with experience or knowledge priors); the LLM component is genuine but the manuscript does not position the contribution against the group's prior work; (ii) the **$D_{\mathrm{chg}}$ proxy is described as a control-oriented proxy but the manuscript does not reference the canonical Suri & Onori 2016 paper** that defines the severity-factor family; (iii) the **representative protocol analysis (Table III, §V-D) lacks the analytical narrative** that would let a battery engineer see the trade-off (compare EIMO V-B); (iv) the **literature on multistage constant-current protocols** is thin — only ref14 (Jiang 2022) and ref13 (Wang 2023) cite the protocol design; Tahir 2023's review of multi-stage charging strategies should be cited. None of these is fatal; all are repairable.

---

## Strengths

### S1: $D_{\mathrm{chg}}$ is honestly framed as a control-oriented proxy, not a capacity-fade endpoint
**Evidence Anchor**: text: model.tex §III-B "a control-oriented degradation proxy rather than a direct prediction of capacity lost during one charge" + "Because the proxy uses trajectory averages, it does not separately resolve short high-SOC, high-current, or high-temperature excursions. This limitation is retained when interpreting the Pareto protocols."
This is unusual and welcome. Most fast-charging BO papers either ignore the proxy limitation or report a $Q_s$ without acknowledging the gap to a real aging model.

### S2: SPMe-based simulation via PyBaMM is a defensible model choice
**Evidence Anchor**: text: model.tex §III-A "The SPMe retains solid-phase diffusion, electrolyte transport, and interfacial reaction kinetics at substantially lower computational cost than a full porous-electrode model [ref6]. The implementation uses PyBaMM [ref7]."
SPMe is the standard reduced-order model for fast-charging optimization, and PyBaMM is the standard implementation. This is a good choice.

### S3: Honest reporting of the regional-guidance ablation limit
**Evidence Anchor**: text: experiments.tex §V-C "the three-seed experiment does not establish an independent systematic benefit for this component"
The author is honest about the under-powered ablation. This is good scientific practice.

---

## Weaknesses

### W1: Novelty claim against EIMO and GPA-MOBO is under-articulated
**Problem**: The B.-C. Wang group has published (a) **EIMO** (Experience-Informed Multiobjective Optimization for Fast Charging Design of Lithium-Ion Batteries, IEEE TTE, in press) which transfers optimization experience from higher SOH levels to the current SOH level via a transfer acquisition function; and (b) **GPA-MOBO** (Gaussian process-accelerated multiobjective evolutionary design of charging process, IEEE Trans. Ind. Informat. 2024) which is essentially the same ParEGO-style decomposition-based MOBO backbone used in LLMBO-MO. The Introduction does not cite EIMO, and the literature review does not position LLMBO-MO against GPA-MOBO. A reader familiar with the B.-C. Wang group's work would ask: "Is LLMBO-MO just EIMO with the SOH-transfer replaced by an LLM prior?" The answer is yes-but-the-LLM-prior-is-different, and the manuscript should say so.
**Evidence Anchor**: absence: introduction.tex — expected a comparison with EIMO and GPA-MOBO; checked §I absent; absence: references.tex — expected EIMO and GPA-MOBO entries; checked references absent
**Why it matters**: Without the comparison, the novelty claim ("first LLM-guided MOBO for fast charging") is contested by EIMO, which is essentially "first experience-guided MOBO for fast charging". The LLM is a different *source* of prior information, but the manuscript does not make this distinction sharp.
**Suggestion**: Add a paragraph in the Introduction (§I) and a paragraph in the Related Work (if any) explicitly comparing LLMBO-MO with EIMO and GPA-MOBO. State: "EIMO [ref EIMO] transfers *optimization experience* from prior SOH levels, which requires running EIMO at multiple SOH levels; LLMBO-MO instead queries an LLM, which requires only battery-domain text. The two approaches are complementary: EIMO is preferable when historical optimization data are available; LLMBO-MO is preferable when only domain knowledge is available."
**Severity**: Major
**Confidence**: 5 — core expertise: battery optimization literature

### W2: $D_{\mathrm{chg}}$ is not referenced to Suri & Onori 2016
**Problem**: The control-oriented degradation proxy (eq. aging) is a power-law severity-factor model of the form $\chi = (a_s \bar s + b_s) \exp((\beta_I \bar I - E_a) / (R \bar T))$ with $D_{\mathrm{chg}} = \kappa_D Q_{\mathrm{eff}} (\chi / q_a)^{1/\gamma}$. This is the canonical Suri & Onori 2016 severity-factor family. The manuscript cites "the severity-factor family of control-oriented semi-empirical aging models" but does not name the Suri & Onori paper.
**Evidence Anchor**: text: model.tex §III-B "The construction is related to the severity-factor family of control-oriented semi-empirical aging models" + absence: references.tex — expected Suri & Onori 2016 entry; checked references absent
**Why it matters**: Citing Suri & Onori is a hard requirement for any paper using the severity-factor family. Without it, the reviewer cannot verify the construction and the reader cannot trace the parameters.
**Suggestion**: Add the Suri & Onori 2016 reference (Energy 96, 644–653) to references.tex and cite it in §III-B.
**Severity**: Major
**Confidence**: 5 — core expertise: battery aging modeling

### W3: Representative protocol analysis (§V-D) lacks analytical narrative
**Problem**: §V-D introduces Table III (representative Chen2020 LLMBO-MO Pareto protocols) with five protocols A–E and the four time-domain trajectories in Fig. 5. The prose only summarizes the table in two sentences ("The representative protocols exhibit the expected physical trade-offs...") and does not walk the reader through what each protocol means physically.
**Evidence Anchor**: text: experiments.tex §V-D "The representative protocols exhibit the expected physical trade-offs. More aggressive current schedules shorten the charging horizon but generally produce larger temperature excursions and higher degradation-proxy values."
**Why it matters**: The Table III / Fig. 5 combination is the most important *physical* evidence in the paper. Without analytical narrative, a battery engineer cannot extract the design insight. Compare EIMO V-B, which analyzes each of six protocols A–F with a specific physical interpretation.
**Suggestion**: Add 2–3 sentences per representative protocol. For example: "Protocol A ($I_1/I_2/I_3 = 6.000/5.000/3.000$ A, $\Delta s = 0.400/0.300/0.100$) prioritizes $t_c$ at 2880 s by operating the first two stages near the current upper bound, accepting $\Delta T_p = 7.567$ K and $D_{\mathrm{chg}} = 1.261$. The temperature rise is driven by the high current in the first two stages; the degradation-proxy increase is driven by the high $T$ and $I$ at high SOC."
**Severity**: Major
**Confidence**: 5 — core expertise: battery protocol analysis

### W4: Multistage constant-current protocol literature is thin
**Problem**: The multistage constant-current (MCC) protocol has been studied extensively. The manuscript cites ref14 (Jiang 2022) and ref13 (Wang 2023) but misses the standard reference: Tahir et al. 2023 (Journal of Energy Chemistry) which reviews multi-stage charging strategies. The literature on the *number of stages* (M = 3 vs M = 5) is also missing.
**Evidence Anchor**: absence: references.tex — expected Tahir 2023 entry; checked references absent; text: method.tex "Following established BO-based charging formulations, SOC spans rather than stage durations are optimized"
**Why it matters**: Tahir 2023 is the canonical reference for MCC protocol design and the standard citation for any paper using MCC. Without it, the manuscript's MCC parameterization looks ad-hoc.
**Suggestion**: Add Tahir et al. 2023 (Journal of Energy Chemistry) and reference it in §II (Problem Formulation) when introducing the MCC protocol.
**Severity**: Minor
**Confidence**: 5 — core expertise: battery protocol literature

### W5: Cross-battery generality claim ("Ecker2015 second-parameterization check") is under-tested
**Problem**: The Ecker2015 experiment uses the same 5 seeds, the same 56-call budget, and the same algorithm settings as the Chen2020 experiment. The reported advantage is 28.3% at evaluation 30 and 17.8% at evaluation 56 (relative HV improvement over ParEGO). These numbers are large enough to suggest a real effect, but the manuscript does not report the per-seed values or a paired test.
**Evidence Anchor**: text: experiments.tex §V-C "At evaluation 30, the five-seed mean HV is \EckerMidLLMBO\ for LLMBO-MO and \EckerMidParEGO\ for ParEGO... the advantage observed on Chen2020 is also present under the Ecker2015 parameterization, although this experiment is interpreted as an additional battery-model check rather than a formal cross-battery transfer study"
**Why it matters**: The Ecker2015 result is the manuscript's only cross-parameterization evidence. If the 5 seeds are the same as Chen2020, the two are not independent. If they are different, the per-seed dispersion needs to be reported.
**Suggestion**: Report the per-seed Ecker2015 values for both LLMBO-MO and ParEGO at evaluation 30 and 56, and clarify whether the seeds are matched to Chen2020.
**Severity**: Minor
**Confidence**: 4 — core expertise: cross-battery validation

### W6: $D_{\mathrm{chg}}$ proxy units not explicitly bounded
**Problem**: The $D_{\mathrm{chg}}$ proxy returns values in "arbitrary proxy units" (model.tex §III-B). The representative protocol values (Table III) range from 0.573 to 1.261, but the manuscript does not explain what these values mean in terms of cycle life or capacity loss. A reader cannot tell whether $D_{\mathrm{chg}} = 1.0$ corresponds to a 1% capacity loss per cycle or a 10% capacity loss per cycle.
**Evidence Anchor**: text: model.tex "therefore $D_{\mathrm{chg}}$ is reported in arbitrary proxy units rather than as percentage capacity loss" + text: experiments.tex Table III (no unit caption)
**Why it matters**: Without a unit interpretation, the Pareto front in $D_{\mathrm{chg}}$ is uninterpretable to a battery engineer. The author could fix this by reporting the proxy value in a *relative* sense (e.g., the ratio to a CC-CV baseline) or by calibrating against a published aging dataset.
**Suggestion**: Either calibrate $D_{\mathrm{chg}}$ against a published aging dataset (preferred, but expensive) or report it as a relative ratio to a CC-CV baseline with a one-sentence justification.
**Severity**: Major
**Confidence**: 5 — core expertise: aging proxy interpretability

---

## Coverage Receipt
Not applicable (lists populated).

---

## Detailed Comments

### Literature Review / Theoretical Framework
- The literature review (§I) covers BO for fast charging (Shahriari 2016, Attia 2020, Jiang 2022, Wang 2023) and LLM-BO (LLAMBO 2024, LABO 2024, SoberLLMBO 2024). It does not cite EIMO, GPA-MOBO, or the Tahir 2023 MCC review. (See W1, W4.)

### Methodology / Research Design
- The SPMe simulation setup is standard. The Chen2020 (LG INR21700-M50) and Ecker2015 parameterizations are well documented. The $D_{\mathrm{chg}}$ proxy is honestly framed as a control-oriented proxy (S1) but the Suri & Onori reference is missing (W2).

### Results / Findings
- The HV main result is credible. The 10-seed prompt study is the strongest mechanism evidence. The 3-seed ablation is honestly under-powered.
- The representative protocol table (Table III) is well-constructed but under-analyzed (W3).

### Discussion
- The Discussion (§V-E) does not engage with the *physical* interpretation of the representative protocols. Compare EIMO V-B.
- The Discussion also does not address the cross-battery generality question (W5).

### Conclusion
- The Conclusion is a summary, not a limitations + scope section. See the EIC report (W3) for the same concern.

### References
- See W1 (EIMO, GPA-MOBO), W2 (Suri & Onori), W4 (Tahir 2023). Also: ref7 (PyBaMM) should cite the Sulzer 2021 PyBaMM paper or its equivalent.
- The reference list is small (28 entries); for an IEEE TTE paper, a 35–40 entry list would be more typical.

---

## Criterion-Bound Judgements

| Dimension | Criterion source | Judgement | Evidence anchor(s) | Rationale | Decision bearing? |
|---|---|---|---|---|---|
| Originality | §1 universal | PARTLY_MEETS | absence: §I (no EIMO / GPA-MOBO comparison) | The LLM-informed initialization is novel; the bounded-restart design is novel; but the comparison with EIMO and GPA-MOBO is missing. W1 is real. | Yes |
| Methodological Rigor | §1 universal | MEETS | text: §III (model), §V (experiments) | The model and experiment design are standard. | No |
| Evidence Sufficiency | §1 universal | PARTLY_MEETS | absence: references (Suri & Onori); absence: §V-D analytical narrative | The proxy is not anchored to its canonical source (W2) and the representative protocol analysis is thin (W3). | Yes |
| Argument Coherence | §1 universal | PARTLY_MEETS | text: §I, §IV, §V | The LLM-guidance narrative is correct but the relationship to EIMO is underexplored. | No |
| Writing Quality | §1 universal | MEETS | text: §III, §V | The technical prose is clear and the figure captions are informative. | No |
| Literature Integration | §1 universal | DOES_NOT_MEET | absence: references.tex (EIMO, GPA-MOBO, Suri & Onori, Tahir 2023) | Four canonical references are missing. | Yes |
| Significance & Impact | §1 universal | MEETS | text: §V (results) | If the EIMO comparison is added, the impact is real. | No |

**Decision-bearing explanation**: Three criteria are unresolved: Originality (PARTLY_MEETS), Evidence Sufficiency (PARTLY_MEETS), Literature Integration (DOES_NOT_MEET). All are repairable. The recommendation is Major Revision, not Reject.

---

## Questions for Authors

1. The B.-C. Wang group has published EIMO (IEEE TTE) and GPA-MOBO (IEEE Trans. Ind. Informat. 2024) which cover the same application. Can the author articulate the precise relationship between LLMBO-MO, EIMO, and GPA-MOBO, and justify the publication of LLMBO-MO as a *new* contribution rather than an incremental extension of EIMO?
2. The control-oriented degradation proxy is the canonical Suri & Onori 2016 severity-factor family. Can the author add the Suri & Onori reference and trace the proxy construction back to it?
3. The representative protocol table (Table III) is well-constructed but under-analyzed. Can the author add 2–3 sentences of physical interpretation per protocol?
4. The Ecker2015 experiment uses 5 seeds. Are these the same 5 seeds as Chen2020, or independent? If same, the two experiments are not independent.
5. The $D_{\mathrm{chg}}$ proxy returns values in "arbitrary proxy units". Can the author either calibrate against a published aging dataset or report the values as a relative ratio to a CC-CV baseline?

---

## Minor Issues

- method.tex line 45: "$\phi_{\mathrm{cell}}$ maps protocol coordinate $I_k$ to physical cell current" — clarify the unit conversion factor.
- experiments.tex Table I: the cell voltage range is reported as "2.50–4.20 V"; consider including the upper cutoff current (5 A or 6 A).
- references.tex: ref6 (SPMe paper) is missing; the standard SPMe reference is Moura et al. 2016 (IEEE Trans. Control Syst. Technol.).
- figures/fig_charging_design_problem.tex: the figure caption could include the protocol parameter ranges.
