from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_heatmap(
        points,
        x_min,
        x_max,
        y_min,
        y_max,
        bins_x=26 * 5,
        bins_y=14 * 5,
        save_path: str | Path | None = None,
        show: bool = False,
        title: str = "Heatmap посещенных точек",
        vmin=0,
        vmax=None,
) -> None:
    """
    points: list[tuple[float, float]]
    """

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    heatmap, x_edges, y_edges = np.histogram2d(
        xs,
        ys,
        bins=[bins_x, bins_y],
        range=[[x_min, x_max], [y_min, y_max]],
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    image = ax.imshow(
        heatmap.T,
        origin="lower",
        extent=[x_min, x_max, y_min, y_max],
        aspect="auto",
        vmin=vmin,
        vmax=vmax,
    )

    fig.colorbar(image, ax=ax, label="Количество посещений")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=120, bbox_inches="tight")

    if show:
        plt.show()

    plt.close(fig)
