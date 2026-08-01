# Claim–Evidence Matrix

| Manuscript claim | Evidence | Valid scope | Enforced wording |
|---|---|---|---|
| LLM output is advisory, not an objective observation | Only simulator evaluations enter the GP training database | All reported configurations | “Only simulator outputs train the surrogate.” |
| Rejected guidance recovers ordinary EI | Parser, geometry, anchor, and coupling fallbacks have zero mean adjustment | Algorithmic property | Exact recovery claim, not a performance claim |
| The main covariance coupling is bounded | Eq. (5) clips the standardized mean reduction by \(\delta_{\max}\) | Correlation-clipped operator | \(0\leq\delta_t(\theta)\leq\delta_{\max}\) |
| Chen2020 mean final HV is higher | ParEGO \(0.3853\pm0.0094\); LLMBO-MO \(0.3885\pm0.0088\) | Seeds 8409–8413; 56 calls; sample SD | +0.84%, 3/5 paired wins; “modest configuration-level advantage” |
| Ecker2015 mean final HV is higher | ParEGO \(0.5540\pm0.0121\); LLMBO-MO \(0.5660\pm0.0104\) | Seeds 8409–8413; 56 calls; common ideal/reference box; sample SD | +2.18%, 4/5 paired wins |
| HV comparisons are fair within each parameterization | Identical transformed objectives and benchmark-specific box for both methods | Within Chen2020 or within Ecker2015 | Absolute HV is not compared across parameterizations |
| Warm starting contributes positively in the component study | \(0.3902\pm0.0078\) versus \(0.3836\pm0.0101\); 4/5 wins | Chen2020 component batch | Larger and more consistent individual change |
| Regional guidance can help | \(0.3862\pm0.0112\); +0.0026; 4/5 wins | Chen2020 component batch | Positive but more dispersed component change |
| The complete component configuration has the highest mean | \(0.3932\pm0.0117\); 3/5 wins | Matched-budget five-seed follow-up | Seed-dependent complementarity, not uniform synergy |
| \(D_{\mathrm{chg}}\) measures a relative degradation proxy | Fixed trajectory-average algebra; no calibrated cycling fit | Common simulator only | Arbitrary proxy units, never percentage capacity loss |
| The platform is an intended validation interface | No platform measurement enters a reported result | Deployment context only | Simulation-only caption and limitations |

## Claims that still require new evidence

- Causal attribution of the principal fixed-budget gains to one advisory
  touchpoint.
- Statistical significance beyond five seeds.
- Superiority to matched qEHVI/qNEHVI or other direct-hypervolume BO methods.
- Calibrated lifetime or capacity-fade improvement.
- Hardware robustness, protection performance, or cell-to-cell generalization.
