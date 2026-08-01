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
| Regional preference | Anchor scores, softmax weights, covariance correlation, quality gate, confidence, trust, and early-window attenuation are defined before use. | The empty-set convention for nearest-neighbor distance is \(d_{\min}=0\); \(\varepsilon_K=10^{-6}\) and \(\varepsilon_v=10^{-12}\) are listed in Table I. |
| Principal coupling | Only the bounded posterior-covariance mean adjustment is formalized and numbered in the main method. It leaves fitted targets and posterior variance unchanged. | Explicit clipping gives \(0\leq\delta_t(\theta)\leq\delta_{\max}\), and all gates must pass before the adjusted mean is active. |
| Component-only operator | The variance-normalized regional variant is confined to the component study and described by its mean-absolute-shift budget \(B_\delta\). | It is not presented as the principal LLMBO-MO operator and its budget is not misreported as a pointwise cap. |
| Hyperparameters | Table I contains the fixed budget, seeds, initialization composition, backend, and only the core coupling settings. | Simulator coefficients, fitted GP parameters, and low-level constants are not mixed into the optimization settings. |
| Hypervolume | HV is reported as the evaluation metric, using one common ideal/reference box for both methods within each parameterization. | Values are comparable within Chen2020 or Ecker2015, but not interpreted across the two parameterizations. |

## Audit conclusion

The retained numbered equations correspond to the problem definition,
method-specific portfolio construction, ParEGO target, and the proposed bounded
coupling. The paper no longer exposes a long list of elementary formulas or
numeric substitutions. Changing the degradation proxy, scalar target, coupling
operator, or benchmark normalization would change the experiment and therefore
requires new runs; the present revision does not make those changes.
