# -*- coding: utf-8 -*-
"""为首页缺标题的文件加“编号+名称”（与正文同页，不另起页）。
PDF：pdftoppm 渲染首页 → 检测顶部留白 → 留白够直接写入 / 不足则原内容等比缩小让出标题带
     → 新首页整页替换（规避 /Rotate 旋转与 pypdf 合并的方向陷阱）。
DOCX：在正文开头插入标题段（默认左对齐黑体加粗14pt）。
标题检测：首页文本包含文件名编号（如 1.2.1）视为已有；纯扫描件无文本层视为缺失——
     若文件首页标题是图像（旧处理残留），文本检测不到，用 --items 显式指定并先恢复干净原件。

用法:
  python add_item_titles.py --folder <目录> [--items 1,3.2.1,4] [--band-pt 42]
                            [--title-pt 16] [--align left|center] [--left-pt 90] [--dpi 160]
"""
import argparse, os, re, sys, shutil, subprocess, zipfile
sys.stdout.reconfigure(encoding="utf-8")
from pypdf import PdfReader, PdfWriter
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--folder", required=True)
ap.add_argument("--items", default=None, help="逗号分隔编号（支持 1.2.1 形式）；缺省=自动检测缺标题者")
ap.add_argument("--band-pt", type=int, default=42)
ap.add_argument("--title-pt", type=int, default=16)
ap.add_argument("--align", default="left", choices=["left", "center"])
ap.add_argument("--left-pt", type=int, default=90)
ap.add_argument("--dpi", type=int, default=160)
a = ap.parse_args()

HB = os.path.normpath(a.folder)
WORK = os.path.join(HB, "_titletmp")
os.makedirs(WORK, exist_ok=True)
FONT = "C:/Windows/Fonts/simhei.ttf"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import catalog

def find_file(n_str):
    key = tuple(int(x) for x in re.findall(r"\d+", n_str))
    for p, num_str, name, k in catalog(HB):
        if k == key:
            return p
    # 兜底：编号首段相同即可
    first = key[0]
    cands = [p for p, num_str, name, k in catalog(HB) if k[0] == first]
    return cands[0] if len(cands) == 1 else None

def render_first(f, tag):
    pre = os.path.join(WORK, tag)
    subprocess.run(["pdftoppm", "-png", "-r", str(a.dpi), "-f", "1", "-l", "1", f, pre],
                   check=True, capture_output=True)
    cands = [x for x in os.listdir(WORK) if x.startswith(tag + "-") and x.endswith(".png")]
    return os.path.join(WORK, cands[0])

def top_blank_px(im):
    g = im.convert("L"); w, h = g.size; px = g.load()
    for y in range(h):
        if min(px[x, y] for x in range(0, w, 3)) < 235:
            return y
    return h

def has_title_text(f, num_str, name):
    ext = os.path.splitext(f)[1].lower()
    if ext == ".docx":
        import zipfile
        z = zipfile.ZipFile(f)
        xml = z.read("word/document.xml").decode("utf-8")
        return (num_str in xml) and (name[:4] in xml if name else True)
    import fitz
    fitz.TOOLS.mupdf_display_errors(False)
    d = fitz.open(f)
    t = d[0].get_text()
    d.close()
    return (num_str in t) and (name[:4] in t if name else True)

# 待处理清单
if a.items:
    targets = []
    for s in a.items.split(","):
        s = s.strip()
        num_str, name, key = parse_name(s if re.search(r"[一-鿿]", s) else s + ".")
        f = find_file(num_str if not name else num_str)
        targets.append((f, num_str, name))
else:
    targets = []
    for p, num_str, name, key in catalog(HB):
        if key == (10**9,):
            continue
        if not has_title_text(p, num_str, name):
            targets.append((p, num_str, name))
print("处理文件:", [(os.path.basename(p), ns) for p, ns, _ in targets])

for f, num_str, name in targets:
    ext = os.path.splitext(f)[1].lower()
    disp = f"{num_str}　{name}" if name else num_str
    if ext == ".docx":
        import zipfile
        zin = zipfile.ZipFile(f)
        entries = [(i, zin.read(i.filename)) for i in zin.infolist()]
        zin.close()
        with zipfile.ZipFile(f + ".tmp", "w", zipfile.ZIP_DEFLATED) as zout:
            for info, data in entries:
                if info.filename == "word/document.xml":
                    s = data.decode("utf-8")
                    i0 = s.index("<w:body>") + len("<w:body>")
                    m = re.search(r"<w:p\b", s[i0:])
                    ins = ('<w:p><w:pPr><w:jc w:val="' + a.align + '"/>'
                           '<w:spacing w:before="120" w:after="120"/></w:pPr>'
                           '<w:r><w:rPr><w:rFonts w:hint="eastAsia" w:ascii="黑体" w:hAnsi="黑体" '
                           'w:eastAsia="黑体" w:cs="黑体"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
                           f'<w:t xml:space="preserve">{disp}</w:t></w:r></w:p><w:p/>')
                    s = s[:i0 + m.start()] + ins + s[i0 + m.start():]
                    data = s.encode("utf-8")
                zout.writestr(info, data)
        shutil.move(f + ".tmp", f)
        print("docx标题段已插入:", os.path.basename(f))
        continue

    png = render_first(f, os.path.splitext(os.path.basename(f))[0])
    im = Image.open(png).convert("RGB")
    W, H = im.size
    blank = top_blank_px(im)
    band_px = int(a.band_pt * a.dpi / 72)
    fs_px = int(a.title_pt * a.dpi / 72)
    left_px = int(a.left_pt * a.dpi / 72)

    if blank >= band_px:
        canvas = im.copy()
        ty = min(max(int(blank / 2) - fs_px // 2, int(6 * a.dpi / 72)),
                 blank - int(20 * a.dpi / 72))
    else:
        scale = (H - band_px) / H
        nw, nh = int(W * scale), int(H * scale)
        canvas = Image.new("RGB", (W, H), "white")
        canvas.paste(im.resize((nw, nh), Image.LANCZOS), ((W - nw) // 2, band_px))
        ty = (band_px - fs_px) // 2

    dr = ImageDraw.Draw(canvas)
    x_start = left_px if a.align == "left" else (W - int(dr.textlength(disp, font=ImageFont.truetype(FONT, size)))) // 2
    size = fs_px
    font = ImageFont.truetype(FONT, size)
    while x_start + dr.textlength(disp, font=font) > W - int(12 * a.dpi / 72) and size > 10:
        size -= 1
        font = ImageFont.truetype(FONT, size)
    dr.rectangle([0, 0, W, ty + size + int(4 * a.dpi / 72)], fill="white")
    dr.text((x_start, ty), disp, fill="black", font=font)

    page_pdf = os.path.join(WORK, "_newfirst.pdf")
    canvas.save(page_pdf, "PDF", resolution=a.dpi)

    r = PdfReader(f)
    w2 = PdfWriter()
    w2.add_page(PdfReader(page_pdf).pages[0])
    for p in list(r.pages)[1:]:
        w2.add_page(p)
    tmp = f + ".tmp"
    with open(tmp, "wb") as fh:
        w2.write(fh)
    os.replace(tmp, f)
    blank_pt = blank * 72 // a.dpi
    mode = "写入留白" if blank >= band_px else "缩放让位"
    print(f"完成 {os.path.basename(f)[:40]}: {mode} {blank_pt}pt → 共{len(PdfReader(f).pages)}页")
print("全部完成")
