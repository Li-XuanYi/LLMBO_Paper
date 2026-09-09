# LLMBO-MO Paper (IEEE TTE)

Canonical LaTeX source for the IEEE Transactions on Transportation
Electrification review manuscript.

## Structure

```text
main.tex                         Root document and shared macros
sections/experiment_values.tex  Single source of reported numerical values
sections/*.tex                  Manuscript sections and references
figures/                        Vector and raster figure assets
scripts/make_hv_figures.py      Deterministic HV figure generator
claim_evidence_matrix.md        Reviewer-facing claim/evidence audit
revision_audit.md               Reproducibility and presentation audit
```

The title block is anonymized for review. Replace `Anonymous Authors` with the
final author, affiliation, correspondence, and funding metadata before a
non-anonymous submission.

## Build

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

References are maintained as `\bibitem` entries in
`sections/references.tex`; no BibTeX or biber step is required.

## Experimental values and figures

Do not type result values independently into individual sections. Update
`sections/experiment_values.tex` and regenerate the manuscript so the
abstract, introduction, tables, and conclusion remain synchronized.

The HV figures are generated from archived curve CSV files:

```powershell
python scripts/make_hv_figures.py `
  --chen-csv <chen-five-way-curve.csv> `
  --ecker-csv <ecker-five-seed-curve.csv> `
  --normalization-csv <normalization-five-seed-curve.csv> `
  --optimal-manifest <optimal-protocol-source-manifest.json> `
  --pareto-database <seed=database.json> `
  --output-dir figures
```

`figures/hv_figure_manifest.json` records the sources used for the current
assets. The Chen figure intentionally mixes two visualization conventions:
LLMBO-MO and ParEGO use representative seed-8409 centers with proxy envelopes,
whereas NSGA-II, DISK, and PIMD use five-run mean/standard-deviation curves.
Formal final statistics are reported in the manuscript tables.
The same generator produces the Ecker2015, objective-preprocessing, optimal-
protocol-archive, and A--E Pareto figures.  The selected protocol records and
their seed/observation provenance are written to `results/`.

## Evidence boundary

The revision uses existing archives only; no new simulator or LLM calls were
made. The Chen five-seed summary combines compatible historical archives and
is descriptive. The manuscript does not claim matched qEHVI/qNEHVI results,
an independently isolated regional-coupling effect, calibrated capacity fade,
or physical-cell validation.
