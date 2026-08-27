# Peer Review Report — Perspective Reviewer

## Manuscript Information
- **Title**: Battery Fast-Charging Protocol Design via Large Language Model-Guided Multiobjective Bayesian Optimization
- **Review Date**: 2026-08-27
- **Review Round**: Round 1

## Reviewer Information
### Reviewer Role: Peer Reviewer 3 (Perspective / Cross-disciplinary)
### Reviewer Identity: AutoML & LLM-for-Science researcher
### Review Focus: LLM-guided optimization cross-domain transferability, alternative interpretations, "why LLM not rules"

## Overall Assessment
### Recommendation: Major Revision
### Confidence Score: 4
### Summary Assessment: The paper proposes LLMBO-MO, which augments a ParEGO-style MOBO backbone with two LLM touchpoints (LLM-informed initialization and weight-conditioned regional guidance) for 56-evaluation, 3-objective battery-charging design. The methodological hygiene is strong: the LLM never injects unevaluated objective values, every protocol is simulator-validated, and the two mechanisms are designed to befall back to a purely numerical search. The five-seed Chen2020 / Ecker2015 evidence is internally consistent, and the discussion is unusually honest about ablation seed counts and the lack of cross-LLM robustness. However, the paper's central LLM-integration claim — that an LLM is doing non-trivial work beyond a hand-coded rule base — is undersupported. There is no comparator against (a) expert-rule initialization using the same qualitative knowledge, (b) random + Sobol/LHS initialization with the same prompt budget, or (c) a no-LLM strong baseline. The LLAMBO / LABO / SoberLLMBO positioning is hand-waved in a single paragraph, and the SoberLLMBO result that LLM guidance can be net-negative outside its training distribution is not engaged. The regional-guidance component shows no independent benefit on three seeds and is essentially admitted as a "secondary refinement." I therefore recommend Major Revision: the paper needs a controlled "rules vs. LLM" ablation, a LLM-backend / prompt robustness study, and a sharper positioning against LLAMBO-style warm-starting before the central thesis is convincing.

## Strengths *(only genuine ones)

### S1: Clean separation of LLM advisory role from numerical evaluation pipeline
- **Evidence Anchor**: text: §IV (method) and §IV.A "no unevaluated LLM proposal is used as a surrogate target or Pareto value"
- The LLM only proposes *locations*; the simulator, GP, and EI loop retain full authority over objective values, feasibility, and Pareto updates. This is the right architectural pattern for LLM-BO and the paper states it clearly.

### S2: Protocol-domain screening as a defensive layer for LLM unreliability
- **Evidence Anchor**: text: §IV.C — "Non-numerical or non-finite entries and duplicates are removed, box violations are clipped, and candidates that cannot satisfy $\Delta s_K\geq\Delta s_K^{\min}$ are rejected"
- The paper anticipates LLM hallucination / format failure and constrains it to box-bounded, monotonic, SOC-feasible proposals. This is more careful than many LLM-BO papers that trust the LLM as an oracle over the decision space.

### S3: Genuinely self-critical limitations section
- **Evidence Anchor**: text: §V.E — "the regional-guidance ablation contains only three matched seeds, so its independent contribution is less firmly established" and "a controlled comparison across LLM backends and prompt realizations is outside the present study"
- The discussion transparently admits (a) the three-seed ablation is underpowered, (b) no qEHVI / qNEHVI baselines, and (c) no cross-LLM study. This is rare and commendable; it should be amplified as a roadmap rather than a footnote.

### S4: The "battery-specific vs. generic prompt" prompt-control study
- **Evidence Anchor**: text: §V.C.1, Table III — 0.31062 (random) vs 0.31371 (detailed generic) vs 0.36890 (battery-specific)
- This is the most informative mechanism-level evidence in the paper. The near-equality of random and generic-prompt HVs, contrasted with the battery-specific gain, is a strong argument that *what the LLM is told about batteries* — not the act of asking an LLM — drives the improvement.

## Weaknesses *(with evidence anchor + severity + confidence)*

### W1: No "rules vs. LLM" ablation — the central thesis is unsupported
- **Problem**: The paper claims LLM guidance is useful, but never compares LLM initialization to a hand-coded rule base encoding the *same* qualitative battery knowledge (multi-stage current ordering, SOC allocation heuristics, monotonicity, soft terminal-span penalty). Since the LLM "prompt specifies ... qualitative charging knowledge such as reasonable current ordering and SOC allocation" (method.tex §IV.C), that knowledge is *already formalized* — the LLM is at best a stochastic encoder of an explicit rule list. The paper never rules out the cheaper alternative.
- **Evidence Anchor**: `text: §V.C.1 — initialization source "Random", "Detailed generic prompt", "Battery-specific LLM prompt"; absence: §V — no expert-rule or hand-coded multi-stage template baseline; checked §V.E limitations`
- **Why it matters**: Without this comparison, the contribution reduces to "using a 1B-class LLM to encode a rule list you could write in 30 lines of Python." For TTE readers, the practical message is unclear: should they install an LLM API key, or write a domain template?
- **Suggestion**: Add a fourth row to Table III (and the corresponding mechanism ablation) that uses a battery-domain hand-coded multi-stage template (e.g., a CC-then-tapered-CC schedule generator with a few physics-motivated parameter ranges) as initialization, evaluated on the same matched seeds and budget. If the LLM does not beat it, the contribution framing must shift.
- **Severity**: Critical
- **Confidence**: 5 — Without this comparison, the "LLMBO-MO" label is doing work the mechanism does not earn.

### W2: LLAMBO / LABO / SoberLLMBO positioning is a single paragraph and does not establish novelty boundary
- **Problem**: The introduction cites LLAMBO (ref10), SoberLLMBO (refSoberLLMBO), LABO (refLABO), and a 2026 preference-guided LLM-BO (ref16), then asserts "two aspects remain insufficiently explored" — warm-starting with diversity-aware screening and weight-conditioned regional guidance. But LLAMBO already does LLM warm-starting; LABO does selective experimentation; ref16 does preference-guided search. The paper does not articulate what is mechanically new in LLMBO-MO that these works do not provide, and does not cite SoberLLMBO's sobering finding that LLM-BO can hurt on out-of-distribution tasks. As written, a reader familiar with the LLM-BO literature cannot tell whether LLMBO-MO is (a) a domain specialization, (b) a multiobjective extension, or (c) a substantive methodological advance.
- **Evidence Anchor**: `text: §I — "LLAMBO introduced LLM-assisted warm starts, candidate generation, and surrogate-related reasoning for BO" / "Subsequent studies have considered point or region preferences and selective use of inexpensive LLM predictions" — no head-to-head or feature-matrix comparison`
- **Why it matters**: LLM-BO is an active 2024–2026 subfield. Without a crisp "here is what we add that LLAMBO/LABO/SoberLLMBO do not," the paper reads as an application, not a contribution.
- **Suggestion**: Add a short comparison table (or paragraph block) that maps LLMBO-MO features against LLAMBO, LABO, SoberLLMBO, and ref16 along axes: warm-start diversity screening, MO support, weight-conditioned regions, domain-knowledge injection, simulator-validated pipeline. The multiobjective dimension (decomposition-conditioned regional guidance) is a plausible genuine contribution; the writing must say so explicitly and show why LLAMBO's single-objective warm-start does not trivially extend.
- **Severity**: Major
- **Confidence**: 4 — Strong LLAMBO/LABO coverage likely already exists in the LLM-BO literature; the paper should at minimum cite Liu et al. 2024 and Chen et al. 2026 as direct feature comparators.

### W3: Three-seed ablation is statistically inadequate for the regional-guidance claim
- **Problem**: The "Bounded Regional Guidance" mechanism is the second of two contributions, but its independent contribution is tested on three seeds (8409–8411) and shows "modest" mean change. The paper states this honestly but still claims "regional guidance supplies a local, weight-conditioned search bias during the early acquisition stage" and that the combined variant has the "highest observed mean HV." Three seeds cannot distinguish a 0.01 HV signal from seed noise; the bolded "+ Regional guidance only" row in Table IV carries no inferential weight.
- **Evidence Anchor**: `text: §V.C.2 — "three matched seeds (8409--8411), six initialization evaluations, and ten sequential BO evaluations"; "the three-seed experiment does not establish an independent systematic benefit for this component"`
- **Why it matters**: The paper bills regional guidance as a peer to LLM-informed initialization, but the evidence supports it as at best an auxiliary refinement. A reviewer must ask whether the second mechanism is worth the LLM-call cost and engineering complexity. With three seeds the answer is unknown.
- **Suggestion**: Either (a) expand the ablation to ≥10 seeds and report paired-test statistics (Wilcoxon / sign test) across the four variants, or (b) reframe regional guidance as an optional add-on, move the LLM-informed initialization story to the foreground, and drop "two mechanisms" from the contribution list. Don't claim parity on three seeds.
- **Severity**: Major
- **Confidence**: 5 — Three seeds for an ablation that carries a paper-level claim is methodologically insufficient.

### W4: No LLM-backend / prompt-robustness study despite acknowledging the gap
- **Problem**: Table II specifies the LLM as "V4-Flash" (a specific commercial model), and §V.E explicitly admits "a controlled comparison across LLM backends and prompt realizations is outside the present study." But the entire gain is attributed to LLM guidance; without showing that the gain survives at least one more LLM and at least one prompt paraphrase, the result is conditioned on a single point in LLM-space. SoberLLMBO (cited) showed exactly this fragility. The discussion must engage with that risk.
- **Evidence Anchor**: `text: Table II — "Engine used for chat-based tasks: V4-Flash"; §V.E — "a controlled comparison across LLM backends and prompt realizations is outside the present study"`
- **Why it matters**: If the gain is a V4-Flash artifact (e.g., this particular model happens to encode the right chemistry priors), the method does not generalize across the very LLM landscape practitioners will use. The paper cannot claim "LLM-guided" while testing one model.
- **Suggestion**: Add a small cross-LLM study (e.g., V4-Flash + one open-weight 7B–13B model) on the same matched seeds and the §V.C.1 26-evaluation budget, even if only for the initialization mechanism. Discuss SoberLLMBO's out-of-distribution finding directly.
- **Severity**: Major
- **Confidence**: 4 — Single-LLM evaluation in a 2026 LLM-BO paper is increasingly a hard ask.

### W5: LLM hallucination / format-failure handling is asserted, not measured
- **Problem**: The paper claims protocol-domain screening ("non-numerical or non-finite entries ... box violations clipped ... SOC span rejected") catches invalid LLM proposals. But there is no measurement of *how often* the LLM produces an invalid proposal, what fraction of the candidate pool survives screening, or what happens when the LLM is asked a question it cannot answer (the regional-guidance "no-preference response" path). The LLM is presented as a black box that the screening layer handles; for a paper whose entire delta is "ask an LLM," the failure-mode statistics are essential.
- **Evidence Anchor**: `text: §IV.C — screening rules; absence: §V — no LLM-call success rate, no proposal-rejection-rate table, no example of failed LLM response handling`
- **Why it matters**: If 80% of LLM proposals are rejected, the mechanism is more like "an expensive way to occasionally get one good initialization point." If 5% are rejected, the screening is mostly defensive. The paper does not say.
- **Suggestion**: Add a paragraph or table: total LLM queries, number returning valid points, number returning regions, number returning "no preference," number rejected by screening. The numbers belong in the main text, not an appendix.
- **Severity**: Major
- **Confidence**: 4 — Engineering readers will ask this on first read.

### W6: Cross-domain transferability is not discussed despite being the headline framing
- **Problem**: The paper presents LLMBO-MO as an LLM-BO method, not a battery-only method, but the only demonstration is two battery parameterizations. The introduction argues that LLM-BO is attractive because qualitative knowledge is available in many domains, yet the "battery-specific vs. generic prompt" study explicitly shows that generic prompting is *worse* than random — implying the method is *battery-LLM-coupled*, not general. This contradiction is unaddressed.
- **Evidence Anchor**: `text: §V.C.1 Table III — generic prompt 0.31371 ≈ random 0.31062 ≪ battery-specific 0.36890; absence: §I–§VI — no discussion of why the method would or would not transfer to, e.g., alloy design, drug discovery, or hyperparameter tuning`
- **Why it matters**: If the method is "LLM-BO for batteries," the cross-disciplinary contribution is application, not method. The title and abstract position it as method; the evidence supports application. This is a framing problem.
- **Suggestion**: Either (a) reframe the contribution as "battery-LLM-coupled MOBO," or (b) include at least one non-battery LLM-BO benchmark (e.g., a standard function or molecular dataset where an LLM has known prior knowledge) to substantiate the "transferable" framing.
- **Severity**: Major
- **Confidence**: 3 — Reframing is a writing change, not a new experiment, but it materially affects how readers interpret the contribution.

### W7: The "weight-conditioned regional guidance" mechanism's design choices are not motivated
- **Problem**: The regional-guidance prompt includes the current decomposition weight, observed ranges, current best values, and selected protocols, and returns either a point, a region, or "no preference." Several design choices are unexplained: why a hyperrectangle and not an ellipsoid or a Gaussian bump; why a fixed-width margin for point-to-region conversion; why the early-search window $T_{\mathrm L}$ exists at all. A reviewer familiar with LLM-BO cannot tell whether these choices were made because they worked, or because they were the first thing tried.
- **Evidence Anchor**: `text: §IV.D — "A point is converted to a local region with fixed-width margins"; absence: §IV.D — no motivation of the hyperrectangle shape, the margin width, or the early-window heuristic`
- **Why it matters**: Method sections should justify non-obvious design choices. The current text reads as design summary, not design rationale.
- **Suggestion**: Add a 2–3 sentence design rationale subsection, or fold the rationale into the regional-guidance introduction. If shape/margin/window were tuned, say so; if they were fixed a priori, justify.
- **Severity**: Minor
- **Confidence**: 3

### W8: Practical impact for the IEEE TTE reader is underspecified
- **Problem**: The IEEE TTE audience is transportation-electrification engineers. The paper's practical value proposition is: "if you have a battery simulator, LLMBO-MO finds a better Pareto front in 56 evaluations than ParEGO." But the paper does not say: (a) how a practitioner plugs their own simulator in, (b) what compute cost the LLM calls add (token cost, latency), (c) whether the LLM is local or API, (d) how often the LLM must be re-queried as the prompt or model changes. TTE is an applied journal; the engineering "how do I use this" answer is missing.
- **Evidence Anchor**: `text: §V.A — Table II lists V4-Flash but no LLM-call budget, token count, or wall-clock cost; §V.E — mentions Appendix reproducibility but does not quantify LLM operational cost`
- **Why it matters**: Engineering reproducibility is more than seed lists; it is API cost, latency, and integration effort.
- **Suggestion**: Add a short "practical deployment" paragraph: total LLM calls per run, approximate tokens per call, approximate wall-clock overhead, and one sentence on the API surface a practitioner would need to swap in their own simulator.
- **Severity**: Minor
- **Confidence**: 4

### W9: The HV improvement number is reported but the absolute HV is not contextualized
- **Problem**: The paper reports a \ChenFinalGain% improvement in mean final HV over ParEGO, but the reader is not given the *absolute* HV value or the reference-point definition. Without knowing whether the absolute HV is, say, 0.05 or 0.85, the percentage is uninformative. A 20% improvement on a small absolute HV is not the same as a 20% improvement on a saturated HV.
- **Evidence Anchor**: `text: §V.B — "\ChenFinalGain\ relative improvement in mean final HV"; absence: §V.B — no reporting of the absolute HV values, the reference point, or the objective-space volume that defines 100%`
- **Why it matters**: HV is a relative metric by construction; reporting percentage improvements without the absolute values and reference-point geometry is a known weakness that sharp reviewers will flag.
- **Suggestion**: Add the absolute HV means for all methods and the reference point to Table III, and a one-line note on the reference-point geometry.
- **Severity**: Minor
- **Confidence**: 5 — This is a reporting standard issue, not a research-quality issue.

## Detailed Comments

### Introduction
- The LLM-BO literature coverage is *thin* for a 2026 submission. LLAMBO is cited but the feature-by-feature comparison is absent. SoberLLMBO is cited and ignored — a SoberLLMBO-aware reader will ask why the paper does not test its sobering message. LABO and ref16 are listed as "subsequent studies" without explanation of what they do.
- The boundary between this work and the cited LLM-BO family is asserted, not argued. The phrase "two aspects remain insufficiently explored" is the right rhetorical move, but the supporting text is one sentence per aspect, which is not enough for a contribution claim.
- The connection between the "qualitative charging knowledge" problem framing and the "LLM translates text to numbers" solution is well articulated; this is the paper's strongest narrative beat.
- **Writing quality**: Tighter than the experiments section, but the LLM-BO coverage needs a feature-comparison table or a 200-word positioning paragraph.

### Method
- The ParEGO backbone is standard and well-described. The Das–Dennis + Riesz-energy weight initialization is a nice touch; the augmented Tchebycheff with range-of-history guard is a sensible modification.
- The LLM-Informed Initialization (§IV.C) is the most carefully designed part: the soft penalty, the diversity term, the bounded candidate pool, and the "no unevaluated LLM proposal" guarantee are all correct.
- The Bounded Regional Guidance (§IV.D) is *under-motivated*. Why a hyperrectangle, why a fixed margin, why an early window? The mechanism is presented as a design; a reader cannot tell whether it is a design that was tested and won, or one that was tried and reported.
- **Cross-domain transferability**: The method is presented as domain-agnostic, but the prompt text is battery-specific and the §V.C.1 evidence shows the gain is *battery-specific*. The method, as described, is a battery-LLM-coupled MOBO. The paper should say so.

### Experiments
- The 5-seed main comparison is appropriate; the §V.C.1 10-seed initialization study is solid; the §V.C.2 3-seed ablation is under-powered for the claim it carries.
- The absence of (a) LLM-backend comparison, (b) prompt-paraphrase study, (c) qEHVI/qNEHVI baseline, (d) expert-rule initialization, is acknowledged in §V.E but materially weakens the "LLM-guided" claim. The current evidence shows "V4-Flash with this specific prompt helps on these two battery models on these seeds." That is not yet a general claim.
- The Pareto-front analysis (§V.D) is well done and gives the paper a nice qualitative anchor: the protocols make physical sense (high current = fast but hot; low current = slow but cool), which is the strongest defense of the simulator-in-the-loop design.

## Criterion-Bound Judgements

| Dimension | Judgement | Evidence anchor | Rationale | Decision bearing? |
|---|---|---|---|---|
| Originality | PARTLY_MEETS | §I LLM-BO positioning; absence of LLAMBO/LABO feature table | The decomposition-conditioned regional guidance is plausibly novel; warm-starting with diversity screening is incremental on LLAMBO | Yes |
| Methodological Rigor | PARTLY_MEETS | §V.C.2 3-seed ablation; §V.E acknowledged gaps; W3, W4 | The architecture is correct; the experimental design is incomplete for the claims made | Yes |
| Evidence Sufficiency | DOES_NOT_MEET | §V.B–§V.D — single LLM, 3-seed ablation, no rules baseline, no cross-domain test | The evidence supports "one LLM on two batteries helps vs. ParEGO," which is weaker than the abstract claim | Yes |
| Argument Coherence | PARTLY_MEETS | §I "two unexplored aspects" vs §V.C.1 battery-specific coupling; W6 | The framing drifts: "general LLM-BO" in the intro, "battery-LLM-coupled" in the data | Yes |
| Writing Quality | MEETS | §I–§IV generally clear; §V.E unusually honest | Above the bar for TTE; the self-critical limitations section is a model | No |
| Literature Integration | DOES_NOT_MEET | §I — LLAMBO/LABO/SoberLLMBO cited but not compared; W2 | SoberLLMBO's central finding is not engaged; the LLM-BO feature space is not mapped | Yes |
| Significance & Impact | PARTLY_MEETS | §V.D Pareto-protocol analysis; §V.E roadmap | Useful as a battery-charging design study; the LLM-BO methodological contribution is not yet established | No |

## Questions for Authors
1. In §V.C.1, the "battery-specific LLM prompt" is presented as the LLM advantage. Could the authors run a fourth condition where the same qualitative knowledge is encoded as a hand-coded multi-stage template generator (e.g., CC-then-tapered-CC with parameter ranges) and used for initialization? If the hand-coded template matches the LLM, the LLM is not earning its keep; if it beats the LLM, the contribution framing must change.
2. The LLM in Table II is "V4-Flash." Have the authors tested at least one open-weight LLM (e.g., a 7B–13B parameter model) on the §V.C.1 study, even at smaller scale? SoberLLMBO's out-of-distribution finding makes this a non-optional robustness check.
3. For the regional-guidance mechanism, why a hyperrectangle and not an ellipsoid? Why a fixed-width margin? Why an early window? Were these choices tuned, fixed a priori, or first-thing-tried?
4. Could the authors report the fraction of LLM proposals that survive protocol-domain screening, and the fraction of regional-guidance queries that return "no preference"? The mechanism's cost-benefit depends on these numbers.
5. The §V.C.1 10-seed initialization study uses a 26-evaluation budget, while the main comparison uses 56. At the main-study budget, is the initialization effect still dominant, or does the LLM warm-start's advantage erode as the numerical GP–EI loop accumulates data? A 56-budget replication of the §V.C.1 design would close the loop.
6. The paper argues "qualitative charging knowledge" is a gap that LLMs fill. Is that knowledge available only as text, or is it also available as a small structured dataset (e.g., 50–100 prior charging protocols with outcomes)? If the latter, a BO warm-start on prior data — without an LLM — is a natural baseline that is missing.

## Minor Issues
- §I: "broad Gaussian and uniform candidates" (method.tex §IV.B) — what are the uniform candidates' role relative to L-BFGS-B? A one-line clarification would help.
- §V.B: The abstract reports the relative HV improvement as \ChenFinalGain% but the absolute HV value and the reference-point definition are not given anywhere in the main text.
- §V.C.2: The ablation table reports individual seed values and means, but no paired-test statistic. A Wilcoxon signed-rank across the four variants would resolve the "modest" claim.
- Table II: "Percentage of top candidates to select: 0.2" — of how many? With 2 templates generating 15 candidates, 0.2 × 15 = 3. Clarify whether "templates" mean prompt templates and how they map to candidates.
- §V.D: The representative protocol table is informative, but the "dominates" relation between the five protocols and the comparison methods' Pareto fronts is not given. A reader cannot tell whether protocol A is on LLMBO-MO's front only, or also on ParEGO's.
- §V.E: The "broader MOBO baselines, cross-LLM studies, and physical-cell validation are left for future work" sentence is good but should be promoted to a "Limitations and Future Work" subsection in the Conclusion, not buried in the Discussion.
- References: ref16 and refLABO cite arXiv preprints dated 2026 with what appear to be future-style identifiers (arXiv:2605.*); these should be confirmed as published or preprinted. The reference list also cites two of the authors' own prior constrained-MO works (refPengTemporal, refPengDynamic) that are not used in the text — confirm these are intentional and not auto-injected.
- Notation: the paper uses both $\bw$ and $\boldsymbol{\theta}$ for vectors but the inline math in §IV.C occasionally drops bolding; a final copyedit pass is warranted.
