# Equation Audit

This audit records the final formula-hierarchy pass. The manuscript now uses
symbolic equations for the general method and places only the small set of
settings needed for reproduction in Table I. Elementary definitions and
implementation inventory are not promoted to numbered equations.

| Topic | Final treatment | Consistency check |
|---|---|---|
| Charging protocol | A generic \(K\)-stage decision vector and dependent terminal SOC span replace the visually limiting three-stage formulation. The archived stage count is not advertised in the main equations or settings table. | The simulator interface and feasible protocol domain are unchanged. |
| Cell current and charge time | \(I_{\mathrm{cell}}=\phi_{\mathrm{cell}}(I_k)\) and the \(K\)-indexed charge-time relation are symbolic and unnumbered. | No topology-specific numerical factor is embedded in the method statement. |
| Objectives and constraints | One numbered constrained multiobjective problem contains charging time, peak temperature rise, and the degradation proxy. | Operational voltage, temperature, SOC, and current checks remain simulator-side feasibility conditions. |
| Thermal and degradation model | Standard thermal balance and trajectory averages are concise and unnumbered. The degradation objective is explicitly presented as a proxy with symbolic coefficients. | No claim of measured capacity loss or calibrated lifetime is made. |
| Objective transformation | Time and degradation use dimensionless base-10 transforms; temperature remains in its native transformed coordinate. | Both methods receive the same transformation within each benchmark. |
| Dynamic range fallback | If the historical range is narrower than \(\rho_R R_i^{\mathrm{glob}}\), the scale falls back to the full \(R_i^{\mathrm{glob}}\). | This matches the archived implementation; it does not substitute the smaller threshold product. |
| ParEGO target | The augmented Tchebycheff scalarization is retained because it defines the numerical optimization backbone. | LLMBO-MO and ParEGO use the same weight construction and scalar target. |
| Warm-start portfolio | Repair, diversity screening, and the portfolio score are expressed symbolically; routine bounds are in prose. | LLM proposals cannot bypass the protocol-domain checks. |
| Regional preference | An accepted point/box is converted into 32 feasible Sobol anchors with uniform weights. Confidence is a gated and scaled protocol reliability weight, not a calibrated probability. | This matches `warmstart_region_lgbo_proposition1`; the former heuristic anchor scores, entropy/quality gates, and trust-state product are not claimed. |
| Covariance projection | Regional variance \(V_{G,t}\) and normalized candidate--region correlation \(\rho_t\) are defined using standardized GP posterior covariance. | The numerator and denominator use the same posterior-covariance source; degenerate \(V_{G,t}\) triggers standard EI. |
| Principal coupling | A signed standardized shift is attenuated in the early window, globally rescaled to mean/max anchor budgets, pointwise clipped, and mapped back to scalar-target units. | Positive covariance attracts and negative covariance suppresses; this matches the implemented signed shift rather than the obsolete positive-part expression. |
| Posterior boundary | The fitted GP posterior and predictive standard deviation are unchanged; only the mean passed to EI for candidate ranking is adjusted. | The manuscript calls \(\mu_t^{\mathrm L}\) an acquisition-time ranking mean, not a recalibrated GP posterior. |
| Hyperparameters | Table II contains the fixed budget, initialization settings, and core corrected Region-Lift settings. | The stated values match the corrected preset: \(T_{\mathrm L}=12\), \(M=32\), \(c_{\min}=0.60\), \(\alpha_c=0.25\), and standardized budgets 0.05/0.15. |
| Hypervolume | HV is reported as the evaluation metric, using one common ideal/reference box for both methods within each parameterization. | Values are comparable within Chen2020 or Ecker2015, but not interpreted across the two parameterizations. |

## Audit conclusion

The retained numbered equations correspond to the problem definition,
method-specific portfolio construction, ParEGO target, and the proposed bounded
coupling. The Region-Lift equations now track the corrected implementation, but
the historical manuscript-facing archives do not constitute its matched
coupling-on validation. Changing the degradation proxy, scalar target, coupling
operator, or benchmark normalization would change the experiment and therefore
requires new runs.
