# Revision Change Log

## Author-supplied figure set restored

- Superseded the earlier diagram redraws and restored the exact original
  problem-formulation artwork and Draw.io workflow used by the author.
- Restored the tracked objective-preprocessing PDF instead of the regenerated
  visual variant.
- Reintroduced the original Ecker2015 cross-family panel and Chen2020 component
  diagnostic panels. Their captions now distinguish contextual/primary-batch
  records from the audited matched-budget tables.
- Kept the original platform, Pareto, and charging-trajectory assets unchanged;
  only LaTeX placement, scaling, and captions were adjusted.
- Rebalanced the final reference page with IEEE's reference trigger; the
  restored-image manuscript compiles to 10 pages.

## Reference-aligned structure and figure-layout reconstruction

- Merged Related Work into the Introduction and reorganized it around the
  charging-evaluation bottleneck, BO cold start, LLM--BO authority risk, the two
  controlled touchpoints, audited results, and three contributions.
- Split the electrochemical, thermal, and degradation-proxy material into an
  independent Section III and made the arbitrary-unit proxy boundary explicit.
- Reorganized the method into design principle, overall framework, four main
  steps, and the complete procedure while preserving the bounded coupling and
  algorithm interfaces.
- Rebuilt the experimental section as setup, qualitative protocol behavior,
  principal comparison, and further analysis, with four compact booktabs
  tables and archive-specific qualifications.
- Replaced the problem and framework diagrams with compact horizontal
  two-column TikZ figures; retained the platform as a one-column top figure and
  regenerated the objective-preprocessing plot from the archived CSV.
- Removed redundant or nontraceable performance, endpoint/cross-family, and
  component-diagnostic plots from the compilation entry without deleting the
  assets.
- Restored all principal claims to the audited Chen2020 and Ecker2015 values,
  removed cross-scale Ecker wording, and synchronized Abstract, Introduction,
  Experiments, and Conclusion.
- Removed forced page breaks and float-top overrides, enabled final-column
  balancing, and reduced the compiled paper from 13 to 10 naturally paginated
  pages.

## Current five-seed and formula-closure pass

- Revalidated the Chen2020 principal result over seeds 8409--8413 under the
  same 56-call budget.
- Recomputed the Ecker2015 comparison on one common benchmark-specific
  ideal/reference box and removed the earlier cross-scale comparison.
- Updated the principal results to Chen2020
  \(0.3853\rightarrow0.3885\) (+0.84%, 3/5 wins) and Ecker2015
  \(0.5540\rightarrow0.5660\) (+2.18%, 4/5 wins).
- Corrected the global-range fallback, covariance stabilization, anchor
  weighting, guidance-quality gate, and mean-shift interpretation to match the
  implementation.
- Kept the formal method symbolic and moved the retained numerical values into
  one compact core-settings table.
- Removed the component-only covariance formula from the principal method and
  described its mean-absolute-shift budget only in the component study.
- Regenerated the Pareto and trajectory panels with “degradation proxy
  (a.u.)” and “LLMBO-MO” labels, then moved the full-width panel back into the
  experimental discussion page.
- Removed forced page breaks and fixed the visual order of the platform image,
  settings table, main-results table, and qualitative figure.

## Structural changes

- Merged the former problem-formulation and simulation-model sections into
  Section III.
- Renumbered the method, experiments, and conclusion as Sections IV–VI.
- Reorganized the method around design principle, scalar backbone, warm start,
  region preference, bounded coupling, and the complete procedure.
- Reorganized experiments around archive configuration, fair comparison, main
  results, Pareto interpretation, ablation, and deployment limitations.

## Language and terminology

- Replaced “thermal stress” with “peak temperature rise” where the lumped model
  cannot support a stress claim.
- Replaced percentage-aging language with the arbitrary-unit degradation proxy
  \(D_{\mathrm{chg}}\).
- Replaced LLM “confidence” with “reported score” unless the text refers to a
  configured scalar field rather than a calibrated probability.
- Replaced generic `valid/invalid/guarded` labels with
  `accepted/rejected/unusable/screened` where parser, geometry, or coupling
  checks provide the actual criterion.
- Removed broad “sample-efficient,” “safe,” “physically plausible,”
  “mechanistic,” “promising,” and state-of-the-art implications that exceeded
  the available evidence.

## Formula-preserving clarifications

- Reduced the manuscript to seven numbered equation groups, reserving numbers
  for the problem definition, objective, selector, and proposed covariance
  coupling.
- Replaced direct implementation values in the charging-time, degradation,
  normalization, scalarization, warm-start, and coupling descriptions with
  named symbols.
- Centralized the exact numerical mappings in Table I rather than repeating
  them inside equations and prose.
- Replaced the implementation-facing fixed-stage notation with an indexed
  \(K\)-stage SOC-domain representation; the main settings table does not
  advertise an instance-specific stage count.
- Removed the standalone protocol-bound table and the numbered geometry
  equation; the equivalent terminal-stage hard and soft spans are now defined
  symbolically.
- Rewrote the archived degradation proxy as a two-line symbolic expression
  that is algebraically identical to the former `Cap` construction.
- Combined dynamic normalization and augmented Tchebycheff scalarization into
  one compact ParEGO-backbone equation while preserving the absolute ideal gap.
- Downgraded routine charge balance, thermal balance, objective transform, and
  soft-boundary penalty to unnumbered displays; the component-only
  variance-normalized operator is confined to the experiment discussion.
- Replaced the expanded Matérn kernel and standard EI equations with precise
  prose; Algorithm 1 retains the execution semantics.
- Preserved and visually emphasized the warm-start portfolio score,
  correlation-clipped coupling, explicit shift cap, and covariance bound.
- Restored the exact full-global-range fallback and the retained covariance
  stabilization constants from the implementation.

## Figures and tables

- Moved the laboratory platform photograph to the front of the experimental
  section and stated that it is intended for future protocol replay; no
  measurements from it enter the reported quantitative evaluation.
- Rewrote the framework caption to distinguish regional acquisition restarts
  from optional mean coupling.
- Replaced Fig. 2 with the user-supplied Draw.io workflow and converted it to a
  compact vector PDF so its labels remain sharp in the compiled manuscript.
- Rebuilt Fig. 1 as an Okabe--Ito three-panel formulation diagram separating
  protocol coordinates, minimized objectives, protocol-domain feasibility,
  and simulator-checked operational limits.
- Relabeled the degradation column in the Pareto table as arbitrary units.
- Removed the contextual search-curve composite from the main paper because its
  seed and initialization scopes differ and it duplicated the fixed-budget
  result narrative.
- Replaced the combined ablation plot-and-table figure with a compact
  five-seed statistics table, retaining the exact means, deviations, gains, and
  paired wins without repeating the same evidence graphically.
- Reworked the wide reproducibility table into a compact symbolic-constant and
  archive-metadata table, following the supplied reference paper.
- The Fig. 1 current-profile thumbnail is deliberately generic and
  nonmonotone: stage ordering is not presented as a hard constraint. Its
  evaluator arrow explicitly identifies the coupled SPMe--thermal simulation.
- Repositioned the final-HV table directly after the main-results heading so
  that the numerical evidence remains adjacent to its interpretation.
- Kept the platform photograph at the beginning of experiments and moved the
  parameter-table float ahead of the quantitative figures.
- Kept the experimental-platform photograph at the start of Section V and
  opened the Pareto panel at the top of the following interpretation page.
- The final eight-page PDF preserves the result-to-figure order without
  placing the wide Pareto panel on the references page.

## Evidence-attribution corrections

- Reported both principal comparisons over the common seed range 8409--8413.
- Restricted the principal claim to complete-configuration fixed-budget
  performance rather than assigning causality to one advisory touchpoint.
- Reserved component-level region-coupling evidence for the separate component
  study.
- Disclosed that principal ParEGO comparisons match the simulator, objectives,
  total budget, and HV definition but not the initialization mechanism.

## Reproducibility additions

- Recorded LLM aliases, interface type, retained decoding metadata,
  warm-start-pool sizes, region modes, guidance horizons, anchor counts, box
  limits, mean-shift budgets, and coupling outcomes.
- Used “N.R.” for fields not retained by the archive instead of inventing
  values.
- Distinguished five-seed numerical results from the pooled qualitative
  visualization archive.
- Removed the archive-specific efficiency paragraph from the manuscript because
  the retained runs do not provide a controlled cross-backend comparison.

## Deferred changes that require rerunning experiments

- Removing the absolute ideal-point gap.
- Replacing dynamic objective scaling with fixed global bounds.
- Substituting a calibrated degradation/capacity-fade model.
- Running synchronized four-arm ablations from one common code snapshot.
- Adding matched qEHVI/qNEHVI baselines and identical initial databases.
- Drawing hardware-level conclusions from the laboratory platform.

## Second-pass reference-paper alignment

- Compared the draft page by page with the two user-supplied papers.
- Renamed Section V to “Numerical Validation and Discussion,” matching the
  simulation-only evidence and the validation/discussion progression used by
  the fast-charging reference paper.
- Split the fast-charging Related Work discussion into foundational BO and
  recent acceleration/prior mechanisms.
- Added recent digital-twin BO and parallel satisficing BO references to cover
  online adaptation and time-sensitive parallel search.
- Aligned the platform photograph with the experimental-setup placement used by
  the parameter-identification reference, while keeping simulation-only scope
  explicit in the caption and surrounding text.

## Third-pass formula-hierarchy alignment

- Matched the supplied transfer-optimization paper's separation between
  symbolic method equations and tabulated numerical settings.
- Kept model coefficients, objective-processing constants, selector weights,
  LLM metadata, and coupling caps out of the displayed method equations.
- Explicitly identified the screened portfolio and bounded acquisition-time
  posterior-covariance adjustment as the method-specific mathematical content;
  standard GP and EI machinery is now concise background.
- Verified visually that the consolidated parameter table precedes the Pareto
  figure and that the platform photograph remains in the experimental setup.

## Table and narrative simplification

- Recast Tables I--IV with comparison-purpose captions and concise headers;
  removed the Wins columns and seed identifiers from the compiled manuscript.
- Preserved the audited means, sample deviations, improvements, and prompt
  p-value in the tables while changing surrounding prose to trend-level claims.
- Compressed the Abstract, Introduction, Method overview, Simulation Setup,
  Results discussion, and Conclusion to remove call, seed, and batch-log detail.
- Retained every author-supplied figure asset unchanged and simplified only the
  explanatory captions for the auxiliary Ecker and component panels.
- Recompiled the 10-page IEEE manuscript without box, citation, reference, or
  label diagnostics and balanced the final reference columns.
