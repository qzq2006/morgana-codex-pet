import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]


def preview(source):
    image = Image.open(source).convert("RGB")
    image.thumbnail((59, 64), Image.Resampling.LANCZOS)
    result = Image.new("RGB", (59, 64), "white")
    result.paste(image, ((59 - image.width) // 2, (64 - image.height) // 2))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("state")
    args = parser.parse_args()
    state = args.state
    source = ROOT / "source-frames"
    qa = ROOT / "qa"
    qa.mkdir(exist_ok=True)

    frames = [
        preview(source / f"{state}-frame-a.png"),
        preview(source / f"{state}-frame-b.png"),
    ]
    for label, frame in zip(("a", "b"), frames):
        frame.save(qa / f"{state}-preview-{label}.png")

    scale = 6
    gap = 18
    label_height = 32
    canvas = Image.new(
        "RGB",
        (59 * scale * 2 + gap * 3, 64 * scale + label_height + gap * 2),
        "#ececec",
    )
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=18)
    for index, (label, frame) in enumerate(zip(("Frame A", "Frame B"), frames)):
        x = gap + index * (59 * scale + gap)
        canvas.paste(
            frame.resize((59 * scale, 64 * scale), Image.Resampling.NEAREST),
            (x, gap + label_height),
        )
        draw.text((x, gap), label, fill="#181818", font=font)
    canvas.save(qa / f"{state}-contact.png")
    print(f"Created {state} QA previews")


if __name__ == "__main__":
    main()
