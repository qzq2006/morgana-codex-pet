"""Extract approved animation videos into Codex sprite rows and build the package.

Accepted input for every generated state:
  videos/<state>.mp4 (also .mov/.webm/.mkv)
or
  videos/<state>/frame-*.png

running-left is mirrored deterministically from running-right.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos"
ROWS = ROOT / "rows"
QA = ROOT / "qa" / "animations"

SPECS = {
    "idle": 6,
    "running-right": 8,
    "waving": 4,
    "jumping": 5,
    "failed": 8,
    "waiting": 6,
    "running": 6,
    "review": 6,
}
VIDEO_EXTENSIONS = (".mp4", ".mov", ".webm", ".mkv")


def evenly_spaced_indices(length: int, count: int) -> list[int]:
    if length < count:
        raise ValueError(f"only {length} source frames for {count} required frames")
    return np.linspace(0, length, num=count, endpoint=False, dtype=int).tolist()


def read_video(path: Path) -> list[Image.Image]:
    if importlib.util.find_spec("cv2") is None:
        raise RuntimeError(
            "OpenCV is unavailable. Export the animation as videos/<state>/frame-*.png instead."
        )
    import cv2

    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(
            f"cannot decode {path.name}; export it as a PNG sequence under videos/{path.stem}/"
        )
    frames: list[Image.Image] = []
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame))
    capture.release()
    if not frames:
        raise RuntimeError(f"no frames decoded from {path.name}")
    return frames


def find_input(state: str) -> tuple[str, Path]:
    folder = VIDEOS / state
    if folder.is_dir() and list(folder.glob("*.png")):
        return "frames", folder
    for extension in VIDEO_EXTENSIONS:
        candidate = VIDEOS / f"{state}{extension}"
        if candidate.exists():
            return "video", candidate
    raise FileNotFoundError(
        f"missing {state}: add videos/{state}.mp4 or videos/{state}/frame-*.png"
    )


def load_source(state: str) -> list[Image.Image]:
    kind, path = find_input(state)
    if kind == "video":
        return read_video(path)
    paths = sorted(path.glob("*.png"))
    return [Image.open(item).convert("RGB") for item in paths]


def reset_state_folder(state: str) -> Path:
    folder = ROWS / state
    folder.mkdir(parents=True, exist_ok=True)
    for path in folder.glob("frame-*.png"):
        path.unlink()
    return folder


def write_state(state: str, frames: list[Image.Image], count: int) -> list[Path]:
    chosen = [frames[index].convert("RGB") for index in evenly_spaced_indices(len(frames), count)]
    folder = reset_state_folder(state)
    output: list[Path] = []
    for number, frame in enumerate(chosen, 1):
        path = folder / f"frame-{number:02d}.png"
        frame.save(path)
        output.append(path)
    return output


def mirror_running_left(paths: list[Path]) -> list[Path]:
    folder = reset_state_folder("running-left")
    output: list[Path] = []
    for number, source in enumerate(paths, 1):
        path = folder / f"frame-{number:02d}.png"
        ImageOps.mirror(Image.open(source).convert("RGB")).save(path)
        output.append(path)
    return output


def alpha_cutout(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = np.asarray(rgba).copy()
    light = pixels[..., :3].min(axis=2)
    original_alpha = pixels[..., 3].astype(np.float32)
    feather = np.clip((250.0 - light.astype(np.float32)) / 25.0 * 255.0, 0, 255)
    pixels[..., 3] = np.minimum(original_alpha, feather).astype(np.uint8)
    return Image.fromarray(pixels, "RGBA")


def preview_cell(path: Path) -> Image.Image:
    image = alpha_cutout(Image.open(path))
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError(f"{path}: empty after white-background removal")
    image = image.crop(bounds)
    scale = min(52 / image.width, 58 / image.height)
    image = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    cell = Image.new("RGBA", (59, 64), (22, 22, 24, 255))
    cell.alpha_composite(image, ((59 - image.width) // 2, 62 - image.height))
    return cell


def write_qa(state: str, paths: list[Path]) -> None:
    QA.mkdir(parents=True, exist_ok=True)
    cells = [preview_cell(path) for path in paths]
    gap = 8
    label_height = 24
    contact = Image.new(
        "RGBA",
        (gap + len(cells) * (59 + gap), label_height + 64 + gap),
        (236, 236, 238, 255),
    )
    draw = ImageDraw.Draw(contact)
    draw.text((gap, 5), state, fill=(18, 18, 20, 255), font=ImageFont.load_default())
    for index, cell in enumerate(cells):
        contact.alpha_composite(cell, (gap + index * (59 + gap), label_height))
    contact.save(QA / f"{state}-contact.png", optimize=True)
    cells[0].save(
        QA / f"{state}.gif",
        save_all=True,
        append_images=cells[1:],
        duration=180,
        loop=0,
        disposal=2,
    )


def main() -> None:
    missing = []
    for state in SPECS:
        try:
            find_input(state)
        except FileNotFoundError as error:
            missing.append(str(error))
    if missing:
        raise SystemExit("Missing animation inputs:\n  " + "\n  ".join(missing))

    written: dict[str, list[Path]] = {}
    for state, count in SPECS.items():
        written[state] = write_state(state, load_source(state), count)
        write_qa(state, written[state])
        print(f"PASS {state}: {count} frames")

    written["running-left"] = mirror_running_left(written["running-right"])
    write_qa("running-left", written["running-left"])
    print("PASS running-left: mirrored from running-right")

    subprocess.run([sys.executable, str(ROOT / "tools" / "build_codex_sheet.py")], check=True)
    print("PASS: animation QA and Codex package built")


if __name__ == "__main__":
    main()
