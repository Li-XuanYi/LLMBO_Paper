"""Replay Pareto representatives A--C and plot their charging trajectories.

The representative decision vectors and archived objectives are read from
``results/pareto_representatives.json``.  Trajectories are regenerated with the
same Chen2020 ``PyBaMMSimulator`` used by the optimization code; no synthetic
or interpolated profiles are introduced.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from eimo_figure_style import EIMO_STYLE


PAPER_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIMULATOR_ROOT = PAPER_ROOT.parent / "BO_Multi_12_20" / "New_LLMBO"


@dataclass(frozen=True)
class Protocol:
    label: str
    theta: tuple[float, float, float, float, float]
    archived_objectives: tuple[float, float, float]
    color: str
    linestyle: str


LINE_STYLES = {
    "A": ("#D55E00", "-"),
    "B": ("#0072B2", "--"),
    "C": ("#009E73", "-."),
}


def _load_protocols(path: Path) -> tuple[Protocol, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    representatives = payload.get("representatives", [])
    labels = [record.get("label") for record in representatives]
    if labels != list("ABC"):
        raise ValueError(f"Expected Pareto representatives A, B, C; found {labels}")

    protocols = []
    for record in representatives:
        label = str(record["label"])
        theta = tuple(float(value) for value in record["theta"])
        objectives = tuple(float(value) for value in record["objectives"])
        if len(theta) != 5 or len(objectives) != 3:
            raise ValueError(f"Malformed representative {label}")
        color, linestyle = LINE_STYLES[label]
        protocols.append(
            Protocol(
                label=label,
                theta=theta,
                archived_objectives=objectives,
                color=color,
                linestyle=linestyle,
            )
        )
    return tuple(protocols)


def _replay_protocols(
    protocols: tuple[Protocol, ...], simulator_root: Path
) -> dict[str, dict[str, np.ndarray]]:
    if not (simulator_root / "pybamm_simulator.py").is_file():
        raise FileNotFoundError(
            f"PyBaMMSimulator source is missing from {simulator_root}"
        )
    sys.path.insert(0, str(simulator_root))
    from pybamm_simulator import PyBaMMSimulator

    simulator = PyBaMMSimulator(param_set="Chen2020", aging_mode="empirical")
    profiles: dict[str, dict[str, np.ndarray]] = {}
    for protocol in protocols:
        result = simulator.evaluate(np.asarray(protocol.theta, dtype=float))
        if not bool(result.get("feasible", False)):
            raise RuntimeError(
                f"Simulation failed for protocol {protocol.label}: "
                f"{result.get('violation', 'unknown error')}"
            )

        objectives = np.asarray(result["raw_objectives"], dtype=float)
        archived = np.asarray(protocol.archived_objectives, dtype=float)
        if not np.allclose(objectives, archived, rtol=1e-7, atol=1e-7):
            raise RuntimeError(
                f"Protocol {protocol.label} replay does not match its archived "
                f"objectives: replayed={objectives.tolist()}, "
                f"archived={archived.tolist()}"
            )

        trajectories = result.get("trajectories")
        if not isinstance(trajectories, Mapping):
            raise RuntimeError(f"Protocol {protocol.label} returned no trajectories")
        profile = {
            "time_s": np.asarray(trajectories["time"], dtype=float),
            "voltage_v": np.asarray(trajectories["V"], dtype=float),
            "temperature_k": np.asarray(trajectories["T"], dtype=float),
            "current_a": np.asarray(trajectories["I"], dtype=float),
            "soc": np.asarray(trajectories["SOC"], dtype=float),
            "objectives": objectives,
        }
        lengths = {
            array.size for key, array in profile.items() if key != "objectives"
        }
        if len(lengths) != 1 or next(iter(lengths), 0) < 2:
            raise RuntimeError(f"Protocol {protocol.label} trajectories are misaligned")
        if not all(np.all(np.isfinite(array)) for array in profile.values()):
            raise RuntimeError(f"Protocol {protocol.label} contains non-finite data")
        profiles[protocol.label] = profile
    return profiles


def _configure_style() -> None:
    plt.rcParams.update(EIMO_STYLE)
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 16.0,
            "axes.labelsize": 17.0,
            "legend.fontsize": 16.0,
            "xtick.labelsize": 15.0,
            "ytick.labelsize": 15.0,
            "axes.linewidth": 0.75,
            "lines.linewidth": 1.55,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def _plot_profiles(
    protocols: tuple[Protocol, ...],
    profiles: Mapping[str, Mapping[str, np.ndarray]],
    output_dir: Path,
    dpi: int,
) -> tuple[Path, Path]:
    _configure_style()
    fig, axes = plt.subplots(2, 2, figsize=(7.15, 5.75))
    voltage_ax, temperature_ax, current_ax, soc_ax = axes.ravel()

    for protocol in protocols:
        profile = profiles[protocol.label]
        time_s = profile["time_s"]
        plot_kwargs = {
            "color": protocol.color,
            "linestyle": protocol.linestyle,
            "label": f"Protocol {protocol.label}",
            "solid_capstyle": "round",
        }
        voltage_ax.plot(time_s, profile["voltage_v"], **plot_kwargs)
        temperature_ax.plot(time_s, profile["temperature_k"], **plot_kwargs)
        current_ax.step(
            time_s,
            profile["current_a"],
            where="post",
            color=protocol.color,
            linestyle=protocol.linestyle,
            label=f"Protocol {protocol.label}",
        )
        soc_ax.plot(time_s, profile["soc"], **plot_kwargs)

    max_time = max(float(profile["time_s"][-1]) for profile in profiles.values())
    x_max = float(np.ceil(max_time / 500.0) * 500.0)
    x_ticks = np.arange(0.0, x_max + 1.0, 2000.0)
    panels = (
        (voltage_ax, "Voltage / V", "(a)"),
        (temperature_ax, "Temperature / K", "(b)"),
        (current_ax, "Input Current / A", "(c)"),
        (soc_ax, "State of Charge", "(d)"),
    )
    for axis, ylabel, panel_label in panels:
        axis.set_xlim(0.0, x_max)
        axis.set_xticks(x_ticks)
        axis.set_xlabel("Time / s")
        axis.set_ylabel(ylabel)
        axis.grid(True, color="#D9D9D9", linewidth=0.55, alpha=0.55)
        axis.tick_params(direction="in", length=3.0, width=0.7)
        axis.text(
            0.5,
            -0.38,
            panel_label,
            transform=axis.transAxes,
            ha="center",
            va="top",
            fontsize=16.0,
        )

    voltage_ax.set_ylim(2.7, 4.4)
    voltage_ax.set_yticks([3.0, 3.5, 4.0])
    voltage_ax.axhline(
        4.3,
        color="#D62728",
        linestyle=(0, (2, 2)),
        linewidth=0.85,
        alpha=0.8,
        zorder=0,
    )
    temperature_values = np.concatenate(
        [profile["temperature_k"] for profile in profiles.values()]
    )
    temperature_ax.set_ylim(
        2.0 * np.floor(float(temperature_values.min()) / 2.0),
        2.0 * np.ceil((float(temperature_values.max()) + 0.4) / 2.0),
    )
    temperature_ax.set_yticks(np.arange(*temperature_ax.get_ylim(), 2.0))
    current_ax.set_ylim(1.5, 6.5)
    soc_ax.set_ylim(0.0, 0.85)
    soc_ax.set_yticks(np.arange(0.0, 0.81, 0.2))
    handles, labels = voltage_ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.54, 1.0),
               ncol=3, frameon=False, handlelength=1.8, columnspacing=1.1)

    fig.subplots_adjust(
        left=0.12,
        right=0.985,
        bottom=0.15,
        top=0.90,
        wspace=0.53,
        hspace=0.80,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / "abc_charging_profiles.pdf"
    png_path = output_dir / "abc_charging_profiles.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return pdf_path, png_path


def _write_profiles(
    protocols: tuple[Protocol, ...],
    profiles: Mapping[str, Mapping[str, np.ndarray]],
    output_path: Path,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "battery_parameter_set": "Chen2020",
        "simulator": "PyBaMMSimulator (SPMe, lumped thermal)",
        "aging_mode": "empirical",
        "protocols": {},
    }
    for protocol in protocols:
        profile = profiles[protocol.label]
        payload["protocols"][protocol.label] = {
            "theta": list(protocol.theta),
            "archived_objectives": list(protocol.archived_objectives),
            "replayed_objectives": profile["objectives"].tolist(),
            "time_s": profile["time_s"].tolist(),
            "voltage_v": profile["voltage_v"].tolist(),
            "temperature_k": profile["temperature_k"].tolist(),
            "current_a": profile["current_a"].tolist(),
            "soc": profile["soc"].tolist(),
        }
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replay Pareto representatives A--C and plot V(t), T(t), I(t), and SOC(t)."
    )
    parser.add_argument(
        "--representatives",
        type=Path,
        default=PAPER_ROOT / "results" / "pareto_representatives.json",
    )
    parser.add_argument(
        "--simulator-root", type=Path, default=DEFAULT_SIMULATOR_ROOT
    )
    parser.add_argument(
        "--output-dir", type=Path, default=PAPER_ROOT / "figures"
    )
    parser.add_argument(
        "--profiles-json",
        type=Path,
        default=PAPER_ROOT / "results" / "abc_charging_profiles.json",
    )
    parser.add_argument("--dpi", type=int, default=400)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    protocols = _load_protocols(args.representatives)
    profiles = _replay_protocols(protocols, args.simulator_root)
    pdf_path, png_path = _plot_profiles(
        protocols, profiles, args.output_dir, dpi=args.dpi
    )
    profiles_path = _write_profiles(protocols, profiles, args.profiles_json)
    print(
        json.dumps(
            {
                "pdf": str(pdf_path),
                "png": str(png_path),
                "profiles": str(profiles_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
