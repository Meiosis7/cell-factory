from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path.cwd()
OUT = ROOT / "cutout-assets"
SRC = OUT / "source-map.jpeg"

CUTOUTS = [
    {"file": "background-full.png", "title": "完整地图背景", "box": (0, 0, 1024, 559), "mask": "rect", "note": "完整原图，可作为底图"},
    {"file": "nucleus-castle.png", "title": "细胞核城堡", "box": (155, 128, 178, 214), "mask": "round", "note": "细胞核区域，可做起点场景"},
    {"file": "rough-er.png", "title": "粗面内质网", "box": (135, 105, 380, 382), "mask": "round", "note": "粗面内质网主体"},
    {"file": "golgi.png", "title": "高尔基体", "box": (545, 165, 255, 296), "mask": "round", "note": "高尔基体主体"},
    {"file": "cell-membrane.png", "title": "细胞膜", "box": (760, 10, 206, 525), "mask": "round", "note": "右侧细胞膜区域"},
    {"file": "free-ribosome-left.png", "title": "游离核糖体小人 A", "box": (82, 125, 80, 118), "mask": "circle", "note": "左侧合成起点小角色"},
    {"file": "free-ribosome-top.png", "title": "游离核糖体小人 B", "box": (256, 118, 90, 125), "mask": "circle", "note": "上方合成起点小角色"},
    {"file": "ribosome-er-lower.png", "title": "内质网上核糖体", "box": (178, 325, 75, 92), "mask": "circle", "note": "贴在粗面内质网上的核糖体"},
    {"file": "protein-er.png", "title": "内质网蛋白小人", "box": (296, 335, 84, 104), "mask": "circle", "note": "内质网中的分泌蛋白角色"},
    {"file": "transport-vesicle-er.png", "title": "运输小泡：离开内质网", "box": (378, 333, 83, 88), "mask": "circle", "note": "从内质网出芽的小泡"},
    {"file": "transport-vesicle-middle.png", "title": "运输小泡：中途", "box": (487, 258, 76, 86), "mask": "circle", "note": "路线中段运输小泡"},
    {"file": "transport-vesicle-golgi.png", "title": "运输小泡：进入高尔基体", "box": (748, 178, 78, 86), "mask": "circle", "note": "进入高尔基体的小泡"},
    {"file": "secretory-vesicle-upper.png", "title": "分泌小泡：上路", "box": (785, 300, 88, 92), "mask": "circle", "note": "高尔基体输出的小泡"},
    {"file": "secretory-vesicle-lower.png", "title": "分泌小泡：最终派送", "box": (826, 342, 86, 88), "mask": "circle", "note": "靠近细胞膜的分泌小泡"},
    {"file": "exocytosis-upper.png", "title": "胞吐：上方融合", "box": (865, 150, 112, 112), "mask": "circle", "note": "细胞膜融合/胞吐场景"},
    {"file": "exocytosis-lower.png", "title": "胞吐：下方融合", "box": (865, 336, 112, 118), "mask": "circle", "note": "下方胞吐场景"},
    {"file": "secreted-protein-top.png", "title": "细胞外蛋白小人 A", "box": (930, 118, 72, 94), "mask": "circle", "note": "释放到细胞外的小人"},
    {"file": "secreted-protein-bottom.png", "title": "细胞外蛋白小人 B", "box": (940, 468, 72, 82), "mask": "circle", "note": "右下角释放后的小人"},
    {"file": "mitochondrion.png", "title": "线粒体", "box": (540, 430, 115, 82), "mask": "circle", "note": "线粒体素材"},
    {"file": "lysosome.png", "title": "溶酶体", "box": (655, 427, 92, 95), "mask": "circle", "note": "溶酶体素材"},
    {"file": "compass.png", "title": "路径指南罗盘", "box": (36, 410, 120, 124), "mask": "circle", "note": "地图罗盘"},
    {"file": "title-banner.png", "title": "标题横幅", "box": (206, 24, 620, 62), "mask": "round", "note": "顶部标题文字"},
    {"file": "step-number-1.png", "title": "步骤编号 1", "box": (250, 124, 55, 55), "mask": "circle", "note": "数字 1 图标"},
    {"file": "step-number-3.png", "title": "步骤编号 3", "box": (485, 315, 55, 55), "mask": "circle", "note": "数字 3 图标"},
    {"file": "step-number-4.png", "title": "步骤编号 4", "box": (535, 255, 55, 55), "mask": "circle", "note": "数字 4 图标"},
    {"file": "step-number-5-upper.png", "title": "步骤编号 5 上", "box": (790, 232, 55, 55), "mask": "circle", "note": "上方数字 5 图标"},
    {"file": "step-number-5-lower.png", "title": "步骤编号 5 下", "box": (842, 315, 55, 55), "mask": "circle", "note": "下方数字 5 图标"},
]


def mask_for(size, kind):
    w, h = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    pad = 2
    if kind == "circle":
        draw.ellipse((pad, pad, w - pad, h - pad), fill=255)
    elif kind == "round":
        radius = int(min(28, w * 0.12, h * 0.18))
        draw.rounded_rectangle((pad, pad, w - pad, h - pad), radius=radius, fill=255)
    else:
        draw.rectangle((0, 0, w, h), fill=255)
    return mask


def export():
    OUT.mkdir(exist_ok=True)
    source = Image.open(SRC).convert("RGBA")
    for item in CUTOUTS:
        x, y, w, h = item["box"]
        crop = source.crop((x, y, x + w, y + h)).convert("RGBA")
        crop.putalpha(mask_for((w, h), item["mask"]))
        crop.save(OUT / item["file"])

    manifest = ["# 分泌蛋白地图素材清单", "", "坐标格式为：x,y,width,height，基于 1024x559 原图。", ""]
    for item in CUTOUTS:
        x, y, w, h = item["box"]
        manifest.append(f"- {item['file']} | {item['title']} | {x},{y},{w},{h} | {item['note']}")
    (OUT / "manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")

    figures = []
    for item in CUTOUTS:
        figures.append(f"""
        <figure>
          <div class="preview"><img src="{item['file']}" alt="{item['title']}"></div>
          <figcaption><strong>{item['title']}</strong><span>{item['file']}</span><em>{item['note']}</em></figcaption>
        </figure>
        """)

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>分泌蛋白地图素材预览</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
      color: #243044;
      background: linear-gradient(135deg, #f7fbf4, #e7f4f6 55%, #fff2dc);
    }}
    main {{ width: min(1180px, 100%); margin: 0 auto; padding: 28px; }}
    h1 {{ margin: 0 0 18px; font-size: clamp(24px, 3vw, 36px); letter-spacing: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 14px; }}
    figure {{
      margin: 0;
      border-radius: 8px;
      overflow: hidden;
      background: rgba(255,255,255,.84);
      box-shadow: 0 12px 28px rgba(28,45,62,.12);
    }}
    .preview {{
      height: 150px;
      display: grid;
      place-items: center;
      padding: 12px;
      background:
        linear-gradient(45deg, rgba(30,45,60,.08) 25%, transparent 25%),
        linear-gradient(-45deg, rgba(30,45,60,.08) 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, rgba(30,45,60,.08) 75%),
        linear-gradient(-45deg, transparent 75%, rgba(30,45,60,.08) 75%);
      background-size: 24px 24px;
      background-position: 0 0, 0 12px, 12px -12px, -12px 0;
    }}
    img {{ max-width: 100%; max-height: 126px; object-fit: contain; }}
    figcaption {{ display: grid; gap: 5px; padding: 11px 12px 13px; }}
    strong {{ font-size: 15px; }}
    span {{ color: #197f8f; font-size: 12px; word-break: break-all; }}
    em {{ color: #657382; font-size: 12px; line-height: 1.45; font-style: normal; }}
  </style>
</head>
<body>
  <main>
    <h1>分泌蛋白地图素材预览</h1>
    <section class="grid">
      {''.join(figures)}
    </section>
  </main>
</body>
</html>
"""
    (OUT / "preview.html").write_text(html, encoding="utf-8")
    print(f"Exported {len(CUTOUTS)} cutout images to {OUT}")


if __name__ == "__main__":
    export()
