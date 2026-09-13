from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-frames"
QA = ROOT / "qa"
QA.mkdir(exist_ok=True)


def fit_preview(source: Path, destination: Path) -> Image.Image:
    image = Image.open(source).convert("RGB")
    image.thumbnail((59, 64), Image.Resampling.LANCZOS)
    preview = Image.new("RGB", (59, 64), "white")
    preview.paste(image, ((59 - image.width) // 2, (64 - image.height) // 2))
    preview.save(destination)
    return preview


frame_a = fit_preview(SOURCE / "idle-frame-a.png", QA / "idle-preview-a.png")
frame_b = fit_preview(SOURCE / "idle-frame-b.png", QA / "idle-preview-b.png")

scale = 6
gap = 18
label_h = 32
canvas = Image.new("RGB", (59 * scale * 2 + gap * 3, 64 * scale + label_h + gap * 2), "#ececec")
draw = ImageDraw.Draw(canvas)
font = ImageFont.load_default(size=18)
for index, (label, frame) in enumerate((("Frame A", frame_a), ("Frame B", frame_b))):
    enlarged = frame.resize((59 * scale, 64 * scale), Image.Resampling.NEAREST)
    x = gap + index * (59 * scale + gap)
    y = gap + label_h
    canvas.paste(enlarged, (x, y))
    draw.text((x, gap), label, fill="#181818", font=font)
canvas.save(QA / "idle-contact.png")
print("Created 59x64 previews and A/B contact sheet.")

