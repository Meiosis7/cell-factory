from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path.cwd()
OUT = ROOT / "ai-assets"
SOURCE = OUT / "ribosome-peptide-source.png"

ASSETS = [
    ("ribosome.png", "核糖体"),
    ("peptide-chain.png", "肽链"),
]


def remove_green(cell: Image.Image) -> Image.Image:
    rgba = cell.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    alpha = Image.new("L", rgba.size, 0)
    alpha_pixels = alpha.load()

    for y in range(height):
        for x in range(width):
            r, g, b, _ = pixels[x, y]
            green_strength = g - max(r, b)
            if g > 160 and green_strength > 55:
                a = 0
            elif g > 125 and green_strength > 25:
                a = 80
            else:
                a = 255
            alpha_pixels[x, y] = a

    alpha = alpha.filter(ImageFilter.GaussianBlur(0.3))
    rgba.putalpha(alpha)

    bbox = alpha.point(lambda value: 255 if value > 12 else 0).getbbox()
    if bbox:
        pad = 20
        rgba = rgba.crop((
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(width, bbox[2] + pad),
            min(height, bbox[3] + pad),
        ))
    return rgba


def main():
    sheet = Image.open(SOURCE).convert("RGBA")
    width, height = sheet.size
    cell_w = width // 2

    for index, (filename, title) in enumerate(ASSETS):
        cell = sheet.crop((index * cell_w, 0, (index + 1) * cell_w, height))
        asset = remove_green(cell)
        asset.save(OUT / filename)
        print(f"exported {filename}: {asset.size[0]}x{asset.size[1]} {title}")

    manifest = OUT / "manifest.md"
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write("\n- ribosome.png | 核糖体\n")
        handle.write("- peptide-chain.png | 肽链\n")


if __name__ == "__main__":
    main()
