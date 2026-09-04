# Revision Change Log

## Posterior-covariance Region-Lift restoration

- Restored Region-Lift as the proposed online LLM--GP coupling mechanism in
  the abstract, introduction, method, algorithm, experiment settings, and
  conclusion.
- Replaced the restart-only description with the implemented path:
  accepted LLM region $\rightarrow$ feasible Sobol anchors $\rightarrow$
  standardized GP posterior cross-covariance $\rightarrow$ bounded signed
  acquisition-time mean shift $\rightarrow$ lifted EI.
- Added numbered definitions for the regional latent variance, normalized
  candidate--region correlation, confidence/early-window attenuation,
  mean/max budget scaling, lifted ranking mean, and lifted EI.
- Kept the fitted GP posterior, predictive standard deviation, simulator
  observations, and Pareto dominance relation unchanged; invalid or
  degenerate guidance falls back to standard EI.
- Updated Algorithm 1 while preserving the established manuscript figure sequence.
- Preserved the evidence boundary: archived restart/candidate-pool results are
  not presented as causal evidence for the corrected covariance coupling.

## Current evidence-alignment pass

- Centralized all reported experimental values in
  `sections/experiment_values.tex`.
- Replaced the former Chen2020 result with five archived seeds:
  LLMBO-MO \(0.3848\pm0.0073\) and ParEGO
  \(0.3778\pm0.0169\).
- Added NSGA-II, DISK, and PIMD to the main Chen2020 table.
- Regenerated the supplied five-way Chen figure with `LLMBO-MO` and `HV`
  labels while preserving the archived curves.
- Distinguished representative seed-8409 center lines and proxy envelopes from
  genuine five-run mean/standard-deviation curves.
- Replaced Fig. 4 with the specified Ecker2015 five-seed archive: the observed
  difference is \(28.3\%\) at evaluation 30 and \(17.8\%\) at evaluation 56.
- Positioned Chen2020 as the primary parameterization and Ecker2015 as a
  secondary cross-parameterization check.
- Restored the five-seed min--max, Z-score, and unnormalized objective-
  preprocessing sensitivity study.
- Added the iteration-indexed Pareto-archive growth diagnostic, ending at mean
  archive sizes of 49.4 for LLMBO-MO and 45.8 for ParEGO.
- Rebuilt the Pareto plot from five Chen2020 databases and added a traceable
  Table III-style A--E protocol parameter table.
- Moved Fig. 1 to IEEE-compatible top floating and brought its feedback path
  inside the frame, removing the Section III transition gap without negative
  spacing.
- Added the ten-seed prompt study as the primary controlled language-component
  evidence.
- Corrected the component table to show warm start as the more stable
  contributor and removed additive/synergy claims.
- Removed the hardware photograph and all implications of physical validation.
- Removed outcome-count reporting from the manuscript and audit documents.

## Method and terminology corrections

- Unified the metric label as `HV` throughout the manuscript.
- Defined the algorithm budget as \(N=n_0+n_{\mathrm{BO}}=6+50\).
- Clarified that the bounded mean adjustment is expressed in standardized
  scalar-target units rather than as a fraction of posterior standard
  deviation.
- Clarified that the main Chen archive uses early candidate-pool expansion with
  posterior-mean coupling disabled.
- Restricted fallback statements to the numerical operator being disabled;
  removed claims that LLM guidance cannot reduce optimization performance.
- Replaced template author, affiliation, date, and volume strings with an
  anonymous review title block.

## Deferred work requiring new evidence

- synchronized five-seed reruns;
- matched qEHVI/qNEHVI experiments;
- an isolated regional-coupling study;
- calibrated aging and physical-cell validation.
