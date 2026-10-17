"""Audit archived protocol and Pareto-set dominance without running simulations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def front(database: dict) -> np.ndarray:
    values = np.unique(np.asarray([
        row["objectives"] for row in database["observations"]
        if row.get("feasible", False) and np.isfinite(row["objectives"]).all()
    ], dtype=float), axis=0)
    keep = [not np.any(np.all(values <= point, axis=1)
                       & np.any(values < point, axis=1)) for point in values]
    return values[keep]


def coverage(source: np.ndarray, target: np.ndarray) -> int:
    dominates = (np.all(source[:, None, :] <= target[None, :, :], axis=2)
                 & np.any(source[:, None, :] < target[None, :, :], axis=2))
    return int(dominates.any(axis=0).sum())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paper = Path(__file__).resolve().parents[1]
    root = args.experiment_root.resolve()
    batch = root / "Compare_Exp/experiment_records/seed8409_llmbo_vs_parego_50iter/seed8409"
    selected = {}
    for method, index in (("llmbo_mo", 6), ("parego_matlab_reference", 51)):
        path = batch / method / "database.json"
        database = load(path)
        row = database["observations"][index]
        values = np.asarray(row["objectives"], dtype=float)
        selected[method] = {
            "source": str(path), "observation_number": index + 1,
            "zero_based_index": index, "iteration": row["iteration"],
            "theta": row["theta"], "objectives": row["objectives"],
            "feasible": row.get("feasible", False),
            "in_recomputed_front": bool(np.any(np.all(front(database) == values, axis=1))),
            "in_stored_front": index in database["pareto_indices"],
        }
    left = np.asarray(selected["llmbo_mo"]["objectives"])
    right = np.asarray(selected["parego_matlab_reference"]["objectives"])
    manifest = load(paper / "results/results_manifest.json")["chen2020"]
    rows = []
    for seed in range(8409, 8414):
        fronts, sources, hv = {}, {}, {}
        for method in ("llmbo_mo", "parego"):
            rel = (manifest[method]["sources"]["8409"] if seed == 8409 else
                   manifest[method]["sources"]["8410-8413"].replace("{seed}", str(seed)))
            path = root / rel.replace("summary.json", "database.json")
            fronts[method], sources[method] = front(load(path)), str(path)
            hv[method] = float(load(root / rel)["canonical_hv"])
        llmbo, parego = fronts["llmbo_mo"], fronts["parego"]
        rows.append({
            "seed": seed, "sources": sources,
            "llmbo_front_size": len(llmbo), "parego_front_size": len(parego),
            "parego_points_dominated_by_llmbo": coverage(llmbo, parego),
            "llmbo_points_dominated_by_parego": coverage(parego, llmbo),
            "archived_llmbo_hv": hv["llmbo_mo"],
            "archived_parego_hv": hv["parego"],
            "hv_agrees_with_paper_manifest": all(
                bool(np.isclose(hv[m], manifest[m]["values"][str(seed)], rtol=0, atol=1e-12))
                for m in ("llmbo_mo", "parego")),
        })
    llmbo_mean = float(np.mean([r["archived_llmbo_hv"] for r in rows]))
    parego_mean = float(np.mean([r["archived_parego_hv"] for r in rows]))
    result = {
        "scope": "Archived Chen2020 records; no new simulator or LLM calls",
        "objective_order": ["charging_time_s", "temperature_rise_K", "aging_indicator"],
        "all_objectives_minimized": True,
        "selected_protocols": selected,
        "selected_llmbo_strictly_better_in_all_objectives": bool(np.all(left < right)),
        "selected_pair_improvement_percent": ((right - left) / right * 100).tolist(),
        "five_seed_fronts": rows,
        "archived_mean_hv": {"llmbo_mo": llmbo_mean, "parego": parego_mean,
                             "relative_gain_percent": (llmbo_mean / parego_mean - 1) * 100},
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"selected_pair_strict_dominance": bool(np.all(left < right)),
                      "seed_count": len(rows), "mean_hv": result["archived_mean_hv"]}))


if __name__ == "__main__":
    main()
