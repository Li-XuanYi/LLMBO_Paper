# Equation Audit

This audit records the final formula-hierarchy pass. All semantic display
equation groups in the manuscript are now numbered, aligned at their principal
relation signs, and cited from the surrounding prose. Closely related lines
share one equation number, while ordinary inline definitions remain unnumbered.

| Topic | Final treatment | Consistency check |
|---|---|---|
| Charging protocol | A generic \(K\)-stage decision vector and dependent terminal SOC span replace the visually limiting three-stage formulation. The archived stage count is not advertised in the main equations or settings table. | The simulator interface and feasible protocol domain are unchanged. |
| Cell current and charge time | \(I_{\mathrm{cell}}=\phi_{\mathrm{cell}}(I_k)\) and the \(K\)-indexed charge-time relation are symbolic and unnumbered. | No topology-specific numerical factor is embedded in the method statement. |
| Objectives and constraints | One numbered constrained multiobjective problem contains charging time, peak temperature rise, and the degradation proxy. | Operational voltage, temperature, SOC, and current checks remain simulator-side feasibility conditions. |
| Thermal and degradation model | The thermal balance/temperature objective and degradation proxy are numbered and cited where the reported objectives are introduced. | No claim of measured capacity loss or calibrated lifetime is made. |
| Objective transformation | The dimensionless base-10 transform is numbered and cited before benchmark comparison. | Both methods receive the same transformation within each benchmark. |
| Dynamic range fallback | The hybrid scale is numbered; if the historical range is narrower than \(\rho_R R_i^{\mathrm{glob}}\), it falls back to \(R_i^{\mathrm{glob}}\). | This matches the archived implementation; it does not substitute the smaller threshold product. |
| ParEGO target | The augmented Tchebycheff scalarization is numbered and cited because it defines the numerical optimization backbone. | LLMBO-MO and ParEGO use the same weight construction and scalar target. |
| Warm-start portfolio | The soft penalty, portfolio score, and diversity distance are separately numbered and linked by explicit prose references. | LLM proposals cannot bypass the protocol-domain checks. |
| Regional preference | Anchor scores, covariance projection, and quality gate are numbered and cited; confidence, trust, and attenuation remain concise inline definitions. | The empty-set convention for nearest-neighbor distance is \(d_{\min}=0\); \(\varepsilon_K=10^{-6}\) and \(\varepsilon_v=10^{-12}\) are listed in Table I. |
| Principal coupling | The bounded posterior-covariance mean adjustment is numbered and cited from the algorithm and component study. It leaves fitted targets and posterior variance unchanged. | Explicit clipping gives \(0\leq\delta_t(\theta)\leq\delta_{\max}\), and all gates must pass before the adjusted mean is active. |
| Component-only operator | The variance-normalized regional variant is confined to the component study and described by its mean-absolute-shift budget \(B_\delta\). | It is not presented as the principal LLMBO-MO operator and its budget is not misreported as a pointwise cap. |
| Hyperparameters | Table I contains the fixed budget, seeds, initialization composition, backend, and only the core coupling settings. | Simulator coefficients, fitted GP parameters, and low-level constants are not mixed into the optimization settings. |
| Hypervolume | HV is reported as the evaluation metric, using one common ideal/reference box for both methods within each parameterization. | Values are comparable within Chen2020 or Ecker2015, but not interpreted across the two parameterizations. |

## Audit conclusion

The numbered sequence now covers the problem definition, simulator objectives,
warm-start construction, ParEGO backbone, and proposed bounded coupling. Each
numbered group is referenced at least once, and no display equation is left
without a number. Changing the degradation proxy, scalar target, coupling
operator, or benchmark normalization would change the experiment and therefore
requires new runs; the present revision changes presentation only.
