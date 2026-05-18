import matplotlib.pyplot as plt
import numpy as np


def smooth(x, k=20):
    """"""
    if len(x) < k:
        return x

    return np.convolve(x, np.ones(k) / k, mode="valid")


def plot_winrate(winrates, save_path=None):
    """"""
    epochs = range(1, len(winrates) + 1)

    plt.figure(figsize=(8, 4))
    plt.plot(epochs, winrates, alpha=0.4)

    smoothed = smooth(winrates, k=20)

    if len(smoothed) > 0:
        smooth_epochs = range(20, 20 + len(smoothed))
        plt.plot(smooth_epochs, smoothed, linewidth=2)

    plt.xlabel("Epoch")
    plt.ylabel("Winrate")
    plt.title("Learning curve: moving success rate, window=150")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=120)

    plt.close()


def plot_success_time_cdf(
        x: list[int],
        y: list[float],
        save_path: str | None = None,
) -> None:
    """"""
    plt.figure(figsize=(8, 4))
    plt.plot(x, y)

    plt.xlabel("Episode time")
    plt.ylabel("P(T <= t)")
    plt.title("CDF of episode time, moving window=150")
    plt.xlim(min(x), max(x))
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=120)

    plt.close()
