# TII initial-submission checklist

Target: IEEE Transactions on Industrial Informatics, Regular Paper,
anonymous initial submission. Requirements checked on 2026-10-17.

## Sources

- [TII official author information](https://www.ieee-ies.org/pubs/transactions-on-industrial-informatics)
- [IES-hosted TII manuscript checklist](https://www.ieee-ies.org/pubs/jestie/17-publications/tii)
- [IES Periodicals Editorial Policy and Guidelines](https://www.ieee-ies.org/images/files/publications/guidelines/IES_Periodicals_Policy_Guidelines.pdf)

The official website rejected direct page retrieval during this check;
the searchable text of the IES-hosted checklist and policy PDF confirmed
the 10-page cap, double-column format, author anonymization, 40 MB maximum,
institutional primary e-mails, and optional cover letter. The requested
250-word abstract ceiling is used as a conservative IEEE formatting target.

## Manuscript

- [x] Latest remote revision `28faba1`, including real-cell results, is the base.
- [x] IEEEtran journal class with 10 pt type and standard two-column layout.
- [x] Author block, affiliations, e-mails, and ORCID links removed.
- [x] Running heads and PDF metadata contain no author identity.
- [x] No acknowledgments, funding identifiers, biographies, author photos,
  or author-linked code repositories in the compiled manuscript.
- [x] Self-citations retained in third-person form.
- [x] No Note to Practitioners in the manuscript.
- [x] Cover letter remains separate; none is required for this format conversion.
- [x] Abstract shortened to fewer than 250 words while retaining simulation
  and real-cell findings.

## Build verification

- [x] Root and canonical-directory builds both pass `latexmk -pdf` and produce
  identical manuscript text.
- [x] Current review PDF: **9 pages**, US Letter, **34,918,388 bytes** (34.92 MB).
- [x] Abstract: **205 words** after treating LaTeX nonbreaking spaces as spaces.
- [x] All fonts embedded; no overfull boxes, undefined references, or undefined
  citations in the final build.
- [x] PDF Author metadata is empty. No author identities, ORCID links, mailto
  links, or author-linked repository URLs found in the extracted review PDF.
- [x] All 28 bibliography entries and all equation, table, and figure labels
  retained. The latest pagination repair removes only the fixed reference
  break and retains the manuscript content present before that repair.
- [x] All 23 relocated assets and historical source snapshots are byte-for-byte
  unchanged; current scientific figures and real-cell measurements are preserved.
- [x] Updated pages 8 and 9 rendered and inspected; no clipping or overlapping
  content. References now flow naturally through page 9, including entries
  21-28; no forced reference break remains.
- [x] Six TTE references replaced with verified TII publications. Crossref
  metadata and BibTeX validation pass with zero errors, warnings, or duplicates;
  all 28 citation keys and numbering relationships are retained.
- [x] After the reference update, all nine pages rendered and inspected;
  bibliography and corresponding related-work sentences agree with the new
  papers. See `TII_reference_replacement_audit.md` for the detailed mapping.

Scientific claim audit: `simulation_dominance_audit.md` confirms dominance
for the selected protocol pair, but not for the complete Pareto sets. It also
identifies an unresolved mismatch between the current Chen2020 mean-HV claim
and the five source archives. The pagination repair does not change those claims.

Generated deliverable: `output/pdf/TII_anonymous.pdf`. Build outputs are
ignored by Git; source and submission notes remain in the working tree.

## Submission-system items

- [ ] Enter the full author list and affiliations outside the anonymous PDF.
- [ ] Supply each author's ORCID and institutional primary e-mail.
- [ ] Confirm all authors' approval and exclusive submission status.
- [ ] Review the rendered manuscript and the existing experimental figures.
- [ ] Submit through the [IEEE TII Author Portal](https://ieee.atyponrex.com/journal/tii).

A response letter is mandatory for a revision or resubmission. A cover
letter is optional under the IES policy and must not be merged with the
anonymous manuscript. This checklist does not submit the paper.
