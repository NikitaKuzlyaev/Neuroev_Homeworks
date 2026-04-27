from pathlib import Path

import imageio.v2 as imageio


def make_gif(
        frames_dir: str | Path = "frames",
        output_path: str | Path = "heatmap_training.gif",
        duration: float = 0.4,
) -> None:
    frames_dir = Path(frames_dir)
    frame_paths = sorted(frames_dir.glob("heatmap_epoch_*.png"))

    images = [imageio.imread(path) for path in frame_paths]

    imageio.mimsave(
        output_path,
        images,
        duration=duration,
        loop=0,
    )
