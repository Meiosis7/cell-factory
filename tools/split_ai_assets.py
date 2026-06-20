from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path.cwd()
OUT = ROOT / "ai-assets"
SOURCE = OUT / "source-sprite-sheet.png"

ASSETS = [
    ("nucleus-castle", "细胞核城堡"),
    ("rough-er", "粗面内质网"),
    ("golgi", "高尔基体"),
    ("cell-membrane", "细胞膜"),
    ("ribosome-character", "核糖体/蛋白小人"),
    ("transport-vesicle", "运输小泡"),
    ("secretory-vesicle", "分泌小泡"),
    ("mitochondrion", "线粒体"),
]


def remove_green(cell: Image.Image) -> Image.Image:
    rgba = cell.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size

    # Chroma key: keep non-green pixels, soften the edge a little.
    alpha = Image.new("L", rgba.size, 0)
    alpha_pixels = alpha.load()
    for y in range(height):
        for x in range(width):
            r, g, b, _ = pixels[x, y]
            green_strength = g - max(r, b)
            if g > 160 and green_strength > 55:
                a = 0
            elif g > 125 and green_strength > 25:
                a = 90
            else:
                a = 255
            alpha_pixels[x, y] = a

    alpha = alpha.filter(ImageFilter.GaussianBlur(0.35))
    rgba.putalpha(alpha)

    # Crop to subject bounds.
    bbox = alpha.point(lambda value: 255 if value > 12 else 0).getbbox()
    if bbox:
        pad = 18
        left = max(0, bbox[0] - pad)
        top = max(0, bbox[1] - pad)
        right = min(width, bbox[2] + pad)
        bottom = min(height, bbox[3] + pad)
        rgba = rgba.crop((left, top, right, bottom))

    return rgba


def make_preview(files):
    cards = []
    background = OUT / "clean-background.png"
    if background.exists():
        cards.append("""
        <figure class="wide">
          <div class="preview"><img src="clean-background.png" alt="干净地图背景"></div>
          <figcaption><strong>干净地图背景</strong><span>clean-background.png</span></figcaption>
        </figure>
        """)
    for filename, title in files:
        cards.append(f"""
        <figure>
          <div class="preview"><img src="{filename}" alt="{title}"></div>
          <figcaption><strong>{title}</strong><span>{filename}</span></figcaption>
        </figure>
        """)

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 重新生成素材预览</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
      color: #243044;
      background: linear-gradient(135deg, #f7fbf4, #e7f4f6 55%, #fff2dc);
    }}
    main {{ width: min(1080px, 100%); margin: 0 auto; padding: 28px; }}
    h1 {{ margin: 0 0 18px; font-size: clamp(24px, 3vw, 36px); letter-spacing: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 14px; }}
    figure {{
      margin: 0;
      border-radius: 8px;
      overflow: hidden;
      background: rgba(255,255,255,.86);
      box-shadow: 0 12px 28px rgba(28,45,62,.12);
    }}
    .wide {{ grid-column: span 2; }}
    .preview {{
      height: 180px;
      display: grid;
      place-items: center;
      padding: 14px;
      background:
        linear-gradient(45deg, rgba(30,45,60,.08) 25%, transparent 25%),
        linear-gradient(-45deg, rgba(30,45,60,.08) 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, rgba(30,45,60,.08) 75%),
        linear-gradient(-45deg, transparent 75%, rgba(30,45,60,.08) 75%);
      background-size: 24px 24px;
      background-position: 0 0, 0 12px, 12px -12px, -12px 0;
    }}
    img {{ max-width: 100%; max-height: 150px; object-fit: contain; }}
    figcaption {{ display: grid; gap: 5px; padding: 12px 13px 14px; }}
    strong {{ font-size: 15px; }}
    span {{ color: #197f8f; font-size: 12px; word-break: break-all; }}
  </style>
</head>
<body>
  <main>
    <h1>AI 重新生成素材预览</h1>
    <section class="grid">
      {''.join(cards)}
    </section>
  </main>
</body>
</html>
"""
    (OUT / "preview.html").write_text(html, encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    sheet = Image.open(SOURCE).convert("RGBA")
    width, height = sheet.size
    cell_w = width // 4
    cell_h = height // 2

    exported = []
    for index, (name, title) in enumerate(ASSETS):
        col = index % 4
        row = index // 4
        cell = sheet.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
        asset = remove_green(cell)
        filename = f"{name}.png"
        asset.save(OUT / filename)
        exported.append((filename, title))

    manifest = ["# AI 重新生成素材清单", "", "这些素材由 AI 参考原图风格重新生成，再本地去除绿幕背景。", ""]
    for filename, title in exported:
        manifest.append(f"- {filename} | {title}")
    (OUT / "manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    make_preview(exported)
    print(f"Exported {len(exported)} transparent AI assets to {OUT}")


if __name__ == "__main__":
    main()
