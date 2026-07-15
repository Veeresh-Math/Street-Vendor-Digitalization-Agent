"""Generate PWA icons for the Street Vendor Digitalization Agent."""
import os
from PIL import Image, ImageDraw, ImageFont

SIZES = [72, 96, 128, 144, 152, 192, 384, 512]
OUTPUT_DIR = os.path.join("static", "icons")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_icon(size: int) -> Image.Image:
    """Create an Indian-themed saffron gradient icon with 'SV' text."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle with saffron gradient approximation
    for i in range(size):
        ratio = i / size
        r = int(255 * (1 - ratio * 0.3))
        g = int(107 * (1 + ratio * 0.2))
        b = int(0 + ratio * 20)
        draw.ellipse([0, i, size, i + 1], fill=(r, g, b, 255))

    # Inner circle (darker)
    margin = int(size * 0.08)
    inner_size = size - margin * 2
    draw.ellipse(
        [margin, margin, margin + inner_size, margin + inner_size],
        fill=(7, 8, 10, 230),
    )

    # Draw "SV" text
    try:
        font_size = int(size * 0.28)
        font = ImageFont.truetype("arial.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    text = "SV"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2
    y = (size - th) // 2 - int(size * 0.02)
    draw.text((x, y), text, fill=(255, 107, 0, 255), font=font)

    return img


if __name__ == "__main__":
    for s in SIZES:
        icon = create_icon(s)
        path = os.path.join(OUTPUT_DIR, f"icon-{s}.png")
        icon.save(path, "PNG")
        print(f"Created {path}")

    print(f"\nGenerated {len(SIZES)} icons in {OUTPUT_DIR}/")
