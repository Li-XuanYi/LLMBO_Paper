"""EIMO-like typography for figures placed at IEEE single-column width.

These sizes target a 7.15-inch source canvas scaled to a 3.5-inch column:
axis titles are about 9 pt and ticks/legends about 8 pt in the manuscript.
"""

EIMO_STYLE = {
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "mathtext.fontset": "stix",
    "font.size": 16,
    "axes.labelsize": 18,
    "legend.fontsize": 16,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#999999",
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "grid.color": "#D9D9D9",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.45,
    "legend.framealpha": 1.0,
    "legend.edgecolor": "#AAAAAA",
    "legend.fancybox": False,
    "legend.borderpad": 0.3,
    "legend.labelspacing": 0.25,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
}
