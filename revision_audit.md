# Manuscript Revision Audit

## Final compiled structure

1. Introduction (including related work)
2. Fast-Charging Optimization Problem
3. Electrochemical--Thermal Simulation and Degradation Proxy
4. Proposed LLMBO-MO
5. Numerical Validation and Discussion
6. Conclusion

The manuscript now follows the reference paper's problem--model--method--results
sequence while retaining the IEEE Transactions two-column style.

## Evidence audit

- Chen2020: `0.3853 +/- 0.0094` to `0.3885 +/- 0.0088`, `+0.84%`, 3/5 paired wins.
- Ecker2015: `0.5540 +/- 0.0121` to `0.5660 +/- 0.0104`, `+2.18%`, 4/5 paired wins.
- These execution details remain in this internal audit only. The compiled paper removes seed identifiers, Wins, and batch-log terminology.
- Table II preserves the audited means, sample deviations, and improvements; the surrounding prose reports only the direction and modest scale of the effects.
- Table IV preserves the prompt result and Holm-adjusted `p = 0.0059`; its study-specific budget and independent-run count appear only in the note.
- The component and preprocessing analyses are interpreted as separate controlled comparisons without archive-style narration.
- The degradation objective is reported only in arbitrary proxy units; no measured capacity-fade, lifetime, hardware-safety, or cell-to-cell-generalization conclusion is made.

## Figure, table, and pagination audit

- Fig. 1 retains the original author-supplied problem-formulation artwork; only its LaTeX float wrapper is controlled.
- Fig. 2 retains the original author-supplied Draw.io workflow PDF without graphical modification.
- Fig. 3 remains a one-column top figure in Simulation Setup and states that no measurement enters the reported results.
- Fig. 4 retains the two-panel qualitative Pareto/trajectory interpretation and states its pooled visualization scope.
- The original Ecker2015 auxiliary panel is retained with a one-sentence caption that identifies its independent protocol and points to Table II for the principal comparison.
- The original Chen2020 component diagnostic panels are retained with a concise descriptive caption.
- The original objective-preprocessing PDF is restored unchanged.
- Tables I--IV contain settings, principal results, component results, and prompt results. Their captions describe the comparison purpose rather than execution details.
- The final PDF is 10 pages with natural body floats and balanced final reference columns.

## Build and visual QA

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: pass.
- Undefined citation/reference, multiply defined label, overfull box, and underfull box scan: pass.
- Stale-value scan for `+17.8%`, `0.4760`, and `0.5605`: pass.
- Compiled-source scan for Wins, paired wins, seed identifiers, and batch-log terminology: pass.
- Git status and SHA-256 inspection of every included raster/PDF figure asset: no figure asset was modified.
- All ten rendered pages were inspected for hierarchy, clipping, float order, figure legibility, and last-page balance.

## Remaining evidence gaps requiring new experiments

1. matched qEHVI/qNEHVI comparisons;
2. an identical-initial-database acquisition-guidance study;
3. a simultaneously executed four-arm component study;
4. a calibrated lifetime or measured capacity-fade endpoint;
5. physical replay under independently approved protection limits.
