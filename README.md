# LLMBO-MO Paper (IEEE TTE)

Modular LaTeX source, split for **multi-author collaboration**. The rule: one
person, one section file. Never edit `main.tex` in parallel.

## Layout

```
paper/
├── main.tex              # ROOT: preamble + title + \input. Rarely edited.
├── sections/
│   ├── abstract.tex      # Abstract + keywords
│   ├── introduction.tex  # Sec. I
│   ├── problem.tex       # Sec. II  Problem Formulation (CMOP)
│   ├── model.tex         # Sec. III Electrochemical-Thermal-Aging Model
│   ├── method.tex        # Sec. IV  Proposed LLMBO-MO Framework
│   ├── experiments.tex   # Sec. V   Experiments
│   ├── conclusion.tex    # Sec. VI  Conclusion
│   └── references.tex    # thebibliography (hand-written, no .bib)
├── figures/              # figure assets, e.g. fig_llambo_mo_framework.tex
├── IEEEtran.cls          # journal class (keep)
├── balance.sty           # column balancing (keep)
├── .gitignore            # ignores build artifacts
├── .context/             # non-paper material (notes, old drafts, PDFs)
└── .trash/               # abandoned drafts
```

Tables live inside their owning section file (each author edits their own
tables). Figures go in `figures/`; `\graphicspath{{figures/}}` is set in
`main.tex`, so reference them by filename only.

## Build

```bash
latexmk -pdf main.tex     # produces main.pdf
latexmk -c                # clean aux files
```

References are hand-written `\bibitem`s in `sections/references.tex` — **no
BibTeX/biber step needed**. To add a citation, append a `\bibitem{refN}` there
and cite with `\cite{refN}`.

## Collaboration rules

- Edit only your assigned `sections/*.tex`; leave `main.tex` alone unless adding
  a new section input or package.
- Keep `\label{...}` names stable — other sections `\ref{}` them
  (`sec:`, `eq:`, `tab:`, `alg:` prefixes).
- New shared math macros go in the `main.tex` preamble, not inline.

## `.context/`

Non-paper-body material kept for reference, out of the compile path:
`IEEE_TTE_Paper_Structure.tex/.pdf` (original monolithic source before the
split), `LLMBO_experiment_report.md`, `ppt_warmstart_llm_region_algorithm.md`,
`project_intro.md`, `source.md`, and the old `IEEE-LaTeX/` draft.

## `.trash/`

`main.tex` — the previous abandoned draft. Kept for safety; delete when sure.
