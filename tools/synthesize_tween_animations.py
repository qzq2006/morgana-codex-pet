"""Build deterministic animation sequences from approved A/B images."""

import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-frames"
VIDEOS = ROOT / "videos"
STATES = (
    "idle",
    "running-right",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
)
FRAME_COUNT = 24
WORK_SIZE = 512


def load_image(path):
    image = Image.open(path).convert("RGB")
    image.thumbnail((WORK_SIZE, WORK_SIZE), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (WORK_SIZE, WORK_SIZE), "white")
    position = ((WORK_SIZE - image.width) // 2, (WORK_SIZE - image.height) // 2)
    canvas.paste(image, position)
    return np.asarray(canvas)


def calculate_flow(source, target):
    source_gray = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)
    algorithm = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    algorithm.setUseSpatialPropagation(True)
    return algorithm.calc(source_gray, target_gray, None)


def warp(image, motion, amount):
    height, width = image.shape[:2]
    grid_x, grid_y = np.meshgrid(np.arange(width), np.arange(height))
    map_x = (grid_x - motion[..., 0] * amount).astype(np.float32)
    map_y = (grid_y - motion[..., 1] * amount).astype(np.float32)
    return cv2.remap(
        image,
        map_x,
        map_y,
        cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255),
    )


def interpolate(frame_a, frame_b, flow_ab, flow_ba, amount):
    if amount <= 0:
        return frame_a.copy()
    if amount >= 1:
        return frame_b.copy()
    warped_a = warp(frame_a, flow_ab, amount)
    warped_b = warp(frame_b, flow_ba, 1.0 - amount)
    blended = cv2.addWeighted(warped_a, 1.0 - amount, warped_b, amount, 0)
    blended[blended.min(axis=2) >= 248] = 255
    return blended


def reset_folder(folder):
    folder.mkdir(parents=True, exist_ok=True)
    for path in folder.glob("frame-*.png"):
        path.unlink()


def make_state(state):
    frame_a = load_image(SOURCE / f"{state}-frame-a.png")
    frame_b = load_image(SOURCE / f"{state}-frame-b.png")
    flow_ab = calculate_flow(frame_a, frame_b)
    flow_ba = calculate_flow(frame_b, frame_a)
    output = VIDEOS / state
    reset_folder(output)
    for index in range(FRAME_COUNT):
        amount = 0.5 - 0.5 * math.cos(2.0 * math.pi * index / FRAME_COUNT)
        result = interpolate(frame_a, frame_b, flow_ab, flow_ba, amount)
        Image.fromarray(result).save(output / f"frame-{index + 1:04d}.png")
    print(f"PASS {state}: {FRAME_COUNT} optical-flow frames")


def main():
    for state in STATES:
        make_state(state)
    metadata = {
        "method": "deterministic bidirectional DIS optical-flow tween",
        "loop": "cosine A-to-B-to-A",
        "source": "operator-approved Frame A/B pairs",
        "workSize": f"{WORK_SIZE}x{WORK_SIZE}",
        "framesPerState": FRAME_COUNT,
        "states": list(STATES),
    }
    (VIDEOS / "generation.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PASS: videos/generation.json")


if __name__ == "__main__":
    main()
