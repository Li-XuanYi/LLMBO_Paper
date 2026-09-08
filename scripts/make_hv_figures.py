"""Regenerate manuscript figures and traceable representative protocols.

No simulator or language-model calls are made here.  Every output is derived
from retained CSV tables, summary files, or observation databases supplied on
the command line.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from eimo_figure_style import EIMO_STYLE


COLORS = {
    "ParEGO": "#2878B5",
    "LLMBO-MO": "#D62728",
    "NSGA-II": "#E67E22",
    "DISK": "#2E8B57",
    "PIMD": "#7B2CBF",
    "Min-max": "#C51B2B",
    "Z-score": "#2864AD",
    "No normalization": "#7B2CBF",
}


def _read_csv(path: Path) -> list[dict[str, float]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {key: float(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 10,
            "axes.labelsize": 11,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.linewidth": 0.8,
            "grid.color": "#D0D0D0",
            "grid.alpha": 0.45,
        }
    )


def _save(fig: plt.Figure, output_dir: Path, stem: str, dpi: int = 400) -> list[str]:
    outputs: list[str] = []
    for suffix in ("pdf", "png"):
        path = output_dir / f"{stem}.{suffix}"
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        outputs.append(str(path))
    if dpi == 600:
        highres = output_dir / f"{stem}_600dpi.png"
        highres.write_bytes((output_dir / f"{stem}.png").read_bytes())
        outputs.append(str(highres))
    plt.close(fig)
    return outputs


def _band_line(
    ax: plt.Axes,
    x: np.ndarray,
    mean: np.ndarray,
    band: np.ndarray,
    *,
    label: str,
    marker: str,
    alpha: float = 0.16,
    linestyle: str = "-",
) -> None:
    color = COLORS[label]
    ax.fill_between(x, mean - band, mean + band, color=color, alpha=alpha, linewidth=0)
    ax.plot(
        x,
        mean,
        color=color,
        linewidth=2.0,
        linestyle=linestyle,
        marker=marker,
        markevery=7,
        markersize=4.5,
        label=label,
    )


@plt.rc_context(EIMO_STYLE)
def make_chen(rows: list[dict[str, float]], output_dir: Path) -> dict[str, Any]:
    x = np.asarray([row["eval_index"] for row in rows])
    fig, ax = plt.subplots(figsize=(7.15, 5.15))
    specs = (
        ("ParEGO", "parego_hv", "parego_plot_band", "s", 0.16),
        ("LLMBO-MO", "llambo_mo_hv", "llambo_mo_plot_band", "o", 0.16),
        ("NSGA-II", "nsga2_mean_hv", "nsga2_std_hv", "v", 0.11),
        ("DISK", "disk_mean_hv", "disk_std_hv", "^", 0.11),
        ("PIMD", "pimd_mean_hv", "pimd_std_hv", "D", 0.11),
    )
    for label, mean_key, band_key, marker, alpha in specs:
        _band_line(
            ax,
            x,
            np.asarray([row[mean_key] for row in rows]),
            np.asarray([row[band_key] for row in rows]),
            label=label,
            marker=marker,
            alpha=alpha,
        )
    ax.set_xlim(0, 56)
    ax.set_ylim(0.12, 0.40)
    ax.set_xlabel("Cumulative simulator evaluations")
    ax.set_ylabel("HV")
    ax.grid(True)
    ax.legend(loc="lower right", frameon=True, fancybox=False, edgecolor="#777777")
    fig.tight_layout(pad=0.45)
    return {"outputs": _save(fig, output_dir, "chen2020_hv_5way", dpi=600), "evaluations": 56}


@plt.rc_context(EIMO_STYLE)
def make_ecker(rows: list[dict[str, float]], output_dir: Path) -> dict[str, Any]:
    """Reproduce the supplied Ecker curve on its common manuscript HV scale."""
    x = np.asarray([row["eval_index"] for row in rows])
    display_scale = 0.3
    sample_correction = np.sqrt(5.0 / 4.0)
    parego_mean = display_scale * np.asarray([row["parego_mean_hv"] for row in rows])
    parego_sd = (
        display_scale
        * sample_correction
        * np.asarray([row["parego_raw_std_hv"] for row in rows])
    )
    llmbo_mean = display_scale * np.asarray([row["llmbo_mo_mean_hv"] for row in rows])
    llmbo_sd = (
        display_scale
        * sample_correction
        * np.asarray([row["llmbo_mo_raw_std_hv"] for row in rows])
    )

    fig, ax = plt.subplots(figsize=(7.15, 5.15))
    _band_line(ax, x, parego_mean, parego_sd, label="ParEGO", marker="s")
    _band_line(ax, x, llmbo_mean, llmbo_sd, label="LLMBO-MO", marker="o")
    ax.set_xlim(0, 56)
    ax.set_ylim(0.08, 0.60)
    ax.set_xlabel("Cumulative simulator evaluations")
    ax.set_ylabel("HV")
    ax.grid(True)
    ax.legend(loc="lower right", frameon=True, fancybox=False, edgecolor="#777777")
    fig.tight_layout(pad=0.45)

    return {
        "outputs": _save(fig, output_dir, "ecker2015_hv", dpi=600),
        "evaluations": 56,
        "seeds": 5,
        "uncertainty": "sample standard deviation",
        "display_scale": display_scale,
        "evaluation_30": {
            "parego_mean": float(parego_mean[29]),
            "llmbo_mo_mean": float(llmbo_mean[29]),
        },
        "evaluation_56": {
            "parego_mean": float(parego_mean[-1]),
            "parego_sample_sd": float(parego_sd[-1]),
            "llmbo_mo_mean": float(llmbo_mean[-1]),
            "llmbo_mo_sample_sd": float(llmbo_sd[-1]),
        },
    }


def make_normalization(rows: list[dict[str, float]], output_dir: Path) -> dict[str, Any]:
    x = np.asarray([row["evaluation"] for row in rows])
    fig, ax = plt.subplots(figsize=(7.15, 4.85))
    specs = (
        ("Min-max", "minmax_mean", "minmax_sample_sd", "o", "-"),
        ("Z-score", "zscore_mean", "zscore_sample_sd", "s", "--"),
        ("No normalization", "none_mean", "none_sample_sd", "^", "-."),
    )
    for label, mean_key, sd_key, marker, linestyle in specs:
        _band_line(
            ax,
            x,
            np.asarray([row[mean_key] for row in rows]),
            np.asarray([row[sd_key] for row in rows]),
            label=label,
            marker=marker,
            linestyle=linestyle,
            alpha=0.13,
        )
    ax.set_xlim(0, 56)
    ax.set_ylim(0.14, 0.45)
    ax.set_xlabel("Cumulative simulator evaluations")
    ax.set_ylabel("HV")
    ax.grid(True)
    ax.legend(loc="lower right", frameon=True, fancybox=False, edgecolor="#777777")
    fig.tight_layout(pad=0.45)
    return {
        "outputs": _save(fig, output_dir, "objective_normalization_hv"),
        "evaluations": 56,
        "seeds": 5,
        "uncertainty": "sample standard deviation",
        "evaluation_30": {
            "minmax": rows[29]["minmax_mean"],
            "zscore": rows[29]["zscore_mean"],
            "none": rows[29]["none_mean"],
        },
        "evaluation_56": {
            "minmax_mean": rows[-1]["minmax_mean"],
            "minmax_sample_sd": rows[-1]["minmax_sample_sd"],
            "zscore_mean": rows[-1]["zscore_mean"],
            "zscore_sample_sd": rows[-1]["zscore_sample_sd"],
            "none_mean": rows[-1]["none_mean"],
            "none_sample_sd": rows[-1]["none_sample_sd"],
        },
    }


def _project_root_from_report_manifest(path: Path) -> Path:
    for candidate in path.parents:
        if (candidate / "Compare_Exp").is_dir() and (candidate / "optimized_experiments").is_dir():
            return candidate
    raise RuntimeError(f"Cannot locate experiment project root from {path}")


def _portable_source(path: Path) -> str:
    """Keep provenance traceable without embedding a workstation-specific prefix."""
    resolved = path.resolve()
    for parent in resolved.parents:
        if parent.name == "New_LLMBO":
            return resolved.relative_to(parent).as_posix()
    return resolved.as_posix()


def _iteration_pareto_trace(summary_path: Path) -> tuple[np.ndarray, np.ndarray]:
    payload = _load_json(summary_path)
    by_iteration: dict[int, float] = {}
    for item in payload.get("hv_trace", []):
        by_iteration[int(item.get("iteration", 0))] = float(item.get("pareto_size", 0))
    if not by_iteration:
        raise ValueError(f"No hv_trace in {summary_path}")
    x = np.asarray(sorted(by_iteration), dtype=int)
    y = np.asarray([by_iteration[int(index)] for index in x], dtype=float)
    return x, y


def make_optimal_protocols(manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    metrics = manifest["metrics"]
    project_root = _project_root_from_report_manifest(manifest_path)

    def resolve_many(items: Iterable[str]) -> list[Path]:
        paths: list[Path] = []
        for item in items:
            path = Path(item)
            paths.append(path if path.is_absolute() else project_root / path)
        return paths

    source_map = {
        "LLMBO-MO": resolve_many(metrics["llmbo_sources"]),
        "ParEGO": resolve_many(metrics["parego_sources"]),
    }
    stacked: dict[str, dict[str, Any]] = {}
    for method, paths in source_map.items():
        traces: list[np.ndarray] = []
        x_ref: np.ndarray | None = None
        for path in paths:
            x, y = _iteration_pareto_trace(path)
            if x_ref is None:
                x_ref = x
            elif not np.array_equal(x_ref, x):
                raise ValueError(f"Iteration mismatch in {path}")
            traces.append(y)
        if x_ref is None:
            raise ValueError(f"No traces for {method}")
        values = np.vstack(traces)
        stacked[method] = {
            "x": x_ref,
            "mean": values.mean(axis=0),
            "population_sd": values.std(axis=0, ddof=0),
            "sources": [_portable_source(path) for path in paths],
        }

    fig, ax = plt.subplots(figsize=(7.15, 5.15))
    for method, marker in (("ParEGO", None), ("LLMBO-MO", None)):
        values = stacked[method]
        color = "#5AA354" if method == "ParEGO" else "#377EB8"
        mean = values["mean"]
        sd = values["population_sd"]
        ax.fill_between(values["x"], mean - sd, mean + sd, color=color, alpha=0.12, linewidth=0)
        ax.plot(values["x"], mean, color=color, linewidth=2.8, label=method)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 55)
    ax.set_xlabel("Number of iterations")
    ax.set_ylabel("Number of optimal charging protocols")
    ax.grid(True)
    ax.legend(loc="upper left", frameon=True, fancybox=False, edgecolor="#777777")
    fig.tight_layout(pad=0.45)

    return {
        "outputs": _save(fig, output_dir, "optimal_protocols_curve"),
        "iterations": 50,
        "seeds": 5,
        "uncertainty": "archived across-run standard deviation",
        "definition": "feasible Pareto-nondominated archive entries",
        "final_mean": {
            method: float(stacked[method]["mean"][-1]) for method in stacked
        },
        "sources": {method: values["sources"] for method, values in stacked.items()},
    }


def _parse_seed_database(spec: str) -> tuple[int, Path]:
    seed_text, separator, path_text = spec.partition("=")
    if not separator:
        raise ValueError(f"Expected SEED=PATH, got {spec}")
    return int(seed_text), Path(path_text)


def _nondominated_mask(values: np.ndarray) -> np.ndarray:
    keep = np.ones(values.shape[0], dtype=bool)
    for index, point in enumerate(values):
        dominates = np.all(values <= point, axis=1) & np.any(values < point, axis=1)
        dominates[index] = False
        if np.any(dominates):
            keep[index] = False
    return keep


def _select_arc_representatives(front: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(front, key=lambda record: record["objectives"][0])
    objective_array = np.asarray([record["objectives"] for record in ordered], dtype=float)
    minimum = objective_array.min(axis=0)
    span = np.maximum(objective_array.max(axis=0) - minimum, 1e-12)
    normalized = (objective_array - minimum) / span
    increments = np.linalg.norm(np.diff(normalized, axis=0), axis=1)
    cumulative = np.concatenate(([0.0], np.cumsum(increments)))
    if cumulative[-1] <= 0:
        raise ValueError("Degenerate nondominated front")
    cumulative /= cumulative[-1]

    selected_indices: list[int] = []
    for target in np.linspace(0.0, 1.0, 3):
        for candidate in np.argsort(np.abs(cumulative - target)):
            candidate_index = int(candidate)
            if candidate_index not in selected_indices:
                selected_indices.append(candidate_index)
                break
    selected = [ordered[index] for index in selected_indices]
    selected.sort(key=lambda record: record["objectives"][0])
    for label, record in zip("ABC", selected):
        record["label"] = label
    return selected


def _representative_annotation(selected: list[dict[str, Any]]) -> str:
    """Render the design vector of each starred representative as a text block.

    Times/DejaVu serif digits are tabular, so padding the numeric fields with
    plain spaces keeps the columns aligned without a monospace font.
    """
    lines = [
        r"        $I_1/I_2/I_3$ (A)        $\Delta s_1/\Delta s_2/\Delta s_3$"
    ]
    for record in selected:
        currents = "/".join(f"{value:.2f}" for value in record["theta"][:3])
        spans = "/".join(
            f"{value:.2f}"
            for value in (record["theta"][3], record["theta"][4], record["dsoc3"])
        )
        lines.append(f"  {record['label']}     {currents}       {spans}")
    return "\n".join(lines)


def _place_vertical_axis_title(fig: plt.Figure, ax: Any, text: str, fontsize: int) -> None:
    """Draw the vertical-axis title as an ordinary Text child of the axes.

    ``mpl_toolkits.mplot3d`` leaves axis titles out of the tight bounding box, so
    a title produced by ``set_zlabel`` is cropped away by
    ``savefig(bbox_inches="tight")`` whenever it lands outside the axes
    rectangle.  A Text artist is part of the layout, so it always survives.
    The anchor is measured from the drawn tick labels instead of being guessed.
    Persistent ``Tick`` artists carry pre-projection positions, so the axis
    tight bounding box is the only reliable source for that measurement.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    tick_box = ax.zaxis.get_tightbbox(renderer)
    axes_box = ax.get_window_extent(renderer)
    axis_is_left = tick_box.x0 + 0.5 * tick_box.width < axes_box.x0 + 0.5 * axes_box.width
    title_x = (
        tick_box.x0 - 0.035 * axes_box.width
        if axis_is_left
        else tick_box.x1 + 0.035 * axes_box.width
    )
    x_axes = ax.transAxes.inverted().transform((title_x, 0.0))[0]
    ax.text2D(
        x_axes,
        0.5,
        text,
        transform=ax.transAxes,
        rotation=90,
        ha="center",
        va="center",
        fontsize=fontsize,
    )


def make_pareto_protocols(
    database_specs: list[str], output_dir: Path, results_dir: Path
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    source_paths: dict[int, str] = {}
    for spec in database_specs:
        seed, path = _parse_seed_database(spec)
        portable_path = _portable_source(path)
        source_paths[seed] = portable_path
        payload = _load_json(path)
        for observation_index, observation in enumerate(payload.get("observations", []), start=1):
            if not bool(observation.get("feasible", False)):
                continue
            theta = [float(value) for value in observation["theta"]]
            objectives = [float(value) for value in observation["objectives"]]
            records.append(
                {
                    "seed": seed,
                    "observation_index": observation_index,
                    "theta": theta,
                    "objectives": objectives,
                    "source": observation.get("source"),
                    "database": portable_path,
                }
            )

    deduplicated: list[dict[str, Any]] = []
    seen: set[tuple[float, ...]] = set()
    for record in records:
        key = tuple(round(value, 10) for value in record["theta"] + record["objectives"])
        if key not in seen:
            seen.add(key)
            deduplicated.append(record)

    values = np.asarray([record["objectives"] for record in deduplicated], dtype=float)
    mask = _nondominated_mask(values)
    front = [record for record, retained in zip(deduplicated, mask) if bool(retained)]
    selected = _select_arc_representatives(front)

    for record in selected:
        theta = record["theta"]
        record["dsoc3"] = 0.8 - theta[3] - theta[4]
        record["feasible"] = True
        record["globally_nondominated"] = True
    _style()
    fig = plt.figure(figsize=(7.15, 6.30))
    ax = fig.add_subplot(111, projection="3d", computed_zorder=False)

    # Match the reference orientation: temperature lies on the base plane and
    # degradation is vertical, which exposes the bowed Pareto-front shape.
    # objectives 的存储顺序仍为 (charging time, temperature rise, degradation)。
    all_values = np.asarray([record["objectives"] for record in deduplicated], dtype=float)
    ax.scatter(                              # 空心点 → 范例式的实心薰衣草紫圆点
        all_values[:, 0],
        all_values[:, 1],
        all_values[:, 2],
        s=24,
        c="#8484CC",
        alpha=0.65,
        linewidths=0,
        label="LLMBO-MO",
        depthshade=False,
        zorder=1,
    )
    degradation_span = float(all_values[:, 2].max() - all_values[:, 2].min())
    for record in selected:
        time_value, temperature, degradation = record["objectives"]
        ax.scatter(
            [time_value],
            [temperature],
            [degradation],
            marker="*",
            s=400,                           # 星标加大，范例中很醒目
            c="#D62728",
            edgecolors="#9E1B1B",
            linewidths=0.6,
            depthshade=False,
            zorder=10,
        )
        ax.text(
            time_value,
            temperature,
            degradation + 0.045 * degradation_span,
            record["label"],
            fontsize=16,                     # 字母标签加大加粗，同范例
            fontweight="bold",
            color="black",
            zorder=11,
        )

    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.set_facecolor("#f2f2f2")        # 浅暖灰 pane，模仿范例底色
        pane.set_edgecolor("#D9D9D9")

    axis_label_size = 13                              # 与刻度字号一致，避免轴标题偏小
    ax.set_xlabel("Charging Time / s", labelpad=14, fontsize=axis_label_size)
    ax.set_ylabel("Temperature Rise / K", labelpad=14, fontsize=axis_label_size)
    ax.tick_params(labelsize=13, pad=5)               # 刻度字号加大
    ax.view_init(elev=20, azim=240)
    ax.grid(True)

    ax.text2D(
        0.005,
        0.995,
        _representative_annotation(selected),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=11,
        linespacing=1.55,
        bbox={
            "boxstyle": "round,pad=0.45",
            "facecolor": "white",
            "edgecolor": "#777777",
            "linewidth": 0.8,
        },
        zorder=12,
    )
    ax.legend(
        loc="upper right",
        fontsize=14,
        handlelength=1.0,
    )
    fig.tight_layout(pad=0.25)
    _place_vertical_axis_title(fig, ax, "Degradation / a.u.", axis_label_size)
    outputs = _save(fig, output_dir, "pareto_protocols_ae")


    results_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / "pareto_representatives.json"
    json_payload = {
        "selection_rule": (
            "Pool feasible observations, remove duplicates, retain the global minimization "
            "nondominated set, sort by charging time, normalize all objectives, and select "
            "the records nearest cumulative front-arc fractions 0, 0.50, and 1."
        ),
        "soc_target": 0.8,
        "source_databases": source_paths,
        "n_feasible_records": len(records),
        "n_unique_records": len(deduplicated),
        "n_global_nondominated": len(front),
        "representatives": selected,
    }
    json_path.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")

    csv_path = results_dir / "pareto_representatives.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "label",
                "seed",
                "observation_index",
                "I1_A",
                "I2_A",
                "I3_A",
                "dSOC1",
                "dSOC2",
                "dSOC3",
                "charging_time_s",
                "temperature_rise_K",
                "degradation_proxy_au",
            ]
        )
        for record in selected:
            theta = record["theta"]
            objectives = record["objectives"]
            writer.writerow(
                [
                    record["label"],
                    record["seed"],
                    record["observation_index"],
                    theta[0],
                    theta[1],
                    theta[2],
                    theta[3],
                    theta[4],
                    record["dsoc3"],
                    objectives[0],
                    objectives[1],
                    objectives[2],
                ]
            )

    return {
        "outputs": outputs,
        "results_json": str(json_path),
        "results_csv": str(csv_path),
        "seeds": sorted(source_paths),
        "n_global_nondominated": len(front),
        "labels": [record["label"] for record in selected],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chen-csv", type=Path, required=True)
    parser.add_argument("--ecker-csv", type=Path, required=True)
    parser.add_argument("--normalization-csv", type=Path, required=True)
    parser.add_argument("--optimal-manifest", type=Path, required=True)
    parser.add_argument("--pareto-database", action="append", default=[], required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("figures"))
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.results_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "metric_label": "HV",
        "new_simulator_runs": False,
        "new_llm_calls": False,
        "chen2020": make_chen(_read_csv(args.chen_csv), args.output_dir),
        "ecker2015": make_ecker(_read_csv(args.ecker_csv), args.output_dir),
        "objective_normalization": make_normalization(
            _read_csv(args.normalization_csv), args.output_dir
        ),
        "optimal_protocols": make_optimal_protocols(
            args.optimal_manifest, args.output_dir
        ),
        "pareto_representatives": make_pareto_protocols(
            args.pareto_database, args.output_dir, args.results_dir
        ),
        "sources": {
            "chen_csv": args.chen_csv.name,
            "ecker_csv": args.ecker_csv.name,
            "normalization_csv": args.normalization_csv.name,
            "optimal_manifest": args.optimal_manifest.name,
        },
    }
    (args.output_dir / "hv_figure_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
