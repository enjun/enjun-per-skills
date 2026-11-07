# -*- coding: utf-8 -*-
"""生成封面、目录（两遍法回填真实页码）、分类标题页、整册页码戳，输出 pages.json 供装配。
用法:
  python make_front_matter.py --folder <材料目录> \
    --cats "分类A:1-9|分类B:3,4,5" --cover-lines "封面行1|封面行2"
  --cats 必需（每次任务不同）：分类名:编号范围，多分类用 | 分隔，范围支持 a-b 或逗号列表；
  --cover-lines 必需：封面文字行，用 | 分隔。
  --names-xlsx 可选：名称映射表（自动识别编号列与名称列），缺省用文件名解析的名称。
未归入分类的编号文件会告警并跳过。
页码规则：封面无页码不盖戳；目录页从1起；每个分类占1页标题页计入页码。
"""
import argparse, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
import win32com.client
from pypdf import PdfReader, PdfWriter
from openpyxl import load_workbook

ap = argparse.ArgumentParser()
ap.add_argument("--folder", required=True)
ap.add_argument("--cats", required=True,
                help='分类定义："分类名:编号范围"，多分类用 | 分隔；范围支持 a-b 区间或逗号列表')
ap.add_argument("--cover-lines", required=True, help="封面文字行，以 | 分隔")
ap.add_argument("--names-xlsx", default=None,
                help="可选：名称映射表（自动识别编号列与名称列）；缺省用文件名解析的名称")
ap.add_argument("--title-pt", type=int, default=40, help="分类标题页字号")
a = ap.parse_args()

HB = os.path.normpath(a.folder)   # Word COM 正斜杠路径会静默失败，必须归一化
PDF = os.path.join(HB, "_pdf")
os.makedirs(PDF, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import catalog

def expand(spec):
    """'1-9' → [1..9]；'3,4' → [3,4]（均为首段数字）"""
    out = []
    for piece in spec.split(","):
        piece = piece.strip()
        m = re.match(r"^(\d+)(?:\s*[-–]\s*(\d+))?$", piece)
        if m:
            lo = int(m.group(1))
            hi = int(m.group(2) or m.group(1))
            out += list(range(lo, hi + 1))
        else:
            out.append(int(piece))
    return out

# 分类：[(名称, 首段数字列表)]，保持给定顺序
cats = []
assigned = set()
for part in a.cats.split("|"):
    cname, spec = part.split(":", 1)
    firsts = expand(spec)        # 编号归属按【首段数字】
    cats.append((cname.strip(), firsts))
    assigned |= set(firsts)

# 文件清单：[(路径, first_seg, key, title)]，key 升序
files = catalog(HB)

# 名称覆盖（可选xlsx：自动识别纯数字列为编号、相邻长文本列为名称；按首段匹配）
name_map = {}
if a.names_xlsx and os.path.exists(os.path.normpath(a.names_xlsx)):
    wbn = load_workbook(os.path.normpath(a.names_xlsx))
    wsn = wbn.worksheets[0]
    for row in wsn.iter_rows():
        vals = [c.value for c in row]
        int_cols = [i for i, v in enumerate(vals) if isinstance(v, (int, float))]
        if not int_cols:
            continue
        key0 = int(vals[int_cols[0]])
        texts = [str(v).strip() for i, v in enumerate(vals)
                 if isinstance(v, str) and len(str(v).strip()) > 3 and i not in int_cols]
        if texts:
            name_map[key0] = texts[-1]

# 分配到分类（按首段数字）；显示名 = 清单表覆盖 或 文件名主干
assign = {cn: [] for cn, _ in cats}
unassigned = []
for (p, first_seg, num_str, key, title) in files:
    hit = None
    for cname, firsts in cats:
        if first_seg in firsts:
            hit = cname
            break
    if hit is None:
        unassigned.append((p, title))
        continue
    nm = name_map.get(first_seg, title)
    assign[hit].append((p, nm, key))
for cn in assign:
    assign[cn].sort(key=lambda x: x[2])
if unassigned:
    print("!! 未归入分类（跳过）:")
    for (p, ti) in unassigned:
        print("   ", os.path.basename(p)[:50])

# --- Word COM ---
w = win32com.client.Dispatch("Word.Application")
w.Visible = False
w.DisplayAlerts = 0

def new_doc(center_vertical=False):
    d = w.Documents.Add()
    d.PageSetup.PageWidth, d.PageSetup.PageHeight = 595.3, 841.9  # A4（勿用默认Letter）
    d.PageSetup.TopMargin = d.PageSetup.BottomMargin = 72
    d.PageSetup.LeftMargin = d.PageSetup.RightMargin = 90
    if center_vertical:
        d.Sections(1).PageSetup.VerticalAlignment = 1  # 垂直居中
    return d

def export_pdf(d, out):
    import time
    out = os.path.normpath(out)  # 正斜杠/瞬时占用会报“只读文件”，归一化+重试
    last = None
    for k in range(4):
        try:
            d.ExportAsFixedFormat(out, 17)  # 17 = PDF
            return
        except Exception as e:
            last = e
            time.sleep(2)
    raise last

# 1) 封面（段前距继承：第二行起清零，否则溢出为两页）
lines = a.cover_lines.split("|")
d = new_doc()
sel = w.Selection
sel.ParagraphFormat.Alignment = 1
sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
sel.Font.Size = 28; sel.Font.Bold = True
sel.ParagraphFormat.SpaceBefore = 150
for i, line in enumerate(lines):
    if i >= 1:
        sel.ParagraphFormat.SpaceBefore = 30
    sel.TypeText(line)
    if i < len(lines) - 1:
        sel.TypeParagraph()
cover_pdf = os.path.normpath(os.path.join(PDF, "_cover.pdf"))
export_pdf(d, cover_pdf)
d.Close(False)
n_cover = len(PdfReader(cover_pdf).pages)
assert n_cover == 1, f"封面溢出为{n_cover}页"
print("封面页数:", n_cover)

# 2) 分类标题页（每类独立文档+节垂直居中，保证标题位于页面中部）
for idx, (cname, _) in enumerate(cats):
    d = new_doc(center_vertical=True)
    sel = w.Selection
    sel.ParagraphFormat.Alignment = 1
    sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
    sel.Font.Size = a.title_pt; sel.Font.Bold = True
    sel.TypeText(f"{idx + 1}. {cname}")
    out = os.path.normpath(os.path.join(PDF, f"_div_{idx + 1}.pdf"))
    export_pdf(d, out)
    d.Close(False)
    assert len(PdfReader(out).pages) == 1, f"分类{cname}标题页溢出"
print("分类标题页:", len(cats), "页")

from pypdf import PdfWriter as _PW
w2 = _PW()
for idx, (cname, _) in enumerate(cats):
    for p in PdfReader(os.path.join(PDF, f"_div_{idx + 1}.pdf")).pages:
        w2.add_page(p)
dividers = os.path.normpath(os.path.join(PDF, "_dividers.pdf"))
with open(dividers, "wb") as fh:
    w2.write(fh)

# 3) 目录（两遍法）
def build_toc(pages_map):
    d = new_doc()
    sel = w.Selection
    sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
    sel.Font.Size = 16; sel.Font.Bold = True
    sel.ParagraphFormat.Alignment = 1
    sel.TypeText("目　录")
    sel.TypeParagraph()
    for idx, (cname, nums) in enumerate(cats):
        sel.ParagraphFormat.Alignment = 0
        sel.Font.Name = "黑体"; sel.Font.NameFarEast = "黑体"
        sel.Font.Size = 12; sel.Font.Bold = True
        sel.ParagraphFormat.TabStops.Add(415, 2, 1)  # 右对齐+点线引导符（415pt=A4可用宽）
        sel.TypeText(f"{idx + 1}. {cname}")
        if pages_map:
            sel.TypeText("\t" + str(pages_map["cats"][cname]))
        sel.TypeParagraph()
        for (p, nm, key) in assign[cname]:
            sel.Font.Name = "宋体"; sel.Font.NameFarEast = "宋体"
            sel.Font.Size = 10.5; sel.Font.Bold = False
            sel.ParagraphFormat.TabStops.Add(415, 2, 1)
            sel.TypeText(f"　　{nm}")
            if pages_map:
                sel.TypeText("\t" + str(pages_map["items"][nm]))
            sel.TypeParagraph()
        sel.Font.Bold = False
    out = os.path.normpath(os.path.join(PDF, "_toc.pdf"))
    export_pdf(d, out)
    d.Close(False)
    return len(PdfReader(out).pages)

cat_order = [cn for cn, _ in cats]
t1 = build_toc(None)
print("TOC 页数(第一遍):", t1)

pages_map = {"cats": {}, "items": {}}
cur = t1
for cn, nums in cats:
    cur += 1
    pages_map["cats"][cn] = cur
    for (p, nm, key) in assign[cn]:
        pp = len(PdfReader(p).pages)
        cur += pp
        pages_map["items"][nm] = cur - pp + 1
t2 = build_toc(pages_map)
assert t2 == t1, f"TOC页数变化 {t1}->{t2}，目录条目换行不稳定"
print("TOC 页数(第二遍):", t2)

total = n_cover + t2 + n_div + sum(len(PdfReader(x[0]).pages) for cn in cat_order for x in assign[cn])
print("整册总页数:", total)

json.dump({"cover": n_cover, "t": t2, "div": n_div, "total": total,
           "pages_map": pages_map,
           "cat_order": cat_order,
           "assign": {cn: [x[1] for x in assign[cn]] for cn in cat_order}},
          open(os.path.join(PDF, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False)

# 4) 页码戳：从目录起共 (t2+分类页+条目页) 页
n_stamp = t2 + n_div + sum(len(assign[cn]) for cn in cat_order)
d = new_doc()
fp = d.Sections(1).Footers(1).Range  # Document无Footers，须经Sections
fp.Font.Name = "宋体"; fp.Font.Size = 10.5
fp.Fields.Add(fp, 33)                # 33 = wdFieldPage
fp.ParagraphFormat.Alignment = 2     # 域插入后再设右对齐（先设会被重置）
sel = w.Selection
for i in range(n_stamp - 1):
    sel.InsertBreak(7)               # 7 = wdPageBreak
stamp_pdf = os.path.normpath(os.path.join(PDF, "_stamp.pdf"))
export_pdf(d, stamp_pdf)
d.Close(False)
print("页码戳页数:", len(PdfReader(stamp_pdf).pages))
w.Quit()
print("done")
