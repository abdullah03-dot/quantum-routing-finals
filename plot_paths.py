# plot_paths.py (Enhanced Version for Publication-Quality Figure)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.collections import PatchCollection

# Node positions (row, col) → (x, y)
positions = {
    "N1": (0, 2), "N2": (1, 2), "N3": (2, 2),
    "N4": (0, 1), "N5": (1, 1), "N6": (2, 1),
    "N7": (0, 0), "N8": (1, 0), "N9": (2, 0)
}

# Paths from real experiments
paths = {
    "Shortest-path & Highest-fidelity\n(most common at 5% noise)": ["N1", "N2", "N3", "N6", "N9"],
    "Hybrid rule (ours)\n(discovered automatically)": ["N1", "N4", "N7", "N8", "N9"],
    "Theoretical optimal diagonal\n(rarely stable under noise)": ["N1", "N5", "N9"]
}

# Colorblind-safe palette (Okabe–Ito)
colors = {
    "Shortest": "#D55E00",
    "Hybrid": "#0072B2",
    "Diagonal": "#009E73"
}

# Assign colors to paths
path_colors = [
    colors["Shortest"],
    colors["Hybrid"],
    colors["Diagonal"]
]

# Line style & thickness
styles = ["-", "-", "--"]
widths = [4.5, 6.0, 4.2]
alphas = [0.95, 1.0, 0.85]

fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor("white")

# Title
plt.title(
    "Routing Paths Discovered in 3×3 Quantum Mesh\n"
    "(5% Depolarizing Noise, Double Purification, 60 Trials per Policy)",
    fontsize=20, fontweight="bold", pad=30
)

# Draw background mesh (faint)
for x in range(3):
    ax.axhline(x, color="gray", linestyle="--", linewidth=0.6, alpha=0.3)
    ax.axvline(x, color="gray", linestyle="--", linewidth=0.6, alpha=0.3)

# Draw nodes as uniform circles
patches = []
facecolors = []
edgecolors = []
linewidths = []

for node, (x, y) in positions.items():

    if node in ["N1", "N9"]:
        color = "#FEE191"   # gold
        edge = "black"
        lw = 2.8
    elif node == "N5":
        color = "#BBD7EA"   # highlighted middle
        edge = "black"
        lw = 2.8
    else:
        color = "#E5E5E5"   # light gray
        edge = "#444"
        lw = 1.8

    c = Circle((x, y), 0.22)
    patches.append(c)
    facecolors.append(color)
    edgecolors.append(edge)
    linewidths.append(lw)

    ax.text(
        x, y, node,
        ha="center", va="center",
        fontsize=15, fontweight="bold",
        zorder=10
    )

pc = PatchCollection(
    patches,
    facecolor=facecolors,
    edgecolor=edgecolors,
    linewidth=linewidths,
    zorder=5
)
ax.add_collection(pc)

# Draw path lines with arrows
for (label, path), col, sty, wid, alp in zip(paths.items(), path_colors, styles, widths, alphas):

    # Convert node list → coordinates
    coords = [(positions[n][0], positions[n][1]) for n in path]

    # Draw connecting lines
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    ax.plot(xs, ys, color=col, linestyle=sty, linewidth=wid,
            alpha=alp, zorder=2, label=label)

    # Add arrow between every consecutive pair
    for i in range(len(coords) - 1):
        (x1, y1), (x2, y2) = coords[i], coords[i+1]
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='-|>',  # clean arrow
            mutation_scale=30,
            linewidth=wid,
            color=col,
            alpha=alp,
            zorder=3
        )
        ax.add_patch(arrow)

# Final layout settings
ax.set_aspect("equal")
plt.xlim(-0.5, 2.5)
plt.ylim(-0.5, 2.5)
plt.axis("off")

# Legend
leg = plt.legend(
    fontsize=14,
    loc="center left",
    bbox_to_anchor=(-0.25, 0.5),  # shift leftward
    frameon=True,
    fancybox=True,
    shadow=True,
    borderpad=1.2
)


plt.tight_layout()
plt.savefig("quantum_routing_paths_enhanced.png", dpi=450, bbox_inches="tight")
plt.show()
