"""Recreate the Chen2020 short-budget component-ablation boxplot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


PAPER_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = (
    PAPER_ROOT.parent
    / "BO_Multi_12_20"
    / "New_LLMBO"
    / "Ablation_Exp"
    / "experiment_records"
    / "ablation_4way_3seeds_10iter_deepseek_v3_codex_2026_05_17"
)
DEFAULT_OUTPUT_BASE = PAPER_ROOT / "figures" / "ablation_hv_box"
EXPECTED_KEYS = (
    "baseline",
    "baseline_warmstart",
    "baseline_llm_region",
    "llmbo_mo",
)
DISPLAY_LABELS = {
    "baseline": "No LLM",
    "baseline_warmstart": "+WarmStart",
    "baseline_llm_region": "+Region",
    "llmbo_mo": "LLMBO-MO",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_groups(source_root: Path) -> list[dict[str, Any]]:
    plot_manifest = source_root / "plot_manifest.json"
    groups = _load_json(plot_manifest).get("groups")
    if not isinstance(groups, list):
        raise ValueError(f"Missing groups in {plot_manifest}")
    keys = tuple(str(group.get("key")) for group in groups)
    if keys != EXPECTED_KEYS:
        raise ValueError(f"Unexpected ablation group order: {keys}")
    for group in groups:
        values = np.asarray(group.get("values", []), dtype=float)
        if values.shape != (3,) or not np.all(np.isfinite(values)):
            raise ValueError(f"Invalid values for {group.get('key')}")
    return groups


def make_figure(
    groups: list[dict[str, Any]], output_base: Path, dpi: int
) -> tuple[Path, Path]:
    labels = [DISPLAY_LABELS[str(group["key"])] for group in groups]
    colors = [str(group["color"]) for group in groups]
    data = [np.asarray(group["values"], dtype=float) for group in groups]

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 10,
            "axes.labelsize": 11,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    fig, ax = plt.subplots(figsize=(7.15, 4.2))
    positions = np.arange(1, len(data) + 1)
    box = ax.boxplot(
        data,
        positions=positions,
        widths=0.45,
        patch_artist=True,
        showfliers=False,
    )
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.18)
        patch.set_edgecolor("#222222")

    rng = np.random.default_rng(8409)
    for position, values, color in zip(positions, data, colors):
        offsets = rng.normal(0.0, 0.035, size=values.size)
        ax.scatter(
            position + offsets,
            values,
            s=42,
            color=color,
            edgecolor="#222222",
            linewidth=0.35,
            zorder=3,
        )

    ax.set_xticks(positions, labels=labels)
    ax.set_ylabel("HV")
    ax.grid(True, axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    fig.tight_layout()

    output_base.parent.mkdir(parents=True, exist_ok=True)
    png_path = output_base.with_suffix(".png")
    pdf_path = output_base.with_suffix(".pdf")
    fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    return png_path, pdf_path


def write_manifest(
    groups: list[dict[str, Any]], source_root: Path, png_path: Path, pdf_path: Path
) -> Path:
    payload = {
        "figure": "Chen2020 short-budget component ablation",
        "source": source_root.as_posix(),
        "display_labels": [DISPLAY_LABELS[key] for key in EXPECTED_KEYS],
        "groups": [
            {
                "key": group["key"],
                "display_label": DISPLAY_LABELS[str(group["key"])],
                "values": group["values"],
            }
            for group in groups
        ],
        "outputs": {
            "png": {"path": png_path.as_posix(), "sha256": _sha256(png_path)},
            "pdf": {"path": pdf_path.as_posix(), "sha256": _sha256(pdf_path)},
        },
    }
    path = png_path.with_name("ablation_hv_box_manifest.json")
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--output-base", type=Path, default=DEFAULT_OUTPUT_BASE)
    parser.add_argument("--dpi", type=int, default=400)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    groups = load_groups(args.source_root)
    png_path, pdf_path = make_figure(groups, args.output_base, args.dpi)
    manifest_path = write_manifest(groups, args.source_root, png_path, pdf_path)
    print(
        json.dumps(
            {
                "png": str(png_path),
                "pdf": str(pdf_path),
                "manifest": str(manifest_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
