"""Regenerate Figures 3, 4, 5 and 7 from retained data, without simulations."""

from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

import make_hv_figures as hv
import make_ablation_hv_box as ablation
import make_abc_charging_profiles as charging


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", type=Path,
                        default=ROOT.parent / "BO_Multi_12_20" / "New_LLMBO")
    args = parser.parse_args()
    output = ROOT / "figures"
    manifest = json.loads((ROOT / "results/results_manifest.json").read_text(encoding="utf-8"))
    chen = args.experiment_root / manifest["chen2020"]["displayed_figure"]["source"]
    ecker = args.experiment_root / manifest["ecker2015"]["source"]
    ablation_root = args.experiment_root / ablation.DEFAULT_SOURCE_ROOT.relative_to(
        ROOT.parent / "BO_Multi_12_20" / "New_LLMBO")
    profiles_path = ROOT / "results/abc_charging_profiles.json"
    sources = [chen, ecker, ablation_root / "plot_manifest.json", profiles_path,
               ROOT / "results/pareto_representatives.json"]
    source_hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}

    results = {"Fig3": hv.make_chen(hv._read_csv(chen), output),
               "Fig4": hv.make_ecker(hv._read_csv(ecker), output)}
    groups = ablation.load_groups(ablation_root)
    png, pdf = ablation.make_figure(groups, output / "ablation_hv_box", dpi=600)
    ablation.write_manifest(groups, ablation_root, png, pdf)
    results["Fig5"] = {"outputs": [str(pdf), str(png)]}

    protocols = charging._load_protocols(ROOT / "results/pareto_representatives.json")
    cached = json.loads(profiles_path.read_text(encoding="utf-8"))["protocols"]
    fields = ("time_s", "voltage_v", "temperature_k", "current_a", "soc")
    profiles = {}
    for protocol in protocols:
        record = cached[protocol.label]
        np.testing.assert_allclose(record["theta"], protocol.theta, rtol=0, atol=0)
        np.testing.assert_allclose(record["archived_objectives"],
                                   protocol.archived_objectives, rtol=0, atol=0)
        profiles[protocol.label] = {key: np.asarray(record[key], dtype=float) for key in fields}
    pdf, png = charging._plot_profiles(protocols, profiles, output, dpi=600)
    results["Fig7"] = {"outputs": [str(pdf), str(png)]}
    for path in sources:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source_hashes[str(path)]
    audit = {"style": "EIMO-like Times New Roman; enlarged single-column typography",
             "new_simulations": False, "source_sha256": source_hashes, "figures": results}
    (output / "eimo_style_manifest.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print("Regenerated Figures 3, 4, 5 and 7; source data hashes unchanged.")


if __name__ == "__main__":
    main()
