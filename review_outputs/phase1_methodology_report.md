# Peer Review Report — Methodology Reviewer (R1)

## Manuscript Information
- **Title**: Battery Fast-Charging Protocol Design via Large Language Model-Guided Multiobjective Bayesian Optimization
- **Review Date**: 2026-08-27
- **Review Round**: Round 1

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology

### Reviewer Identity
Bayesian-optimization and multi-objective optimization methodology expert, with publications on Gaussian process surrogate modeling, ParEGO family, qEHVI / qNEHVI, and acquisition function design. Has served on the program committees of NeurIPS BO track, ICML AutoML, and AISTATS.

### Review Focus
1. Mathematical correctness of the GP + EI + Tchebycheff backbone
2. Interaction between log-transform, normalization, and scalarization under tight evaluation budgets
3. Reproducibility: 56 calls / 5 seeds — is this enough to support the claimed advantages?
4. Whether the bounded LLM touchpoint interacts cleanly with the underlying BO loop (no leakage into surrogate targets or Pareto archive)

### Will particularly care about
The log-transform choice (eq. objective_transform) interacting with the early-stage `R_{i,t}^{hist}` scale equation (eq. objective_scale), and whether the regional-guidance mechanism is mathematically *separate* from the EI landscape (or whether it implicitly biases it through the restarts).

### Possible blind spots
Will not assess the LLM prompt engineering or the physical plausibility of the battery model.

---

## Overall Assessment

### Recommendation
**Major Revision**

### Confidence Score
5 (Completely within my area of expertise.)

### Summary Assessment
The methodological core of LLMBO-MO — a ParEGO-style decomposition-based MOBO with two LLM touchpoints — is implemented competently and the v2 audit has done visible work to centralize numerical evidence. The mathematical design is sound in isolation. However, four methodology-level concerns require attention before acceptance: (i) the **log transform + range-based normalization in eq. objective_transform / eq. objective_scale** has a subtle interaction in the early iterations when the historical range is narrower than the global range — the resulting scalarization can be dominated by a single objective; (ii) the **claim that the regional guidance "does not modify" the EI landscape** is asserted but not proved, and a careful reader will want a one-paragraph argument for why additional restarts in the EI search are not a form of landscape bias; (iii) the **5-seed main comparison is descriptive** (the v2 audit itself flags "descriptive five-archive summary") and the HV mean ± SD improvement over ParEGO is at the edge of the standard-deviation bands, so the statistical significance is not established; (iv) the **regional-guidance ablation uses only 3 seeds** and the conclusion "the three-seed experiment does not establish an independent systematic benefit" should be displayed in the table caption, not buried in the prose. None of these is fatal; all are repairable through tightening, explicit claims adjustment, and one additional seed-8409 trajectory.

---

## Strengths

### S1: Correctly identifies the LLM evidence-chain boundary
**Evidence Anchor**: text: method.tex "no unevaluated LLM proposal is used as a surrogate target or Pareto value" + method.tex "Anchors sampled from an accepted region are used only as additional restarts for the numerical EI maximization; the original acquisition restarts and the full protocol domain are retained"
The paper is unusually rigorous about preventing LLM outputs from leaking into the GP training set or the Pareto archive. This is a methodological virtue: the LLM is restricted to "where to look" and never to "what the objective is".

### S2: Decent decomposition of "LLM-informed initialization" into screening, ranking, diversity
**Evidence Anchor**: text: method.tex §IV-C "Non-numerical or non-finite entries and duplicates are removed, box violations are clipped, and candidates that cannot satisfy $\Delta s_K \geq \Delta s_K^{\min}$ are rejected... the LLM score, the soft protocol heuristic, and decision-space diversity"
The LLM-informed initialization is decomposed into a screening pass (admissibility), a ranking pass (LLM score), and a diversity pass (decision-space distance). This is the right factorization for a hybrid LLM-BO initialization.

### S3: Honest about regional-guidance ablation limit
**Evidence Anchor**: text: experiments.tex §V-C "the three-seed experiment does not establish an independent systematic benefit for this component"
Most LLM-BO papers over-claim the regional-guidance component; LLMBO-MO does not. This is methodologically correct.

---

## Weaknesses

### W1: Log-transform + range-based normalization interaction in early iterations
**Problem**: Eq. (objective_transform) applies $\log_{10}\max(t_c/t_{\mathrm{ref}}, \varepsilon_t)$ and $\log_{10}\max(D_{\mathrm{chg}}/D_{\mathrm{ref}}, \varepsilon_D)$ but leaves $\Delta T_p$ untransformed. Eq. (objective_scale) then uses $R_{i,t}^{\mathrm{hist}}$ as the denominator, switching to $R_i^{\mathrm{glob}}$ only when $R_{i,t}^{\mathrm{hist}} < \rho_R R_i^{\mathrm{glob}}$. In the first ~5 iterations, the observed $\Delta T_p$ range is dominated by a single protocol; the early $\bar f_{i,t}$ for $\Delta T_p$ can therefore be much larger than the $\bar f_{i,t}$ for $\log t_c$ and $\log D_{\mathrm{chg}}$, and the Tchebycheff scalarization is then dominated by $\Delta T_p$. The manuscript does not report the per-iteration $\bar f_{i,t}$ balance or the per-iteration $s_{i,t}$ ratio.
**Evidence Anchor**: text: method.tex eq. objective_transform + eq. objective_scale
**Why it matters**: If the scalarization is dominated by a single objective in early iterations, the GP fit is effectively single-objective, the EI landscape is narrow, and the "early-search" claim of the paper is compromised. This is a recurring failure mode in log-mixed MOBO.
**Suggestion**: Add a per-iteration table or small-multiples figure showing the ratio $R_{i,t}^{\mathrm{hist}} / R_i^{\mathrm{glob}}$ for the three objectives across the 56 iterations, or argue analytically why the log transform prevents the imbalance (the reviewer does not believe the argument is trivially true).
**Severity**: Major
**Confidence**: 5 — core expertise: BO scalarization

### W2: Regional guidance's claim of "no landscape bias" is asserted, not proved
**Problem**: §IV-D (method.tex) states: "Regional guidance therefore biases the numerical search without restricting the feasible search space or modifying objective values, GP training targets, the posterior model, or Pareto relations." This claim is correct *for the restarts themselves*, but the additional restarts do change the *probability* that EI lands in a particular region of the input space, and that is a form of bias on the realized trajectory. The author should distinguish between (a) modifying the EI landscape and (b) modifying the EI *optimizer's* sampling distribution.
**Evidence Anchor**: text: method.tex §IV-D "Regional guidance therefore biases the numerical search without restricting the feasible search space or modifying objective values, GP training targets, the posterior model, or Pareto relations."
**Why it matters**: The reader needs to understand whether the regional-guidance advantage (modest, as the 3-seed ablation reports) comes from (a) sampling more points in the LLM-suggested region (which is allowed) or (b) from a hidden change in the EI landscape (which is not). The current prose collapses the two.
**Suggestion**: Add one sentence: "The additional restarts only change the EI optimizer's multi-start distribution; the EI function itself is unmodified. The realized trajectory is biased, the EI landscape is not."
**Severity**: Minor
**Confidence**: 5 — core expertise: acquisition function design

### W3: 5-seed main comparison is descriptive, not inferential
**Problem**: The Chen2020 final HV is reported as $0.3848 \pm 0.0073$ (LLMBO-MO) vs. $0.3778 \pm 0.0169$ (ParEGO). The improvement (~1.85% relative) is well within one standard deviation of ParEGO. The Ecker2015 result at evaluation 30 is reported as a 28.3% difference but no inferential statistic is given.
**Evidence Anchor**: text: paper_review.md "Chen result $0.3848 \pm 0.0073$ vs. $0.3778 \pm 0.0169$, descriptive five-archive summary" + experiments.tex §V-C
**Why it matters**: A 5-seed comparison is below the threshold of most statistical tests; if the manuscript wants to claim a *significant* improvement, it should at minimum (a) report the paired t-test p-value (or Wilcoxon signed-rank) and the effect size, or (b) acknowledge the comparison is descriptive and adjust the Abstract/Conclusion wording.
**Suggestion**: Either run a paired Wilcoxon signed-rank test on the 5 matched seeds and report the p-value + effect size, or soften the claim in the Abstract from "improvement" to "descriptive improvement" or "trend-level improvement".
**Severity**: Major
**Confidence**: 4 — core expertise: statistical reporting

### W4: Bounded preference coupling (Appendix A) is mis-marked as "diagnostic"
**Problem**: Appendix A develops a bounded posterior-mean coupling in standardized scalar-target units. The text says "this is a diagnostic realization and is not used to define the principal results", but the equations (eq. bounded_coupling) include hyperparameters $\lambda_{\max}$, $\eta_H$, $\eta_{\mathrm{EI}}$, $\eta_\sigma$, $\eta_n$, $T_v$, $\varepsilon_v$, $\varepsilon_K$, $\varepsilon_H$ that are not reported. A reader cannot reproduce the Appendix A experiment, and a reviewer cannot tell whether the coupling was actually disabled in the main experiment or simply turned off in the post-processing.
**Evidence Anchor**: absence: appendices.tex — expected a parameter table for the bounded preference coupling; checked §A absent
**Why it matters**: If the coupling is "diagnostic", its parameters should be reported; if they are not reported, the diagnostic claim is hollow and the reviewer cannot verify the separation between main and coupling runs.
**Suggestion**: Either report the parameters or delete the appendix.
**Severity**: Minor
**Confidence**: 4 — core expertise: reproducibility

### W5: The "soft penalty" $p_{\mathrm{soft}}$ in initialization is a heuristic, but no justification
**Problem**: The LLM-informed initialization scoring function (eq. portfolio) combines a soft penalty $p_{\mathrm{soft}}$ for "a terminal SOC span below a preferred boundary" with the LLM score and diversity, weighted by $\omega_p$, $\omega_m$, $\omega_d$. The values of $\omega_p$, $\omega_m$, $\omega_d$, $\Delta s_K^{\mathrm{soft}}$, and $w_{\mathrm{soft}}$ are not reported in Table II (Algorithm Settings), and there is no sensitivity study.
**Evidence Anchor**: text: method.tex eq. portfolio + eq. soft_penalty + absence: experiments.tex Table II — expected the soft-penalty hyperparameters; checked Table II absent
**Why it matters**: The choice of soft-penalty hyperparameters can dominate the initialization portfolio; without reporting them or a sensitivity study, the reader cannot tell whether the LLMBO-MO advantage comes from the LLM information or from the soft-penalty heuristic.
**Suggestion**: Report the hyperparameters in Table II and add a one-line justification (e.g., "$\omega_p$ was set to balance the LLM score range with the $[0, 1]$ soft penalty; sensitivity to $\omega_p$ in $\{0.1, 0.3, 0.5\}$ was negligible").
**Severity**: Major
**Confidence**: 4 — core expertise: hyperparameter reporting

---

## Coverage Receipt
Not applicable (lists populated).

---

## Detailed Comments

### Methodology / Research Design
- See W1, W3, W5 above. The Math is correct; the design choices are defensible; the *justification* for several choices is incomplete.
- The augmented Tchebycheff scalarization is standard (eq. tchebycheff); the $\rho_{\mathrm{aug}}$ value is not reported.
- The ARD Matérn-5/2 GP with a white-noise term is the right choice for smooth objective functions; the noise-floor value is not reported.

### Sampling Strategy
- 5 seeds × 56 evaluations is a small but defensible budget. The 10-seed prompt study at 26 evaluations is a useful complement. The 3-seed ablation at 16 evaluations is below the standard for "systematic benefit" claims.

### Data Collection
- All evaluations come from one simulator (SPMe via PyBaMM), which is the right design choice for isolating the search algorithm from the simulator. The Chen2020 and Ecker2015 parameterizations are documented.

### Analysis Methods
- HV is the right primary metric. The 5-seed main comparison is descriptive. The paired comparison in the prompt study is supported by Holm multiplicity correction (good). The 3-seed ablation is honestly under-powered.

### Reproducibility
- Single value file: ✓
- Algorithm budget: ✓
- Battery parameters: ✓
- LLM prompt: not reported in main text (only in experiment logs)
- Algorithm hyperparameters: partial (Table II has 6 rows, the manuscript has 15+ parameters)

### Statistical Validity
- See W3. Wilcoxon signed-rank or paired t-test missing for the main comparison.

---

## Criterion-Bound Judgements

| Dimension | Criterion source | Judgement | Evidence anchor(s) | Rationale | Decision bearing? |
|---|---|---|---|---|---|
| Originality | §1 universal | PARTLY_MEETS | text: §IV (mechanism) | LLM-informed initialization is close to LLAMBO 2024; the bounded-restart design is the genuine methodological novelty. | No |
| Methodological Rigor | §1 universal | PARTLY_MEETS | text: method.tex eq. objective_scale; absence: Table II hyperparameters | Math is correct; design choices are defensible but under-justified. W1, W5 are real. | Yes |
| Evidence Sufficiency | §1 universal | PARTLY_MEETS | text: experiments.tex §V-C; absence: paired test | The 5-seed main comparison is descriptive, not inferential. W3 is real. | Yes |
| Argument Coherence | §1 universal | PARTLY_MEETS | text: §IV (regional guidance claim) | The "no landscape bias" claim is over-stated. W2 is real. | No |
| Writing Quality | §1 universal | MEETS | text: §IV (overall) | Math and prose are clear; the level of notation is consistent. | No |
| Literature Integration | §1 universal | PARTLY_MEETS | references.tex; absence: warm-start BO refs | Thin on warm-start BO and qEHVI / qNEHVI comparisons. | No |
| Significance & Impact | §1 universal | MEETS | text: §V (results) | The bounded-restart design has a real methodological value if the prompt study and the 5-seed main comparison are reported honestly. | No |

**Decision-bearing explanation**: Two criteria (Methodological Rigor, Evidence Sufficiency) are unresolved. Both are repairable. The recommendation is therefore Major Revision, not Reject.

---

## Questions for Authors

1. Eq. (objective_scale) uses $R_{i,t}^{\mathrm{hist}}$ as the denominator when the observed range is wide enough. Can the author report the per-iteration $R_{i,t}^{\mathrm{hist}} / R_i^{\mathrm{glob}}$ ratio for the three objectives, to show the early-iteration objective balance is not dominated by a single objective?
2. The "soft penalty" $p_{\mathrm{soft}}$ in the LLM-informed initialization has hyperparameters $\omega_p$, $\omega_m$, $\omega_d$, $\Delta s_K^{\mathrm{soft}}$, $w_{\mathrm{soft}}$ that are not reported. Can the author add them to Table II?
3. The 5-seed Chen2020 main comparison reports LLMBO-MO $0.3848 \pm 0.0073$ vs. ParEGO $0.3778 \pm 0.0169$. Can the author run a paired Wilcoxon signed-rank test on the 5 matched seeds and report the p-value + effect size?
4. The augmented Tchebycheff scalarization uses $\rho_{\mathrm{aug}}$; can the author report its value?
5. The ARD Matérn-5/2 GP uses a white-noise term; can the author report the noise-floor value?

---

## Minor Issues

- method.tex line 87: "The selected protocol is repaired to $\Theta_{\mathrm{proto}}$" — clarify whether the repair is hard clipping or back-projection.
- method.tex line 70: the Tchebycheff scalarization is described as "augmented" but $\eta$ in the EIMO paper is not the same as $\rho_{\mathrm{aug}}$ here; the author should clarify the relationship.
- experiments.tex: the 3-seed ablation labels (8409, 8410, 8411) should be cross-referenced to the figure manifest.
- references.tex: ref14 (Jiang 2022) DOI is missing.
- The word "warm start" appears in §II, §III, and §IV with subtly different meanings; recommend a single definition.
