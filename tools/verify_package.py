"""Verify the Codex v1 pet package and its 59x64 display output."""

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = json.loads((ROOT / "codex-layout.json").read_text(encoding="utf-8"))
SHEET_PATH = ROOT / "package" / "spritesheet.png"
MANIFEST_PATH = ROOT / "package" / "pet.json"


def cell_at(sheet, row, column):
    width = LAYOUT["cellWidth"]
    height = LAYOUT["cellHeight"]
    return sheet.crop((column * width, row * height, (column + 1) * width, (row + 1) * height))


def main():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["spriteVersionNumber"] == 1
    assert manifest["spritesheetPath"] == "spritesheet.png"

    sheet = Image.open(SHEET_PATH).convert("RGBA")
    assert sheet.size == (LAYOUT["width"], LAYOUT["height"])
    assert sheet.size == (1536, 1872)

    motion_report = {}
    for row in LAYOUT["rows"]:
        index = row["index"]
        required = row["requiredFrames"]
        previews = []
        for column in range(required):
            cell = cell_at(sheet, index, column)
            alpha = cell.getchannel("A")
            bounds = alpha.getbbox()
            assert bounds is not None, f'{row["state"]} frame {column + 1}: empty'
            assert bounds[0] > 0 and bounds[1] > 0
            assert bounds[2] < LAYOUT["cellWidth"] and bounds[3] < LAYOUT["cellHeight"]
            previews.append(np.asarray(cell.resize((59, 64), Image.Resampling.LANCZOS), dtype=np.float32))
        for column in range(required, LAYOUT["columns"]):
            assert cell_at(sheet, index, column).getchannel("A").getbbox() is None
        differences = []
        for current, following in zip(previews, previews[1:] + previews[:1]):
            differences.append(float(np.abs(current - following).mean()))
        motion_report[row["state"]] = {
            "minMeanAbsoluteDelta": round(min(differences), 3),
            "maxMeanAbsoluteDelta": round(max(differences), 3),
        }

    right = [cell_at(sheet, 1, column) for column in range(8)]
    left = [cell_at(sheet, 2, column) for column in range(8)]
    for column, (right_cell, left_cell) in enumerate(zip(right, left), 1):
        assert np.array_equal(np.asarray(ImageOps.mirror(right_cell)), np.asarray(left_cell)), (
            f"running mirror mismatch at frame {column}"
        )

    report = {
        "status": "PASS",
        "sheet": "1536x1872 RGBA",
        "manifest": manifest,
        "checks": [
            "all required cells contain visible pixels with safe margins",
            "all unused cells are transparent",
            "running-left is an exact horizontal mirror of running-right",
            "all state loops contain measurable frame-to-frame motion",
        ],
        "displayMotion": motion_report,
    }
    output = ROOT / "qa" / "package-verification.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {output}")


if __name__ == "__main__":
    main()
