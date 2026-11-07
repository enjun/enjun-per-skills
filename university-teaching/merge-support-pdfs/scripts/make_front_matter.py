# -*- coding: utf-8 -*-
"""生成封面、目录（两遍法回填真实页码）、分类标题页、整册页码戳，输出 pages.json 供装配。
用法:
  python make_front_matter.py --folder <材料目录> [--names-xlsx <记录表.xlsx>] \
    [--cats "1:学科专业建设:1:9,..."] [--cover-lines "行1|行2|..."]
页码规则：封面无页码不盖戳；目录页从1起；每个分类占1页标题页计入页码。
"""
import argparse, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
import win32com.client
from openpyxl import load_workbook
from pypdf import PdfReader, PdfWriter

ap = argparse.ArgumentParser()
ap.add_argument("--folder", required=True)
ap.add_argument("--names-xlsx", default=None)
ap.add_argument("--cats", default="1:学科专业建设:1:9,2:师资队伍:10:17,3:教学平台:18:29,"
                                 "4:科研平台:30:42,5:教学成果:43:46,6:科研成果:47:50,7:人才培养:51:54")
ap.add_argument("--cover-lines", default="广东技术师范大学|“工业智能与安全”计算机科学拔尖|人才培养创新实验区|支　撑　材　料")
a = ap.parse_args()

HB = os.path.normpath(a.folder)    # Word COM 传正斜杠路径会静默失败，必须归一化
PDF = os.path.join(HB, "_pdf")
os.makedirs(PDF, exist_ok=True)

CATS = []
for part in a.cats.split(","):
    c, cname, lo, hi = part.split(":")
    CATS.append((int(c), cname, int(lo), int(hi)))
COVER_LINES = a.cover_lines.split("|")

def item_pdf(n):
    for d in (PDF, HB):
        for f in os.listdir(d):
            if re.match(rf"^{n}([\s\-（]|$)", f) and f.lower().endswith(".pdf"):
                return os.path.join(d, f)
    raise FileNotFoundError(n)

def pdf_pages(path):
    return len(PdfReader(path).pages)

wb = load_workbook(a.names_xlsx or os.path.join(HB, "材料清单记录表.xlsx"))
ws = wb.worksheets[0]
cur, names = None, {}
for r in range(2, ws.max_row + 1):
    if ws.cell(r, 1).value: cur = ws.cell(r, 1).value
    names[ws.cell(r, 2).value] = str(ws.cell(r, 3).value)

items = []
for c, cname, lo, hi in CATS:
    for n in range(lo, hi + 1):
        items.append((c, n, pdf_pages(item_pdf(n))))

import time
def export_with_retry(doc, path, tries=4, wait=2):
    """导出后立即被杀毒/索引器瞬时占用会导致“只读文件”错误——重试若干次"""
    last = None
    for k in range(tries):
        try:
            doc.ExportAsFixedFormat(os.path.normpath(path), 17)
            return
        except Exception as e:
            last = e
            time.sleep(wait)
    raise last

w = win32com.client.Dispatch("Word.Application")
w.Visible = False
w.DisplayAlerts = 0
import atexit
def _quit_word(app=w): app.Quit()
atexit.register(_quit_word)

def new_doc(center_vertical=False):
    d = w.Documents.Add()
    d.PageSetup.PageWidth, d.PageSetup.PageHeight = 595.3, 841.9  # A4（勿用默认Letter）
    d.PageSetup.TopMargin = d.PageSetup.BottomMargin = 72
    d.PageSetup.LeftMargin = d.PageSetup.RightMargin = 90
    if center_vertical:
        d.Sections(1).PageSetup.VerticalAlignment = 1  # 垂直居中
    return d

# 1) 封面（首段段前距会被后续段落继承，第二段起必须清零，否则封面溢出为两页）
d = new_doc()
sel = w.Selection
sel.ParagraphFormat.Alignment = 1
sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
sel.Font.Size = 28; sel.Font.Bold = True
sel.ParagraphFormat.SpaceBefore = 150
for i, line in enumerate(COVER_LINES):
    if i >= 1:
        sel.ParagraphFormat.SpaceBefore = 30
    sel.TypeText(line)
    if i < len(COVER_LINES) - 1:
        sel.TypeParagraph()
cover_pdf = os.path.normpath(os.path.join(PDF, "_cover.pdf"))
export_with_retry(d, cover_pdf)
d.Close(False)
n_cover = pdf_pages(cover_pdf)
assert n_cover == 1, f"封面溢出为{n_cover}页：调小字号或段前距"
print("封面页数:", n_cover)

# 2) 分类标题页（每类独立文档：同一文档内分页符后的段前距不生效、无法垂直居中；
#    每类单独文档并设置“节垂直居中”，才能保证大标题位于页面中部）
div_files = []
for c, cname, lo, hi in CATS:
    d = new_doc(center_vertical=True)
    sel = w.Selection
    sel.ParagraphFormat.Alignment = 1
    sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
    sel.Font.Size = 40; sel.Font.Bold = True
    sel.TypeText(f"{c}. {cname}")
    out = os.path.normpath(os.path.join(PDF, f"_div_{c}.pdf"))
    export_with_retry(d, out)
    d.Close(False)
    assert pdf_pages(out) == 1, f"分类{c}标题页溢出"
    div_files.append(out)
n_div = len(div_files)
print("分类标题页数:", n_div)

w2 = PdfWriter()
for f in div_files:
    for p in PdfReader(f).pages:
        w2.add_page(p)
dividers = os.path.join(PDF, "_dividers.pdf")
with open(dividers, "wb") as fh:
    w2.write(fh)

# 3) 目录（两遍法：第一遍占位符定页数，第二遍回填真实页码；两遍条目文本相同则页数稳定）
def build_toc(pages_map):
    d = new_doc()
    sel = w.Selection
    sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
    sel.Font.Size = 16; sel.Font.Bold = True
    sel.ParagraphFormat.Alignment = 1
    sel.TypeText("目　录")
    sel.TypeParagraph()
    for c, cname, lo, hi in CATS:
        sel.ParagraphFormat.Alignment = 0
        sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
        sel.Font.Size = 12; sel.Font.Bold = True
        sel.ParagraphFormat.TabStops.Add(415, 2, 1)  # 右对齐+点线引导符（415pt=A4可用宽）
        sel.TypeText(f"{c}. {cname}")
        if pages_map:
            sel.TypeText("\t" + str(pages_map["cats"][c]))
        sel.TypeParagraph()
        for (cc, n, pp) in items:
            if cc != c: continue
            sel.Font.Name = "宋体"; sel.Font.NameFarEast = "宋体"
            sel.Font.Size = 10.5; sel.Font.Bold = False
            sel.ParagraphFormat.TabStops.Add(415, 2, 1)
            sel.TypeText(f"　　序号{n}　{names[n]}")
            if pages_map:
                sel.TypeText("\t" + str(pages_map["items"][n]))
            sel.TypeParagraph()
        sel.Font.Bold = False
    out = os.path.normpath(os.path.join(PDF, "_toc.pdf"))
    export_with_retry(d, out)
    d.Close(False)
    return pdf_pages(out)

t1 = build_toc(None)
print("TOC 页数(第一遍):", t1)

# 页码映射：目录从1起；每个分类先占1页标题页
pages_map = {"cats": {}, "items": {}}
cur = t1
for c, cname, lo, hi in CATS:
    cur += 1
    pages_map["cats"][c] = cur
    for (cc, n, pp) in items:
        if cc == c:
            cur += pp
            pages_map["items"][n] = cur - pp + 1
t2 = build_toc(pages_map)
print("TOC 页数(第二遍):", t2)
assert t2 == t1, f"TOC页数变化 {t1}->{t2}，目录条目换行数不稳定，需检查"

total = n_cover + t2 + n_div + sum(pp for _, _, pp in items)
print("整册总页数:", total)

json.dump({"cover": n_cover, "t": t2, "div": n_div, "total": total,
           "pages_map": pages_map, "cats": CATS, "items": items},
          open(os.path.join(PDF, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False)

# 4) 页码戳：从目录起共 (t2+分类页+条目页) 页
n_stamp = t2 + n_div + sum(pp for _, _, pp in items)
d = new_doc()
fp = d.Sections(1).Footers(1).Range  # 注意：Document无Footers，须经Sections
fp.Font.Name = "宋体"; fp.Font.Size = 10.5
fp.Fields.Add(fp, 33)                # 33 = wdFieldPage
fp.ParagraphFormat.Alignment = 2     # 域插入后再设右对齐（先设会被重置为左对齐）
sel = w.Selection
for i in range(n_stamp - 1):
    sel.InsertBreak(7)               # 7 = wdPageBreak
export_with_retry(d, os.path.join(PDF, "_stamp.pdf"))
d.Close(False)
print("页码戳页数:", pdf_pages(os.path.join(PDF, "_stamp.pdf")))
w.Quit()
print("done")
