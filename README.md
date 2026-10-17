# LLMBO-MO Paper (IEEE TII)

Anonymous Regular Paper for initial submission to **IEEE Transactions on
Industrial Informatics**. The current manuscript is based on remote revision
`28faba1` from `origin/codex/tte-revision-v2`, including its real-cell validation.

## Canonical source and build

```text
main.tex                         Repository-root build entry
LLMBO_MO/IEEE_TII/main.tex       Canonical, consolidated manuscript
LLMBO_MO/IEEE_TII/figures/       Current figure assets
LLMBO_MO/IEEE_TII/IEEEtran.cls   IEEE Transactions class
submission/TII_checklist.md      Submission requirements and validation notes
output/pdf/TII_anonymous.pdf     Generated review PDF
```

Build from the repository root:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

This produces `main.pdf`. Building directly inside `LLMBO_MO/IEEE_TII/` is
also supported. The consolidated manuscript includes its sections, numerical
macros, and `thebibliography`; no BibTeX or biber step is required.

**Edit `LLMBO_MO/IEEE_TII/main.tex`.** The split files in `sections/` and
`LLMBO_MO/IEEE_TII/sections/`, and the root-level figure assets, are historical
working copies and are not inputs to the current manuscript. The former
`LLMBO_MO/IEEE_TTE/` directory has been renamed to `IEEE_TII`.

## Review format

- IEEEtran journal format, 10 pt, two columns, US Letter.
- Initial Regular Paper: at most 10 pages, including figures and references.
- Anonymous title block and running heads; empty PDF Author metadata.
- No author names, affiliations, e-mails, ORCIDs, acknowledgments, funding
  identifiers, biographies, or author photographs in the review manuscript.
- Existing self-citations remain ordinary third-person references.
- No Note to Practitioners. A cover letter is optional and must remain separate
  from the anonymous manuscript.

Author details, institutional primary e-mails, and ORCIDs must be supplied in
the submission system. Consult `submission/TII_checklist.md` and the official
guidelines before uploading.

## Evidence and editing boundary

The format conversion preserves the latest methods, equations, figures,
tables, references, and real-cell results. The abstract is shortened to fit
within 250 words, keywords are alphabetized, and the section roadmap now
includes real-cell validation. The current real-cell section includes an
experimental-platform photograph. No new simulator, LLM optimization, or hardware experiments
are performed by this conversion. The aging objective remains a
simulation-based relative indicator; real-cell validation covers charging
time, voltage, and temperature response.

AI assistance in this conversion is limited to manuscript formatting,
abstract editing, build-entry cleanup, and verification. The authors should
review the changes and determine any disclosure required by the journal.

The latest pagination repair removes a fixed reference break and produces
nine pages. See `submission/simulation_dominance_audit.md` for the subsequent
source-data audit of protocol dominance and the unresolved Chen2020 mean-HV
reporting mismatch.

Six TTE references have subsequently been replaced with verified TII papers.
The corresponding related-work descriptions now match the cited methods;
all 28 references retain their citation keys and order. The replacement
mapping and DOI evidence are in `submission/TII_reference_replacement_audit.md`.
