# Fig. 2 redesign specification (v4)

This specification applies the K-Dense `scientific-schematics` review criteria and the
`Academic Figure Prompt` accessibility rules. The final artwork is rendered deterministically
in TikZ so that arrow anchors, line weights, labels, and exact colours remain auditable.

## Colour and line semantics

- Numerical MOBO: Okabe--Ito Steel Blue `#0072B2`, solid border.
- LLM guidance: Okabe--Ito Vermillion `#D55E00`, dashed arrows.
- Physical simulator: Okabe--Ito Bluish Green `#009E73`, solid border.
- Evaluated data and protocol domain: neutral Charcoal `#333333` / grey.
- Conditioning and constraint inputs: neutral grey dotted arrows.
- Main evaluated-data flow: Charcoal solid arrows.
- White is the dominant fill; only the MOBO group uses a faint blue `#F2F8FB` background.

The palette is colour-vision-deficiency-safe and uses redundant line styles, shapes, direct
labels, and arrow directions so the diagram remains interpretable in grayscale.

```text
Create a minimal publication-quality scientific workflow diagram for an IEEE Transactions paper.
Subject: LLMBO-MO for multiobjective battery fast-charging protocol design. Use one dominant
left-to-right numerical loop and one subordinate knowledge layer above it.

The solid main loop is:
evaluated database D_t and Pareto archive P_t → select weight and scalarize g_t → GP surrogate
(mu_t, sigma_t) → maximize EI_t → battery simulator → simulator-evaluated objectives and
feasibility → update D and P.

The protocol domain Theta_proto supplies prompt context to the LLM and the search domain to the
numerical optimizer through grey dotted arrows whose arrowheads point toward their consumers.

The LLM has exactly two bounded interfaces:
1. A dashed vermillion arrow labelled "screened initial protocols" must terminate with a downward
   arrowhead at the battery simulator. It must never point directly to D_t or P_t.
2. A grey dotted arrow from the numerical MOBO state to the LLM is labelled "w^(t) + BO state".
   A separate dashed vermillion output labelled "admissible EI restarts (t <= T_L)" must terminate
   with a downward arrowhead at the EI maximizer.

Every connector must have an unambiguous source and target. No bidirectional arrows, connector
crossings, decorative arrows, gradients, shadows, pseudo-3D, legends, or warning boxes. All labels
must remain readable at IEEE double-column width and the vector figure must remain clear in grey.
```
