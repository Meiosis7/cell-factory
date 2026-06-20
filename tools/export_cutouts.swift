import AppKit
import Foundation

struct Cutout {
    let file: String
    let title: String
    let x: CGFloat
    let y: CGFloat
    let w: CGFloat
    let h: CGFloat
    let mask: String
    let note: String
}

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let sourceURL = root.appendingPathComponent("cutout-assets/source-map.jpeg")
let outputDir = root.appendingPathComponent("cutout-assets")

guard let image = NSImage(contentsOf: sourceURL) else {
    fatalError("Cannot open source image: \(sourceURL.path)")
}

let imageSize = image.size

let cutouts: [Cutout] = [
    Cutout(file: "background-full.png", title: "完整地图背景", x: 0, y: 0, w: 1024, h: 559, mask: "rect", note: "完整原图，可作为底图"),
    Cutout(file: "nucleus-castle.png", title: "细胞核城堡", x: 155, y: 128, w: 178, h: 214, mask: "round", note: "细胞核区域，可做起点场景"),
    Cutout(file: "rough-er.png", title: "粗面内质网", x: 135, y: 105, w: 380, h: 382, mask: "round", note: "粗面内质网主体"),
    Cutout(file: "golgi.png", title: "高尔基体", x: 545, y: 165, w: 255, h: 296, mask: "round", note: "高尔基体主体"),
    Cutout(file: "cell-membrane.png", title: "细胞膜", x: 760, y: 10, w: 206, h: 525, mask: "round", note: "右侧细胞膜区域"),
    Cutout(file: "free-ribosome-left.png", title: "游离核糖体小人 A", x: 82, y: 125, w: 80, h: 118, mask: "circle", note: "左侧合成起点小角色"),
    Cutout(file: "free-ribosome-top.png", title: "游离核糖体小人 B", x: 256, y: 118, w: 90, h: 125, mask: "circle", note: "上方合成起点小角色"),
    Cutout(file: "ribosome-er-lower.png", title: "内质网上核糖体", x: 178, y: 325, w: 75, h: 92, mask: "circle", note: "贴在粗面内质网上的核糖体"),
    Cutout(file: "protein-er.png", title: "内质网蛋白小人", x: 296, y: 335, w: 84, h: 104, mask: "circle", note: "内质网中的分泌蛋白角色"),
    Cutout(file: "transport-vesicle-er.png", title: "运输小泡：离开内质网", x: 378, y: 333, w: 83, h: 88, mask: "circle", note: "从内质网出芽的小泡"),
    Cutout(file: "transport-vesicle-middle.png", title: "运输小泡：中途", x: 487, y: 258, w: 76, h: 86, mask: "circle", note: "路线中段运输小泡"),
    Cutout(file: "transport-vesicle-golgi.png", title: "运输小泡：进入高尔基体", x: 748, y: 178, w: 78, h: 86, mask: "circle", note: "进入高尔基体的小泡"),
    Cutout(file: "secretory-vesicle-upper.png", title: "分泌小泡：上路", x: 785, y: 300, w: 88, h: 92, mask: "circle", note: "高尔基体输出的小泡"),
    Cutout(file: "secretory-vesicle-lower.png", title: "分泌小泡：最终派送", x: 826, y: 342, w: 86, h: 88, mask: "circle", note: "靠近细胞膜的分泌小泡"),
    Cutout(file: "exocytosis-upper.png", title: "胞吐：上方融合", x: 865, y: 150, w: 112, h: 112, mask: "circle", note: "细胞膜融合/胞吐场景"),
    Cutout(file: "exocytosis-lower.png", title: "胞吐：下方融合", x: 865, y: 336, w: 112, h: 118, mask: "circle", note: "下方胞吐场景"),
    Cutout(file: "secreted-protein-top.png", title: "细胞外蛋白小人 A", x: 930, y: 118, w: 72, h: 94, mask: "circle", note: "释放到细胞外的小人"),
    Cutout(file: "secreted-protein-bottom.png", title: "细胞外蛋白小人 B", x: 940, y: 468, w: 72, h: 82, mask: "circle", note: "右下角释放后的小人"),
    Cutout(file: "mitochondrion.png", title: "线粒体", x: 540, y: 430, w: 115, h: 82, mask: "circle", note: "线粒体素材"),
    Cutout(file: "lysosome.png", title: "溶酶体", x: 655, y: 427, w: 92, h: 95, mask: "circle", note: "溶酶体素材"),
    Cutout(file: "compass.png", title: "路径指南罗盘", x: 36, y: 410, w: 120, h: 124, mask: "circle", note: "地图罗盘"),
    Cutout(file: "title-banner.png", title: "标题横幅", x: 206, y: 24, w: 620, h: 62, mask: "round", note: "顶部标题文字"),
    Cutout(file: "step-number-1.png", title: "步骤编号 1", x: 250, y: 124, w: 55, h: 55, mask: "circle", note: "数字 1 图标"),
    Cutout(file: "step-number-3.png", title: "步骤编号 3", x: 485, y: 315, w: 55, h: 55, mask: "circle", note: "数字 3 图标"),
    Cutout(file: "step-number-4.png", title: "步骤编号 4", x: 535, y: 255, w: 55, h: 55, mask: "circle", note: "数字 4 图标"),
    Cutout(file: "step-number-5-upper.png", title: "步骤编号 5 上", x: 790, y: 232, w: 55, h: 55, mask: "circle", note: "上方数字 5 图标"),
    Cutout(file: "step-number-5-lower.png", title: "步骤编号 5 下", x: 842, y: 315, w: 55, h: 55, mask: "circle", note: "下方数字 5 图标")
]

func drawCutout(_ cutout: Cutout) {
    let outSize = NSSize(width: cutout.w, height: cutout.h)
    let out = NSImage(size: outSize)
    out.lockFocus()

    NSColor.clear.setFill()
    NSRect(origin: .zero, size: outSize).fill()

    let path: NSBezierPath
    let rect = NSRect(x: 0, y: 0, width: cutout.w, height: cutout.h)
    if cutout.mask == "circle" {
        path = NSBezierPath(ovalIn: rect.insetBy(dx: 2, dy: 2))
    } else if cutout.mask == "round" {
        path = NSBezierPath(roundedRect: rect.insetBy(dx: 2, dy: 2), xRadius: min(28, cutout.w * 0.12), yRadius: min(28, cutout.h * 0.12))
    } else {
        path = NSBezierPath(rect: rect)
    }
    path.addClip()

    let sourceRect = NSRect(
        x: cutout.x,
        y: imageSize.height - cutout.y - cutout.h,
        width: cutout.w,
        height: cutout.h
    )
    image.draw(in: rect, from: sourceRect, operation: .copy, fraction: 1.0)
    out.unlockFocus()

    guard
        let tiff = out.tiffRepresentation,
        let rep = NSBitmapImageRep(data: tiff),
        let png = rep.representation(using: .png, properties: [:])
    else {
        fatalError("Cannot render \(cutout.file)")
    }

    try! png.write(to: outputDir.appendingPathComponent(cutout.file))
}

for cutout in cutouts {
    drawCutout(cutout)
}

let manifestLines = cutouts.map { item in
    "- \(item.file) | \(item.title) | \(Int(item.x)),\(Int(item.y)),\(Int(item.w)),\(Int(item.h)) | \(item.note)"
}.joined(separator: "\n")

let manifest = """
# 分泌蛋白地图素材清单

坐标格式为：x,y,width,height，基于 1024x559 原图。

\(manifestLines)
"""

try! manifest.write(to: outputDir.appendingPathComponent("manifest.md"), atomically: true, encoding: .utf8)

let htmlItems = cutouts.map { item in
    """
    <figure>
      <div class="preview"><img src="\(item.file)" alt="\(item.title)"></div>
      <figcaption><strong>\(item.title)</strong><span>\(item.file)</span><em>\(item.note)</em></figcaption>
    </figure>
    """
}.joined(separator: "\n")

let html = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>分泌蛋白地图素材预览</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
      color: #243044;
      background: linear-gradient(135deg, #f7fbf4, #e7f4f6 55%, #fff2dc);
    }
    main { width: min(1180px, 100%); margin: 0 auto; padding: 28px; }
    h1 { margin: 0 0 18px; font-size: clamp(24px, 3vw, 36px); letter-spacing: 0; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 14px; }
    figure {
      margin: 0;
      border-radius: 8px;
      overflow: hidden;
      background: rgba(255,255,255,.84);
      box-shadow: 0 12px 28px rgba(28,45,62,.12);
    }
    .preview {
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
    }
    img { max-width: 100%; max-height: 126px; object-fit: contain; }
    figcaption { display: grid; gap: 5px; padding: 11px 12px 13px; }
    strong { font-size: 15px; }
    span { color: #197f8f; font-size: 12px; word-break: break-all; }
    em { color: #657382; font-size: 12px; line-height: 1.45; font-style: normal; }
  </style>
</head>
<body>
  <main>
    <h1>分泌蛋白地图素材预览</h1>
    <section class="grid">
      \(htmlItems)
    </section>
  </main>
</body>
</html>
"""

try! html.write(to: outputDir.appendingPathComponent("preview.html"), atomically: true, encoding: .utf8)

print("Exported \(cutouts.count) cutout images to \(outputDir.path)")
