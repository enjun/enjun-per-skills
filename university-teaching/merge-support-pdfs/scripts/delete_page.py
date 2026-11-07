# -*- coding: utf-8 -*-
"""删除 PDF 的第 k 页（1-based）。
用法: python delete_page.py --file <pdf> --page 3
注意：若被删页带标题条/正属于某个序号，删除后请同步更新记录表并重跑整册装配。
"""
import argparse, sys, os
sys.stdout.reconfigure(encoding="utf-8")
from pypdf import PdfReader, PdfWriter

ap = argparse.ArgumentParser()
ap.add_argument("--file", required=True)
ap.add_argument("--page", type=int, required=True, help="1-based")
a = ap.parse_args()

r = PdfReader(a.file)
n = len(r.pages)
assert 1 <= a.page <= n, f"页码超出范围 1..{n}"
w = PdfWriter()
for i, p in enumerate(r.pages):
    if i != a.page - 1:
        w.add_page(p)
tmp = a.file + ".tmp"
with open(tmp, "wb") as fh:
    w.write(fh)
os.replace(tmp, a.file)
print(f"已删除第{a.page}页，剩 {n-1} 页")
