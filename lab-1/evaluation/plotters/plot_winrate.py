import matplotlib.pyplot as plt

import numpy as np


def smooth(x, k=20):
    return np.convolve(x, np.ones(k) / k, mode="valid")


def plot_winrate(winrates, save_path=None):
    epochs = range(len(winrates))

    plt.figure(figsize=(8, 4))
    plt.plot(epochs, winrates)

    plt.xlabel("Epoch")
    plt.ylabel("Winrate")
    plt.title("Winrate per epoch")
    plt.ylim(0, 1)  # если это доля
    plt.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=120)

    plt.show()

    plt.plot(winrates, alpha=0.3)
    plt.plot(smooth(winrates), linewidth=2)
