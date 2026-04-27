from pathlib import Path

import imageio.v2 as imageio


def make_gif(
        frames_dir: str | Path = "frames",
        output_path: str | Path = "heatmap_training.gif",
        duration: float = 0.4,
) -> None:
    frames_dir = Path(frames_dir)
    frame_paths = sorted(frames_dir.glob("heatmap_epoch_*.png"))

    if not frame_paths:
        raise ValueError(f"No frames found in {frames_dir}")

    with imageio.get_writer(output_path, mode="I", duration=duration, loop=0) as writer:
        for path in frame_paths:
            image = imageio.imread(path)
            writer.append_data(image)
