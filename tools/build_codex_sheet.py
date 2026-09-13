import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = json.loads((ROOT / "codex-layout.json").read_text(encoding="utf-8"))
ROWS = ROOT / "rows"
PACKAGE = ROOT / "package"

def cutout(path):
    image = Image.open(path).convert("RGBA")
    pixels = np.asarray(image).copy()
    light = pixels[..., :3].min(axis=2)
    original_alpha = pixels[..., 3].astype(np.float32)
    feather = np.clip((250.0 - light.astype(np.float32)) / 25.0 * 255.0, 0, 255)
    pixels[..., 3] = np.minimum(original_alpha, feather).astype(np.uint8)
    return Image.fromarray(pixels, "RGBA")

def cell(path):
    width = LAYOUT["cellWidth"]
    height = LAYOUT["cellHeight"]
    image = cutout(path)
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError(f"{path}: fully transparent")
    image = image.crop(bounds)
    scale = min(width * 0.88 / image.width, height * 0.90 / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    image = image.resize(size, Image.Resampling.LANCZOS)
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    position = ((width - size[0]) // 2, height - size[1] - round(height * 0.045))
    result.alpha_composite(image, position)
    return result

def main():
    width = LAYOUT["width"]
    height = LAYOUT["height"]
    cell_width = LAYOUT["cellWidth"]
    cell_height = LAYOUT["cellHeight"]
    if width != LAYOUT["columns"] * cell_width:
        raise ValueError("invalid horizontal layout")
    if height != len(LAYOUT["rows"]) * cell_height:
        raise ValueError("invalid vertical layout")
    sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    missing = []
    prepared = []
    prepared_by_state = {}
    for row in LAYOUT["rows"]:
        folder = ROWS / row["state"]
        files = sorted(folder.glob("frame-*.png"))
        required = row["requiredFrames"]
        if len(files) < required:
            missing.append(f'{row["state"]}: {len(files)}/{required}')
            continue
        state = row["state"]
        if state == "running-left" and "running-right" in prepared_by_state:
            frames = [ImageOps.mirror(frame) for frame in prepared_by_state["running-right"]]
        else:
            frames = [cell(path) for path in files[:required]]
        prepared_by_state[state] = frames
        prepared.append((row, frames))
    if missing:
        raise SystemExit("Missing required frames:\n  " + "\n  ".join(missing))
    for row, frames in prepared:
        for column, frame in enumerate(frames):
            alpha_min, alpha_max = frame.getchannel("A").getextrema()
            if alpha_max == 0 or alpha_min != 0:
                raise ValueError(f'{row["state"]} frame {column + 1}: invalid alpha')
            sheet.alpha_composite(frame, (column * cell_width, row["index"] * cell_height))
    PACKAGE.mkdir(exist_ok=True)
    sheet.save(PACKAGE / "spritesheet.png", optimize=True)
    draft = json.loads((PACKAGE / "pet.json.draft").read_text(encoding="utf-8"))
    (PACKAGE / "pet.json").write_text(
        json.dumps(draft, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PASS: package/spritesheet.png and package/pet.json")

if __name__ == "__main__":
    main()
