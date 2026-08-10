# Manuscript Revision Audit

## Current evidence contract

- `D:/Users/aa133/Desktop/Paper` is the canonical manuscript.
- No new simulator or LLM calls were made for this revision.
- All manuscript-facing numbers are defined in `sections/experiment_values.tex`.
- Chen2020 reports five archived seeds per method under a 56-evaluation cap.
- The Chen LLMBO-MO/ParEGO seed-8409 trajectories come from the supplied
  five-way figure archive; the remaining seed entries are mapped in the result
  provenance record.
- Ecker2015 reports the five-seed mean curve with sample-standard-deviation
  bands and separates the evaluation-30 and evaluation-56 comparisons.
- The objective-preprocessing figure reports five-seed mean HV and sample-
  standard-deviation bands for min--max, Z-score, and no normalization.
- The optimal-protocol plot is explicitly indexed by algorithmic iteration;
  its final archive means are 49.4 and 45.8 and are not treated as HV.
- Pareto representatives A--E are feasible, globally nondominated database
  records with seed and observation provenance in `results/`.
- HV is interpreted only within one battery parameterization.

## Claim closure

| Topic | Current treatment | Status |
|---|---|---|
| LLM authority | Advisory candidate generation and ranking only | Pass |
| Simulator authority | Sole objective oracle; only evaluated protocols train the GP | Pass |
| Main Chen region mechanism | Candidate-pool expansion; posterior-mean shift disabled | Pass |
| Optional coupling | Bounded in standardized target units and separated from main evidence | Pass |
| Total budget | Six initialization plus 50 BO calls | Pass |
| Chen result | \(0.3848\pm0.0073\) vs. \(0.3778\pm0.0169\), descriptive five-archive summary | Pass with limitation |
| Ecker result | \(28.3\%\) at evaluation 30; \(17.8\%\) at evaluation 56 | Pass |
| Objective preprocessing | Scale-balanced variants are stable; no significance claim between min--max and Z-score | Pass |
| Optimal protocol set | Per-iteration archive-growth diagnostic, distinct from equal-call sample efficiency | Pass |
| Pareto representatives | A--E figure labels and parameter table use identical database records | Pass |
| Prompt mechanism | Ten-seed, short-budget controlled study | Pass |
| Regional contribution | No systematic independent benefit claimed | Pass |
| Physical validation | Not claimed; hardware photograph removed from the manuscript | Pass |

## Presentation closure

- The title page contains anonymous review metadata rather than IEEE template
  examples.
- The Chen five-way plot has `LLMBO-MO` and `HV` labels.
- Figure captions state the seed and uncertainty identity of every curve.
- Fig. 1 uses top floating and keeps the feedback arrow inside the panel frame.
- Tables use booktabs, consistent precision, and no outcome-count column.
- The abstract, introduction, experiments, and conclusion draw values from one
  macro file.

## Evidence gaps that wording cannot repair

1. synchronized reruns from one code snapshot;
2. matched qEHVI/qNEHVI baselines;
3. a controlled acquisition-only regional-coupling study;
4. degradation-proxy calibration;
5. physical-cell validation.
