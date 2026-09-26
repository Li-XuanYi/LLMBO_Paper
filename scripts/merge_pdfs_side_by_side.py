#!/usr/bin/env python3
"""Merge two PDFs side by side (horizontally) into one page.

Usage:
    python3 merge_pdfs_side_by_side.py left.pdf right.pdf output.pdf [left_scale] [right_scale] [gap_pt]

Each page is scaled by its factor (default 1.0) before merging; pages are
bottom-aligned so the bottoms of the two figures match.
"""
import sys

from pypdf import PdfReader, PdfWriter, Transformation


def merge(left_path, right_path, output_path,
          left_scale=1.4, right_scale=1.0, gap=0):
    left = PdfReader(left_path).pages[0]
    right = PdfReader(right_path).pages[0]

    lw = float(left.mediabox.width) * left_scale
    lh = float(left.mediabox.height) * left_scale
    rw = float(right.mediabox.width) * right_scale
    rh = float(right.mediabox.height) * right_scale

    total_w = lw + gap + rw
    total_h = max(lh, rh)

    out = PdfWriter()
    page = out.add_blank_page(width=total_w, height=total_h)

    page.merge_transformed_page(
        left, Transformation().scale(left_scale).translate(0, 0)
    )
    page.merge_transformed_page(
        right, Transformation().scale(right_scale).translate(lw + gap, 0)
    )

    with open(output_path, "wb") as f:
        out.write(f)
    print(f"Wrote {output_path} ({total_w:.1f} x {total_h:.1f} pt)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    left_s = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    right_s = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    gap = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
    merge(sys.argv[1], sys.argv[2], sys.argv[3], left_s, right_s, gap)

"""
example:
     python3 scripts/merge_pdfs_side_by_side.py figures/pareto_protocols_ae.pdf figures/charging_profiles.pdf output.pdf 1.5
"""
