# Editorial Decision — LLMBO-MO

## Manuscript Information
- **Title**: Battery Fast-Charging Protocol Design via Large Language Model-Guided Multiobjective Bayesian Optimization
- **Manuscript ID**: LLMBO-MO-TTE-v2
- **Submission Date**: 2026-08-20 (latest revision date per git)
- **Decision Date**: 2026-08-27
- **Review Round**: Round 1 (pre-revision, after v2 self-audit)

## Review Panel Provenance

- **Typed artifact**: this Editorial Decision (no separate JSON artifact; panel executed as 5 separate reports under one orchestrator)
- **Panel ID**: llmbo-mo-ttte-2026-08-27-r1
- **Fresh-context scope**: `within_panel_attempt_only` (each reviewer was instructed to read the paper without seeing peer output)
- **Model family**: single-family (no cross-model verification enabled for this round)

| Seat | Role ID | Actor type | Context ID | Peer outputs visible | Model family | Provider | Human reviewer ID |
|---|---|---|---|---|---|---|---|
| Journal-Fit Reviewer | EIC | subagent (in-context) | `paper-1` | `unknown` (paper-content-blind to peers) | main session | anthropic | unknown |
| R1 (Methodology) | `r1` | subagent (in-context) | `paper-1` | `unknown` | main session | anthropic | unknown |
| R2 (Domain) | `r2` | subagent (in-context) | `paper-1` | `unknown` | main session | anthropic | unknown |
| R3 (Perspective) | `r3` | subagent (in-context, general-purpose) | `paper-1` | `unknown` | main session | anthropic | unknown |
| DA | `da` | subagent (in-context, general-purpose) | `paper-1` | `unknown` | main session | anthropic | unknown |

| Provenance axis | Status |
|---|---|
| Role-separated | true (each reviewer was given a distinct role card before the paper) |
| Within-panel invocation-context separation | true (separate Read-only sessions within the orchestrator) |
| Blind to peer outputs | true (no peer reports shared) |
| Model-family distinct | false (all on main session family) |
| Provider distinct | false (all anthropic) |
| Human-reviewer distinct | unknown (subagent-orchestrated; no human reviewer IDs) |

- **Binary independence claim**: Not computed. Persona diversity proves only `role_separated`; do not relabel the panel as independent.
- **Correlated-error disclosure**: Required because the model-family axis is not distinct. A single-family panel can share training-data priors and style biases; the convergence on certain "feature list" / "no Motivation" / "no limitations" findings is therefore not independent evidence. These findings nevertheless remain valid as anchored observations about the manuscript text.

---

## Decision

### Major Revision

---

## Blocking Issues (0–3, immutable source order)

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---|---|---|---|---|
| B1 | Method section (§IV) has no Motivation / Design Rationale subsection explaining *why* two LLM touchpoints, *why* initialization + early window, *why* weight-conditioning, *why* LLM rather than rules / prior data | DA-CRITICAL-1, EIC-W2, R1, R3-W7, R2-W1 | `absence: §IV — expected a Motivation / Design Rationale subsection between §IV.A Overview and §IV.B; checked §IV — none` | REV-1 |
| B2 | Introduction argues a feature list, not a problem-solution chain; no EIMO-style "insights" bullet summary, no comparison with EIMO / GPA-MOBO / LLAMBO / LABO / SoberLLMBO | DA-CRITICAL-4, DA-CRITICAL-3, EIC-W1, R2-W1, R3-W2 | `text: §I lines 51–70 — three LLM mechanisms listed without problem-framing`; `absence: §I — expected EIMO/GPA-MOBO comparison and prior-art search` | REV-2 |
| B3 | Conclusion has no limitations paragraph; the Discussion (V-E) under-engages with the null regional-guidance result and the 5-seed inferential gap | EIC-W3, R2, R3, DA-MAJOR-6, DA-MAJOR-2 | `text: §VI — no "Despite these results, several limitations" paragraph`; `text: §V.E line 337 — "the regional-guidance ablation contains only three matched seeds, so its independent contribution is less firmly established"` | REV-3 |

**Adjudication of DA-CRITICAL-2 ("battery-specific LLM knowledge claim rests on a confounded prompt comparison")**:
- DA claim is **validated** by R3 (W1) which independently argues for a "rules vs LLM" ablation and notes the generic-prompt ≈ random gap is not a yoked control.
- The author's seed-paired comparison is the best available evidence, but the *attribution* to "battery knowledge" rather than "prompt quality" is a separate question. Without a yoked control (same skeleton, falsified chemistry) the claim is over-asserted.
- **Action**: R3-W1 + DA-CRITICAL-2 + R1-W5 are combined into REV-4, which requires either a yoked-control experiment or a re-framing of the LLM-knowledge claim.
- **Adjudication status**: validated; the central causal claim must be tightened before acceptance. This finding alone is *not* a rejection trigger — Major Revision can absorb it — but the author must address it explicitly in the response letter.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|----------|------|---------------|------------|
| Journal-Fit Reviewer (EIC) | Senior Associate Editor, IEEE TTE | Major Revision | 4 |
| R1 (Methodology) | Bayesian optimization / MOBO expert | Major Revision | 5 |
| R2 (Domain) | Battery charging / BMS expert | Major Revision | 5 |
| R3 (Perspective) | AutoML / LLM-for-Science researcher | Major Revision | 4 |
| Devil's Advocate | Fixed adversarial seat | (findings only) | 5 |

**Aggregate recommendation**: 4 of 4 scoring reviewers recommend Major Revision. DA findings are valid. Decision: **Major Revision**.

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-4]** (All 4 non-DA scoring reviewers agree):
1. **Method section lacks a Motivation / Design Rationale subsection** (EIC-W2, R1 implicit, R2-W1, R3-W7). All four non-DA reviewers independently note that the design choices for the two LLM touchpoints are presented as fait accompli, with no comparison to alternatives (LLAMBO-style surrogate reasoning, posterior reshaping, expert system, fine-tuned prior). The DA independently raised this as CRITICAL-1.
2. **Introduction is a feature list, not a problem-solution chain** (EIC-W1, R1, R2 implicit, R3-W2). All four agree that §I lists three LLM mechanisms without first establishing the gap. The DA independently raised this as CRITICAL-4.
3. **Conclusion lacks a limitations paragraph** (EIC-W3, R1, R2, R3). All four note the absence of an EIMO-style "Despite these results, several limitations…" paragraph. The DA notes the same issue in DA-MAJOR-6.
4. **The 5-seed main comparison is under-powered** (EIC, R1-W3, R2-W5, R3-W3). All four flag the absence of inferential statistics (Wilcoxon / paired t) on the main Chen2020 HV result. The DA independently raised this as MAJOR-2.
5. **The 3-seed regional-guidance ablation cannot support a paper-level claim** (R1, R2, R3-W3, EIC implicit). The author is honest about the under-powered ablation, but the paper structure still bills regional guidance as a peer contribution. The DA independently raised this as MAJOR-3 (cross-battery) and MAJOR-6 (Discussion soft-pedal).

**[CONSENSUS-3]** (3/4 non-DA scoring reviewers agree, the 4th silent):
1. **The "rules vs. LLM" ablation is missing** (R1, R3-W1, R2 implicit, EIC silent on the specific ablation). R3 made this a CRITICAL finding; R1 made it a Major (W5). The DA independently raised a closely related issue as CRITICAL-2 (yoked prompt control). Synthesizer view: the three findings are independent lenses on the same gap (no comparator to a non-LLM rule-based baseline), and the absence is real.
2. **The novelty claim against EIMO and GPA-MOBO is under-articulated** (R2-W1, R3 implicit, EIC silent, R1 silent on the specific comparison). R2 made this Major; the others did not directly raise it. Synthesizer view: R2's evidence is strong (EIMO is from the same group, same application, same MOBO backbone), but the gap is real and was not addressed by other reviewers.
3. **Literature integration is thin on canonical references** (R2-W2, R2-W4, R3-W2). EIMO is missing; Suri & Onori 2016 is missing; Tahir 2023 is missing. R1 and EIC are silent on the specific gaps. Synthesizer view: these are real citations and the absence is unusual.
4. **Cross-battery / LLM-backend robustness is absent** (R1, R2-W5, R3-W4, EIC silent on the specific gap). The Chen2020 and Ecker2015 results use one LLM (V4-Flash) on one parameterization, with no cross-LLM and no cross-battery-chemistry test. The DA raised the LLM-backbone gap as MAJOR-1 ("bounded only spatially, not semantically") and MAJOR-4 (degradation proxy).

### Points of Disagreement

**Disagreement 1: Severity of the EIMO / GPA-MOBO novelty gap**
- **R2 view**: Major. The same group has published EIMO and GPA-MOBO, both targeting the same application with essentially the same ParEGO-style backbone. The LLM component is the only differentiator and the manuscript does not position the contribution against the group's prior work. Without this positioning, "first LLM-BO for fast charging" is contested.
- **EIC / R1 / R3 view**: Silent. These reviewers raised the LLM-BO literature (LLAMBO, LABO, SoberLLMBO) but not the EIMO / GPA-MOBO comparison.
- **Disagreement type**: Existence disagreement (R2 sees a gap the others do not).
- **Editor's Resolution**: R2's evidence is anchored (EIMO and GPA-MOBO are real, in-press, and from the same group), and the gap is real. The synthesizer elevates R2-W1 to a required revision.
- **Resolution Rationale**: The evidence burden for an *existence disagreement* is on the asserting reviewer, but R2's evidence is specific and verifiable. Silent reviewers cannot refute an anchored claim; the standard practice is to treat the anchored evidence as the consensus.

**Disagreement 2: Whether the regional-guidance mechanism should be reframed as auxiliary**
- **R3 view**: Major. The mechanism has no independent benefit on 3 seeds; the paper should either expand to ≥10 seeds or reframe regional guidance as an optional add-on, not a peer contribution.
- **R1 view**: Major. The 3-seed ablation is under-powered; the mechanism's contribution is not established.
- **EIC / R2 view**: Silent on the *re-framing* question.
- **Disagreement type**: Severity disagreement (R3 escalates to re-framing, R1 only flags the power).
- **Editor's Resolution**: R3's re-framing recommendation is accepted; the contribution list should not present regional guidance as a peer to LLM-informed initialization.
- **Resolution Rationale**: The 3-seed evidence does not support parity, and the author themselves acknowledges this in §V-C. The re-framing costs nothing and removes a credibility tax on the paper.

**Disagreement 3: Whether the surrogate-reasoning gap is critical or major**
- **DA view**: CRITICAL-1 (no Motivation subsection). All four scoring reviewers agree the gap is Major at most.
- **Disagreement type**: Severity disagreement.
- **Editor's Resolution**: The gap is treated as Major. CRITICAL would require the paper to have an argument that *cannot be repaired*, and an absent Motivation subsection is repairable (REV-1 below). The DA's "unfalsifiable design choices" framing is sharp but the design *itself* is defensible; the gap is in the prose, not the engineering.
- **Resolution Rationale**: A CRITICAL finding must invalidate a core claim or make acceptance impossible. Here the core claim survives — LLMBO-MO is implementable and produces a numerical result — but the *defense* of the design is missing. This is a Major.

---

## Decision Rationale

(300 words)

This manuscript proposes LLMBO-MO, a ParEGO-style decomposition-based MOBO augmented with two LLM-guided search mechanisms, applied to 56-evaluation multiobjective battery fast-charging design on two SPMe parameterizations. The technical execution is competent: the v2 self-audit has centralized numerical evidence, the LLM-to-surrogate boundary is rigorously enforced, the ablation is honest about the 3-seed regional-guidance limit, and the prompt-control study is informative.

The decision is Major Revision because the argument chain has three missing links (the Motivation subsection, the problem-solution Introduction, the limitations Conclusion) that all four non-DA reviewers and the DA independently flagged. These are not fatal; each is repairable by 1–2 pages of targeted writing. The supporting evidence base is also under-defended: the 5-seed main comparison lacks inferential statistics, the 3-seed regional-guidance ablation is statistically inadequate, the LLM-backend / cross-LLM robustness is absent, and the literature integration is missing four canonical references (EIMO, GPA-MOBO, Suri & Onori 2016, Tahir 2023). The single LLM backend (V4-Flash) and the absence of a "rules vs LLM" yoked control are the two strongest *external* concerns, raised independently by R1, R3, and DA. None of these is fatal either; they require additional experiments or re-framing.

The decision is **not** Reject because (a) the underlying engineering is sound, (b) every CRITICAL / Major finding is repairable, and (c) the paper's *central* claim — that LLM-derived qualitative battery knowledge can improve early-stage MOBO under a tight budget — is consistent with the available evidence (10-seed prompt study, multi-seed main comparison, honest ablation). The decision is **not** Minor Revision because the missing Motivation subsection, the feature-list Introduction, and the absent limitations paragraph are structural issues that re-organization, not polishing, must address.

---

## Required Revisions (Must Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source Reviewer | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| R1 | Add a "Design Rationale / Motivation" subsection (§IV.A) explaining why two LLM touchpoints, why initialization + early window, why weight-conditioning, why LLM rather than rules / prior data / fine-tuned head | SC-1 | Major | `absence: §IV — expected Motivation subsection between §IV.A Overview and §IV.B` | 5 | DA-CRITICAL-1, EIC-W2, R1, R2-W1, R3-W7 | must_fix | section | §IV reframed; contribution list unchanged |
| R2 | Restructure §I into a problem-solution chain: (a) state the design problem, (b) name the specific failure mode of LLAMBO-style LLM-BO on this problem, (c) introduce LLMBO-MO as the targeted fix, (d) add an EIMO-style "insights" bullet summary, (e) add a comparison paragraph against EIMO / GPA-MOBO | SC-1, SC-2 | Major | `text: §I lines 35–70`; `absence: §I — EIMO comparison and insights bullet` | 5 | DA-CRITICAL-4, EIC-W1, R2-W1, R3-W2 | must_fix | section | §I reframed; literature review expanded |
| R3 | Add an explicit limitations paragraph in §VI (EIMO template: "Despite these results, several limitations should be kept in mind…") and a "Further Discussions" expansion of §V-E addressing the null regional-guidance result, the 5-seed inferential gap, the single-LLM-backend gap, and the cross-battery generality question | SC-3, SC-4 | Major | `text: §VI`; `text: §V.E lines 336–338` | 5 | EIC-W3, R2, R3, DA-MAJOR-6 | must_fix | paragraph | §VI and §V-E expanded |
| R4 | Add a "rules vs LLM" comparator (hand-coded multi-stage template) on the same matched seeds and budget, AND/OR add a yoked prompt control (same skeleton, falsified chemistry). Reframe the "battery-specific LLM knowledge" causal claim accordingly | SC-5 | Major | `absence: §V — no rules-vs-LLM comparator`; `absence: §V.C.1 — no yoked prompt control` | 5 | R3-W1, DA-CRITICAL-2, R1-W5 | must_fix | new experiment or re-framing | §V-C.1 expanded or claim re-framed |
| R5 | Add inferential statistics to the 5-seed main comparison (Wilcoxon signed-rank or paired t-test, p-value, Cohen's d_z, 95% bootstrap CI) for both Chen2020 and Ecker2015 | SC-6 | Major | `text: §V.B lines 124–136` | 4 | EIC, R1-W3, R2, R3 | must_fix | paragraph | §V-B updated with test statistics |
| R6 | Either expand the regional-guidance ablation to ≥10 seeds, or reframe regional guidance as an optional add-on (not a peer to LLM-informed initialization) in the contribution list | SC-4 | Major | `text: §V.C.2 lines 220–223` | 5 | R1, R2, R3-W3, EIC | must_fix | experiment or re-framing | §V-C.2 expanded or contribution list re-ordered |
| R7 | Add the four canonical missing references to references.tex: (a) EIMO 2026, (b) GPA-MOBO 2024, (c) Suri & Onori 2016, (d) Tahir 2023 MCC review | SC-7 | Major | `absence: references.tex — four canonical entries missing` | 5 | R2-W1, R2-W2, R2-W4 | must_fix | references list | references.tex updated |
| R8 | Add a 1–2 sentence transition from §III (Model) to §IV (Method) that names the expensive black-box interface and states what the LLM can and cannot access | SC-1 | Minor | `absence: §III/§IV boundary — expected a transition sentence` | 5 | DA-MAJOR-5, EIC | must_fix | 1–2 sentences | §IV opening updated |

### Required Item Details

**R1: Add a Motivation / Design Rationale subsection in §IV**
- **Problem**: §IV (method) opens with a one-paragraph "Overview" and proceeds directly to the decomposition-based MOBO backbone, then to the two LLM mechanisms, without explaining *why* these two touchpoints and *why* this bounded design. A reader familiar with LLAMBO, LABO, or SoberLLMBO has no principled reason to prefer the LLMBO-MO design over the alternatives.
- **Source**: DA-CRITICAL-1; EIC-W2; R1; R2-W1; R3-W7.
- **Requirement**: Add a §IV.A "Design Rationale" subsection (1–1.5 pages) that explicitly addresses: (1) why LLM rather than rules / fine-tuned prior model / expert system; (2) why exactly two touchpoints; (3) why initialization + early window rather than full-horizon guidance; (4) why weight-conditioning and not objective- or hypervolume-conditioning. Cite LLAMBO, LABO, SoberLLMBO, and EIMO as the *inspiration* and explain the design deltas.
- **Acceptance criteria**: §IV.A exists, is 1+ page, and explicitly addresses all four design questions with citations to at least 3 of the 4 named references.

**R2: Restructure the Introduction as a problem-solution chain**
- **Problem**: §I lists three LLM mechanisms and three contributions without first establishing the gap. No EIMO-style "insights" bullet summary. No comparison with EIMO / GPA-MOBO.
- **Source**: DA-CRITICAL-4; EIC-W1; R2-W1; R3-W2.
- **Requirement**: Restructure §I: (1) state the fast-charging design problem in 2 sentences; (2) argue why BO / MOBO is the right framework; (3) name the specific failure mode of LLAMBO-style LLM-BO on this problem; (4) introduce LLMBO-MO as the targeted fix; (5) state contributions as "we fix gap #1, gap #2, and validate the whole". Add a 4–5-bullet insights summary. Add a comparison paragraph with EIMO and GPA-MOBO.
- **Acceptance criteria**: §I contains (a) an explicit "findings and insights" bullet list, (b) a transition sentence ("Based on these observations…"), (c) an EIMO / GPA-MOBO comparison paragraph, and (d) the contribution list re-framed as targeted fixes to specific gaps.

**R3: Add an explicit limitations paragraph in §VI and a "Further Discussions" expansion of §V-E**
- **Problem**: §VI is a summary, not a limitations + scope section. §V-E is 28 lines and under-engages with the null regional-guidance result, the 5-seed inferential gap, the single-LLM-backend gap, and the cross-battery generality question.
- **Source**: EIC-W3; R2; R3; DA-MAJOR-6.
- **Requirement**: Add a 6–8 sentence limitations paragraph in §VI ("Despite these results, several limitations should be kept in mind…") covering: (1) simulation-only, (2) degradation proxy not capacity-fade endpoint, (3) regional-guidance ablation inconclusive on 3 seeds, (4) no LLM-backend / cross-LLM robustness, (5) no physical-cell validation, (6) cross-battery generality is a check, not a transfer study. Expand §V-E into 3–4 sub-discussions addressing: why the prompt study isolates the LLM contribution, why the regional-guidance ablation is inconclusive, what the boundary of the LLM guidance is, and the cross-battery check scope.
- **Acceptance criteria**: §VI contains a labeled limitations paragraph; §V-E contains at least 3 labeled sub-discussions.

**R4: Add a "rules vs LLM" comparator and/or a yoked prompt control**
- **Problem**: The "battery-specific LLM knowledge" claim rests on a comparison (Random vs. Generic Prompt vs. Battery-Specific Prompt) where the Generic and Battery-Specific prompts differ along multiple dimensions (content, length, prompt engineering quality). The paper cannot distinguish "domain knowledge" from "prompt quality". A hand-coded rule baseline using the same qualitative knowledge (multi-stage current ordering, SOC allocation, monotonicity, soft terminal-span penalty) is also missing.
- **Source**: R3-W1 (CRITICAL); DA-CRITICAL-2; R1-W5.
- **Requirement**: Add a fourth arm to the §V-C.1 prompt study: a battery-domain hand-coded multi-stage template generator (e.g., a CC-then-tapered-CC schedule generator with a few physics-motivated parameter ranges). Use the same 10 matched seeds and 26-evaluation budget. Optionally add a yoked control (same prompt skeleton, falsified chemistry) to distinguish "battery knowledge" from "prompt quality". Reframe the causal claim based on the result.
- **Acceptance criteria**: §V-C.1 contains at least one of: (a) a rules-vs-LLM row, or (b) a yoked prompt control, with the corresponding re-framing of the "battery-specific LLM knowledge" claim.

**R5: Add inferential statistics to the 5-seed main comparison**
- **Problem**: The Chen2020 main result is reported as mean ± SD with no inferential test. The 5-seed sample size is borderline for any test; a Wilcoxon signed-rank on the 5 matched seeds may or may not reach significance.
- **Source**: EIC; R1-W3; R2; R3.
- **Requirement**: Add a paired Wilcoxon signed-rank test (or paired t) on the 5 matched seeds for both Chen2020 and Ecker2015 main comparisons. Report p-value, effect size (Cohen's d_z), and 95% bootstrap CI on the mean HV difference. If the test does not reach significance, soften the Abstract / Conclusion wording to "descriptive improvement" or "trend-level improvement".
- **Acceptance criteria**: §V-B and §V-C contain paired-test p-values, effect sizes, and CIs for both parameterizations.

**R6: Expand regional-guidance ablation or reframe it as auxiliary**
- **Problem**: The 3-seed regional-guidance ablation does not establish an independent systematic benefit. The paper bills regional guidance as a peer to LLM-informed initialization in the contribution list.
- **Source**: R1; R2; R3-W3; EIC.
- **Requirement**: Either (a) expand the ablation to ≥10 seeds with paired-test statistics, or (b) reframe regional guidance as an optional add-on in the contribution list, moving the LLM-informed initialization story to the foreground.
- **Acceptance criteria**: Either the ablation is expanded with paired-test statistics, or the contribution list is re-ordered to position regional guidance as auxiliary.

**R7: Add the four canonical missing references**
- **Problem**: EIMO, GPA-MOBO, Suri & Onori 2016, and Tahir 2023 are all cited by name in our reviews but absent from references.tex.
- **Source**: R2-W1, R2-W2, R2-W4.
- **Requirement**: Add the four references to references.tex. Cite EIMO and GPA-MOBO in §I (LLMBO-MO positioning). Cite Suri & Onori in §III-B (degradation proxy construction). Cite Tahir 2023 in §II-A (MCC protocol).
- **Acceptance criteria**: references.tex contains the four entries with correct bibliographic information; the four citations appear in the main text.

**R8: Add a 1–2 sentence transition from §III to §IV**
- **Problem**: §III ends with "For BO, this mapping is treated as an expensive black box." §IV opens with "LLMBO-MO augments a ParEGO-style decomposition-based multiobjective Bayesian optimization backbone…" There is no explicit bridge.
- **Source**: DA-MAJOR-5; EIC.
- **Requirement**: Add a 2-sentence transition at the start of §IV that names the expensive black-box interface and states what the LLM can and cannot access (LLM has access to battery-domain text and the BO state; LLM does not have access to the simulator, the GP, or the Pareto archive).
- **Acceptance criteria**: §IV opens with a transition paragraph that names the black-box interface and the LLM's access boundary.

---

## Suggested Revisions (Should Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source Reviewer | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Add per-iteration $R_{i,t}^{\mathrm{hist}} / R_i^{\mathrm{glob}}$ ratio (table or small-multiples figure) for the three objectives across 56 iterations | — | Major | `text: method.tex eq. objective_scale` | 5 | R1-W1 | should_fix | figure or table | §IV-A added |
| S2 | Report the soft-penalty hyperparameters ($\omega_p$, $\omega_m$, $\omega_d$, $\Delta s_K^{\mathrm{soft}}$, $w_{\mathrm{soft}}$) in Table II | — | Major | `text: method.tex eq. portfolio`; `absence: Table II — hyperparameters missing` | 4 | R1-W5 | should_fix | table | Table II updated |
| S3 | Add a LLM-call success rate and proposal-rejection-rate paragraph or table: total queries, valid points, valid regions, no-preference, rejected by screening | — | Major | `absence: §V — no LLM-call statistics` | 4 | R3-W5 | should_fix | paragraph | §IV-C expanded |
| S4 | Add a small cross-LLM robustness study (V4-Flash + one open-weight 7B–13B model) on the §V-C.1 26-evaluation budget for the initialization mechanism | — | Major | `text: Table II — "V4-Flash"`; `absence: §V — single LLM` | 4 | R3-W4, DA-MAJOR-1 | should_fix | new experiment | §V-C.1 expanded |
| S5 | Add 2–3 sentences of analytical narrative per representative protocol in Table III (EIMO V-B style) | — | Major | `text: experiments.tex §V-D`; `table: Table III` | 5 | EIC-W4, R2-W3 | should_fix | paragraph | §V-D expanded |
| S6 | Distinguish "spatially bounded" from "semantically bounded" LLM guidance; add a robustness study where the LLM is replaced with a random-region generator of the same shape | — | Major | `text: §IV-D`; `absence: §V — no null-LLM ablation` | 4 | DA-MAJOR-1, R1-W2 | consider | paragraph or new experiment | §IV-D reframed |
| S7 | Clarify whether Chen2020 and Ecker2015 use the same 5 seeds (matched) or independent seeds; report per-seed values for Ecker2015 | — | Minor | `text: §V-C` | 4 | R1, R2-W5 | should_fix | clarification | §V-C updated |
| S8 | Distinguish "as a surrogate target" from "as a candidate generator" LLM usage; clarify that the bounded-restart design is the rejection of posterior-mean reshaping | — | Minor | `text: §IV-D` | 4 | R1-W2 | consider | 1–2 sentences | §IV-D updated |
| S9 | Calibrate the $D_{\mathrm{chg}}$ proxy against a published aging dataset OR report the values as a relative ratio to a CC-CV baseline with a one-sentence justification | — | Major | `text: model.tex §III-B "arbitrary proxy units"` | 5 | R2-W6 | consider | calibration or reframing | §III-B updated |
| S10 | Add the EIMO-specific comparison paragraph (EIMO transfers optimization experience; LLMBO-MO queries an LLM; the two are complementary) | — | Major | `absence: §I` | 5 | R2-W1 | should_fix | paragraph | §I expanded |
| S11 | Add the canonical ParEGO / qEHVI / qNEHVI baselines (or explicitly state their absence as a limitation) | — | Minor | `text: §V-A` | 4 | paper_review.md | consider | paragraph | §V-A updated |
| S12 | Add a "Note to Practitioners" paragraph at the end of §I answering: who should use LLMBO-MO, what it costs in API calls, what fallback it has when LLM is unavailable | — | Minor | `absence: §I` | 4 | EIC-W5 | consider | paragraph | §I expanded |

---

## Revision Roadmap

### Source-traceability checklist

> Keep this in immutable source order. Do not suggest a work order. The author chooses `will_address`, `wont_address`, or `not_on_point` later in the separate author-adjudication checkpoint.

- [ ] R1 — obligation `must_fix`: Add Motivation / Design Rationale subsection in §IV (1–1.5 pages, addresses 4 design questions, cites 3+ of LLAMBO/LABO/SoberLLMBO/EIMO)
- [ ] R2 — obligation `must_fix`: Restructure §I as problem-solution chain (insights bullet, transition sentence, EIMO/GPA-MOBO comparison, contribution list re-framed)
- [ ] R3 — obligation `must_fix`: Add explicit limitations paragraph in §VI + "Further Discussions" expansion of §V-E (3+ sub-discussions)
- [ ] R4 — obligation `must_fix`: Add "rules vs LLM" comparator and/or yoked prompt control; reframe "battery-specific LLM knowledge" causal claim
- [ ] R5 — obligation `must_fix`: Add inferential statistics to 5-seed main comparison (Wilcoxon, p-value, Cohen's d_z, 95% bootstrap CI for both Chen2020 and Ecker2015)
- [ ] R6 — obligation `must_fix`: Expand regional-guidance ablation to ≥10 seeds OR reframe regional guidance as optional add-on in contribution list
- [ ] R7 — obligation `must_fix`: Add EIMO, GPA-MOBO, Suri & Onori 2016, Tahir 2023 to references.tex
- [ ] R8 — obligation `must_fix`: Add 1–2 sentence transition from §III to §IV naming the black-box interface and LLM access boundary
- [ ] S1 — obligation `should_fix`: Add per-iteration $R_{i,t}^{\mathrm{hist}} / R_i^{\mathrm{glob}}$ ratio for 3 objectives × 56 iterations
- [ ] S2 — obligation `should_fix`: Report soft-penalty hyperparameters in Table II
- [ ] S3 — obligation `should_fix`: Add LLM-call success rate and proposal-rejection-rate paragraph
- [ ] S4 — obligation `should_fix`: Add cross-LLM robustness study (V4-Flash + one open-weight model)
- [ ] S5 — obligation `should_fix`: Add 2–3 sentence analytical narrative per representative protocol
- [ ] S6 — obligation `consider`: Distinguish "spatially bounded" vs "semantically bounded" LLM guidance
- [ ] S7 — obligation `should_fix`: Clarify Chen2020 / Ecker2015 seed matching; report per-seed Ecker2015 values
- [ ] S8 — obligation `consider`: Distinguish "as surrogate target" vs "as candidate generator" LLM usage
- [ ] S9 — obligation `consider`: Calibrate $D_{\mathrm{chg}}$ against published aging dataset OR report as relative ratio
- [ ] S10 — obligation `should_fix`: Add EIMO-specific comparison paragraph
- [ ] S11 — obligation `consider`: Add qEHVI / qNEHVI baselines or explicitly state absence
- [ ] S12 — obligation `consider`: Add "Note to Practitioners" paragraph

---

## Journal-Supplied Deadline (Optional Transport)

- **Exact deadline from source letter**: NOT PROVIDED
- Do not infer a deadline, duration, or work estimate.

---

## Response Letter Instructions

Please use the format in `templates/revision_response_template.md` to respond to every reviewer comment item by item.

**Must include**:
1. Response and revision description for each Required Revision (R1–R8)
2. Response for each Suggested Revision (S1–S12) — adopted or reason for not adopting
3. Change markup (mark all changes in the revised manuscript with color or track changes)
4. Cross-reference table of new page numbers/paragraphs
5. **DA-CRITICAL-2 response** must explicitly address: did you add a yoked control? if not, how did you re-frame the causal claim?

---

## Closing

We encourage you to carefully consider the reviewers' comments and submit a substantially revised manuscript. The reviewers have converged on three structural issues (Method Motivation, Introduction argument chain, Conclusion limitations) and four substantive issues (rules-vs-LLM control, inferential statistics, regional-guidance framing, missing canonical references). All are repairable, and the underlying engineering is sound. Please note that the revised manuscript will undergo another round of review.

We look forward to receiving your revision.

---

## Appendix: Full Reviewer Reports

The following five reports are attached:
1. `phase1_eic_report.md` — Journal-Fit Reviewer
2. `phase1_methodology_report.md` — R1 Methodology
3. `phase1_domain_report.md` — R2 Domain
4. `phase1_perspective_report.md` — R3 Perspective
5. `phase1_devils_advocate_report.md` — Devil's Advocate

Field-analysis configuration card is in `phase0_field_analysis.md`.
