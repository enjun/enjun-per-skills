# -*- coding: utf-8 -*-
"""两阶段装配：PyMuPDF 装配内容页（含旋转烘焙/分类标题页）→ pypdf 叠加右下角页码戳 → 自检。
用法:
  python assemble.py --folder <材料目录> [--out 支撑材料.pdf]
顺序：_cover.pdf(无页码) → _toc.pdf → [_dividers.pdf第ci页 + 该分类各项PDF] × N
关键经验：
  1. fitz 页对象没有 pypdf 的合并方法——页码戳必须用 pypdf 在“writer 的页对象”上叠加
     （叠加在读取器页对象上的修改不会进入成品）；
  2. 带 /Rotate 的源页先烘焙为正向图像页（fitz 阶段完成），否则叠加/页码旋转错位；
  3. 叠加偏移 tx=目标宽-595.32、ty=目标高-841.92（不截断），任何页面尺寸都对齐右下角。
"""
import argparse, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
import fitz
from pypdf import PdfReader, PdfWriter, Transformation

ap = argparse.ArgumentParser()
ap.add_argument("--folder", required=True)
ap.add_argument("--out", default="支撑材料.pdf")
a = ap.parse_args()

HB = a.folder
PDF = os.path.join(HB, "_pdf")
meta = json.load(open(os.path.join(PDF, "pages.json"), encoding="utf-8"))
total_expected = meta["total"]
cats = meta["cats"]
n_cover = meta["cover"]
pm_cats = meta["pages_map"]["cats"]

def item_pdf(n):
    for d in (PDF, HB):
        for f in os.listdir(d):
            if re.match(rf"^{n}([\s\-（]|$)", f) and f.lower().endswith(".pdf"):
                return os.path.join(d, f)
    raise FileNotFoundError(n)

ordered = [(os.path.join(PDF, "_cover.pdf"), None),
           (os.path.join(PDF, "_toc.pdf"), None)]
for c, cname, lo, hi in cats:
    ordered.append((os.path.join(PDF, "_dividers.pdf"), int(c)))
    for n in range(lo, hi + 1):
        ordered.append((item_pdf(n), None))

# ---- 阶段一：PyMuPDF 装配内容 ----
new = fitz.open()
for path, div_page in ordered:
    rsrc = fitz.open(path)
    first_new = new.page_count
    if div_page is not None:
        # 仅取该分类的标题页（_dividers.pdf 第 div_page 页，1-based）
        new.insert_pdf(rsrc, from_page=div_page - 1, to_page=div_page - 1)
    else:
        for i in range(rsrc.page_count):
            if rsrc[i].rotation:
                # 带 /Rotate 的页烘焙为正向图像页（否则页码/叠加旋转错位）
                pix = rsrc[i].get_pixmap(dpi=200)
                w, h = pix.width * 72 / 200, pix.height * 72 / 200
                np_ = new.new_page(width=w, height=h)
                np_.insert_image(np_.rect, stream=pix.tobytes("jpeg", jpg_quality=92))
            else:
                new.insert_pdf(rsrc, from_page=i, to_page=i)
    rsrc.close()
content_pdf = os.path.join(PDF, "_content.pdf")
new.save(content_pdf, garbage=4, deflate=True, clean=True)
new.close()
print("内容装配页数:", fitz.open(content_pdf).page_count)

# ---- 阶段二：pypdf 叠加右下角页码戳 ----
stamp = PdfReader(os.path.join(PDF, "_stamp.pdf"))
content = PdfReader(content_pdf)
w = PdfWriter()
for i, p in enumerate(content.pages):
    w.add_page(p)
# 关键：对 writer 的页对象叠加（对读取器页对象的修改不会进入成品）
for i, pg in enumerate(w.pages):
    if i == 0:   # 封面无页码
        continue
    sp = stamp.pages[i - 1]   # 页码从目录=1起，戳第 i-1 页 = 数字 i
    tw, th = float(pg.mediabox.width), float(pg.mediabox.height)
    tx, ty = tw - 595.32, th - 841.92
    if abs(tx) < 0.5 and abs(ty) < 0.5:
        pg.merge_page(sp, over=True)
    else:
        pg.merge_transformed_page(sp, Transformation().translate(tx, ty), over=True)

out = os.path.join(HB, a.out)
with open(out, "wb") as fh:
    w.write(fh)
print("written:", out, "| 页数:", len(PdfReader(out).pages), "| 预期:", total_expected)
print("页码覆盖页数:", len(PdfReader(out).pages) - 1)

# ---- 自检 ----
d = fitz.open(out)
N = d.xref_length()
dangling = 0
for x in range(1, N):
    try:
        s = d.xref_object(x, compressed=False)
    except Exception:
        continue
    for m in re.finditer(r"(\d+)\s+0\s+R", s):
        n = int(m.group(1))
        if n == 0 or n >= N:
            dangling += 1
bad_num = []
for i in range(1, d.page_count):
    p = d[i]
    clip = fitz.Rect(p.rect.x1 - 120, p.rect.y1 - 60, p.rect.x1, p.rect.y1)
    if str(i) not in p.get_text(clip=clip):
        bad_num.append(i + 1)
rot = [i + 1 for i, p in enumerate(d) if p.rotation]
print("悬空引用:", dangling, "| 页码缺失/不符页:", bad_num[:8] or "无", "| 旋转页:", rot or "无")
print("分类起始页（物理页）:")
for c, cname, lo, hi in cats:
    print(f"  {c}. {cname} → 第{pm_cats[str(c)] + n_cover}页")
sys.exit(0 if (dangling == 0 and not bad_num and not rot) else 1)
