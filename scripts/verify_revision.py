"""Verify manuscript-facing values and database-backed Pareto representatives."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def macros() -> dict[str, str]:
    text = (ROOT / "sections" / "experiment_values.tex").read_text(encoding="utf-8")
    return dict(re.findall(r"\\newcommand\{\\([^}]+)\}\{([^}]*)\}", text))


def assert_close(actual: float, expected: float, tolerance: float = 5e-10) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance):
        raise AssertionError(f"{actual} != {expected}")


def nondominated_mask(values: np.ndarray) -> np.ndarray:
    keep = np.ones(values.shape[0], dtype=bool)
    for index, point in enumerate(values):
        dominates = np.all(values <= point, axis=1) & np.any(values < point, axis=1)
        dominates[index] = False
        keep[index] = not np.any(dominates)
    return keep


def verify_macros() -> None:
    values = macros()
    expected = {
        "EckerMidParEGO": "0.4333",
        "EckerMidLLMBO": "0.5559",
        "EckerMidGain": "28.3\\%",
        "EckerParEGOMean": "0.4760",
        "EckerParEGOStd": "0.0039",
        "EckerLLMBOMean": "0.5605",
        "EckerLLMBOStd": "0.0008",
        "EckerFinalGain": "17.8\\%",
        "NormMinMaxMean": "0.4146",
        "NormMinMaxStd": "0.0067",
        "NormZScoreMean": "0.4122",
        "NormZScoreStd": "0.0078",
        "NormNoneMean": "0.3826",
        "NormNoneStd": "0.0358",
        "OptimalLLMBOFinal": "49.4",
        "OptimalParEGOFinal": "45.8",
    }
    for name, expected_value in expected.items():
        if values.get(name) != expected_value:
            raise AssertionError(f"Macro {name}: {values.get(name)!r} != {expected_value!r}")


def verify_figure_manifest() -> None:
    manifest = load_json(ROOT / "figures" / "hv_figure_manifest.json")
    assert manifest["metric_label"] == "HV"
    assert manifest["new_simulator_runs"] is False
    assert manifest["new_llm_calls"] is False
    ecker = manifest["ecker2015"]
    assert_close(ecker["evaluation_30"]["parego_mean"], 0.4332816479)
    assert_close(ecker["evaluation_30"]["llmbo_mo_mean"], 0.5558822732)
    assert_close(ecker["evaluation_56"]["parego_mean"], 0.4759688093)
    assert_close(ecker["evaluation_56"]["llmbo_mo_mean"], 0.5605251670)
    normalization = manifest["objective_normalization"]["evaluation_56"]
    assert_close(normalization["minmax_mean"], 0.4146460929)
    assert_close(normalization["zscore_mean"], 0.4121532055)
    assert_close(normalization["none_mean"], 0.3825539222)
    optimal = manifest["optimal_protocols"]
    assert optimal["iterations"] == 50 and optimal["seeds"] == 5
    assert_close(optimal["final_mean"]["LLMBO-MO"], 49.4)
    assert_close(optimal["final_mean"]["ParEGO"], 45.8)


def verify_representatives(experiment_root: Path) -> None:
    result = load_json(ROOT / "results" / "pareto_representatives.json")
    representatives = result["representatives"]
    assert [item["label"] for item in representatives] == list("ABCDE")

    pooled: list[tuple[list[float], list[float]]] = []
    for seed_text, relative_path in result["source_databases"].items():
        database = load_json(experiment_root / relative_path)
        for observation in database["observations"]:
            if observation.get("feasible", False):
                pooled.append((observation["theta"], observation["objectives"]))

        selected_for_seed = [item for item in representatives if item["seed"] == int(seed_text)]
        for item in selected_for_seed:
            observation = database["observations"][item["observation_index"] - 1]
            assert observation.get("feasible", False)
            assert np.allclose(observation["theta"], item["theta"], atol=1e-12, rtol=0)
            assert np.allclose(observation["objectives"], item["objectives"], atol=1e-12, rtol=0)

    unique: list[tuple[list[float], list[float]]] = []
    seen: set[tuple[float, ...]] = set()
    for theta, objectives in pooled:
        key = tuple(round(float(value), 10) for value in theta + objectives)
        if key not in seen:
            seen.add(key)
            unique.append((theta, objectives))
    values = np.asarray([objectives for _, objectives in unique], dtype=float)
    front_values = values[nondominated_mask(values)]

    for item in representatives:
        theta = np.asarray(item["theta"], dtype=float)
        dsoc = np.asarray([theta[3], theta[4], item["dsoc3"]], dtype=float)
        assert np.all((theta[:3] >= 2.0) & (theta[:3] <= 6.0))
        assert np.all(dsoc >= 0.1 - 1e-10)
        assert_close(float(dsoc.sum()), 0.8, tolerance=1e-9)
        objective = np.asarray(item["objectives"], dtype=float)
        if not np.any(np.all(np.isclose(front_values, objective, atol=1e-12, rtol=0), axis=1)):
            raise AssertionError(f"Representative {item['label']} is not globally nondominated")

    assert len(pooled) == result["n_feasible_records"] == 280
    assert len(unique) == result["n_unique_records"] == 254
    assert len(front_values) == result["n_global_nondominated"] == 158


def verify_terms() -> None:
    forbidden = re.compile(r"\b(?:sHV|nHV|wins?)\b", re.IGNORECASE)
    manuscript_paths = [ROOT / "main.tex"]
    manuscript_paths.extend((ROOT / "sections").glob("*.tex"))
    manuscript_paths.extend((ROOT / "figures").glob("*.tex"))
    for path in manuscript_paths:
        match = forbidden.search(path.read_text(encoding="utf-8"))
        if match:
            raise AssertionError(f"Forbidden result term {match.group(0)!r} in {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-root", required=True, type=Path)
    args = parser.parse_args()
    verify_macros()
    verify_figure_manifest()
    verify_representatives(args.experiment_root)
    verify_terms()
    print("Revision verification passed.")


if __name__ == "__main__":
    main()
