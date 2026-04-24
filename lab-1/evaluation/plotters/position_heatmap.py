import matplotlib.pyplot as plt
import numpy as np


def plot_heatmap(points, x_min, x_max, y_min, y_max, bins_x=26*5, bins_y=14*5):
    """
    points: list[tuple[float, float]]
    """

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    heatmap, x_edges, y_edges = np.histogram2d(
        xs,
        ys,
        bins=[bins_x, bins_y],
        range=[[x_min, x_max], [y_min, y_max]]
    )

    plt.figure(figsize=(10, 5))

    plt.imshow(
        heatmap.T,
        origin="lower",
        extent=[x_min, x_max, y_min, y_max],
        aspect="auto"
    )

    plt.colorbar(label="Количество посещений")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Heatmap посещённых точек")

    plt.show()