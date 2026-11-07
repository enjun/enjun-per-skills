# -*- coding: utf-8 -*-
"""为缺“序号N：名称”首页标题的材料加标题（与正文同页，不另起页）。
PDF：pdftoppm 渲染首页 → 检测顶部留白 → 留白够直接写标题 / 不足则原内容缩放让位
     → 用新首页整页替换（规避 /Rotate 旋转与 pypdf 合并的方向陷阱）。
DOCX：在正文开头插入标题段（默认左对齐黑体加粗14pt）。
注意：文件首段已是整页图像且顶部有旧标题条的，文本检测不到——用 --items 显式指定并先恢复干净原件。

用法:
  python add_item_titles.py --folder <目录> [--items 11,20,49] [--names-xlsx <记录表.xlsx>]
                            [--band-pt 42] [--title-pt 16] [--left-pt 90] [--align left|center]
"""
import argparse, os, re, sys, shutil, subprocess
sys.stdout.reconfigure(encoding="utf-8")
from pypdf import PdfReader, PdfWriter
from PIL import Image, ImageDraw, ImageFont
from openpyxl import load_workbook

ap = argparse.ArgumentParser()
ap.add_argument("--folder", required=True)
ap.add_argument("--names-xlsx", default=None, help="默认 <folder>/材料清单记录表.xlsx")
ap.add_argument("--items", default=None, help="逗号分隔序号；缺省=自动检测缺标题者")
ap.add_argument("--band-pt", type=int, default=42)
ap.add_argument("--title-pt", type=int, default=16)
ap.add_argument("--left-pt", type=int, default=90)
ap.add_argument("--align", default="left", choices=["left", "center"])
ap.add_argument("--dpi", type=int, default=160)
a = ap.parse_args()

HB = a.folder
WORK = os.path.join(HB, "_titletmp")
os.makedirs(WORK, exist_ok=True)
FONT = "C:/Windows/Fonts/simhei.ttf"

xlsx = a.names_xlsx or os.path.join(HB, "材料清单记录表.xlsx")
wb = load_workbook(xlsx)
ws = wb.worksheets[0]
NAMES = {}
for r in range(2, ws.max_row + 1):
    if ws.cell(r, 2).value is not None:
        NAMES[ws.cell(r, 2).value] = re.sub(r"（(戴校|许校|刘晓勇)？?）\s*$", "", str(ws.cell(r, 3).value))

def find_file(n):
    for f in os.listdir(HB):
        if re.match(rf"^{n}([\s\-（]|$)", f) and f.lower().endswith((".pdf", ".docx")):
            return os.path.join(HB, f)
    raise FileNotFoundError(n)

def detect_lacking():
    """返回缺标题的序号列表（PDF看首页文本；docx看正文XML）"""
    lacking = []
    for f in os.listdir(HB):
        m = re.match(r"^(\d+)", f)
        if not m or not f.lower().endswith((".pdf", ".docx")):
            continue
        n = int(m.group(1))
        if f.endswith(".docx"):
            import zipfile
            z = zipfile.ZipFile(os.path.join(HB, f))
            xml = z.read("word/document.xml").decode("utf-8")
            if f"序号{n}：" not in xml:
                lacking.append(n)
        else:
            import fitz
            fitz.TOOLS.mupdf_display_errors(False)
            d = fitz.open(os.path.join(HB, f))
            if f"序号{n}：" not in d[0].get_text():
                lacking.append(n)
            d.close()
    return sorted(set(lacking))

ITEMS = [int(x) for x in a.items.split(",")] if a.items else detect_lacking()
print("处理序号:", ITEMS)

def render_first(f, tag):
    pre = os.path.join(WORK, tag)
    subprocess.run(["pdftoppm", "-png", "-r", str(a.dpi), "-f", "1", "-l", "1", f, pre],
                   check=True, capture_output=True)
    # pdftoppm 输出文件名的页号位数不定，按前缀查找
    cands = [x for x in os.listdir(WORK) if x.startswith(tag + "-") and x.endswith(".png")]
    return os.path.join(WORK, cands[0])

def top_blank_px(im):
    g = im.convert("L"); w, h = g.size; px = g.load()
    for y in range(h):
        if min(px[x, y] for x in range(0, w, 3)) < 235:
            return y
    return h

for n in ITEMS:
    f = find_file(n)
    name = NAMES.get(n)
    if not name:
        print(f"!! 序号{n} 无名称（记录表缺失），跳过"); continue
    if f.endswith(".docx"):
        import zipfile
        zin = zipfile.ZipFile(f)
        entries = [(i, zin.read(i.filename)) for i in zin.infolist()]
        zin.close()
        with zipfile.ZipFile(f + ".tmp", "w", zipfile.ZIP_DEFLATED) as zout:
            for info, data in entries:
                if info.filename == "word/document.xml":
                    s = data.decode("utf-8")
                    if f"序号{n}：" in s:
                        print(f"序号{n} 已有标题，跳过"); continue
                    i0 = s.index("<w:body>") + len("<w:body>")
                    m = re.search(r"<w:p\b", s[i0:])
                    ins = ('<w:p><w:pPr><w:jc w:val="' + a.docx_align + '"/>'
                           '<w:spacing w:before="120" w:after="120"/></w:pPr>'
                           '<w:r><w:rPr><w:rFonts w:hint="eastAsia" w:ascii="黑体" w:hAnsi="黑体" '
                           'w:eastAsia="黑体" w:cs="黑体"/><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
                           f'<w:t xml:space="preserve">序号{n}：{name}</w:t></w:r></w:p><w:p/>')
                    s = s[:i0 + m.start()] + ins + s[i0 + m.start():]
                    data = s.encode("utf-8")
                zout.writestr(info, data)
        shutil.move(f + ".tmp", f)
        print(f"序号{n}: docx标题段已插入")
        continue

    # --- PDF：渲染首页 → 加标题 → 整页替换 ---
    png = render_first(f, f"i{n}")
    im = Image.open(png).convert("RGB")
    W, H = im.size
    blank = top_blank_px(im)
    band_px = int(a.band_pt * a.dpi / 72)
    fs_px = int(a.title_pt * a.dpi / 72)
    left_px = int(a.left_pt * a.dpi / 72)
    title = f"序号{n}：{name}"

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
    size = fs_px
    while True:
        font = ImageFont.truetype(FONT, size)
        x_start = left_px if a.align == "left" else (W - int(dr.textlength(title, font=font))) // 2
        if x_start + dr.textlength(title, font=font) <= W - int(12 * a.dpi / 72) or size <= 10:
            break
        size -= 1
    dr.rectangle([0, 0, W, ty + size + int(4 * a.dpi / 72)], fill="white")
    dr.text((x_start, ty), title, fill="black", font=font)

    page_pdf = os.path.join(WORK, f"i{n}.pdf")
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
    print(f"序号{n}: {mode} {blank_pt}pt → 共{len(PdfReader(f).pages)}页")
print("全部完成")
