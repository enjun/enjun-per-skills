# -*- coding: utf-8 -*-
"""文件名解析与目录清单。
命名形式多样：49-xxx.pdf、1.2.1+xxx.docx、12 xxx.pdf、1-2-3-xxx.pdf 等。
策略：首段数字用于分类归属与主排序；完整编号段用于细分排序；
标题默认用文件名主干原样（避免把年份等吸进编号），可被清单表覆盖。
"""
import os, re

LEAD_RE = re.compile(r"^\s*[（(]?\s*(\d+(?:\s*[.．\-—–_、]\s*\d+)*)")

def parse_stem(stem):
    """返回 (first_seg, num_str, key, title)。
    first_seg = 第一段数字（分类归属用）；num_str = 完整编号前缀；
    key = 编号各段数字元组（排序用）；title = 文件名主干原样。"""
    stem = stem.strip()
    m = LEAD_RE.match(stem)
    if not m:
        return 10**9, "", (10**9,), stem
    num_str = re.sub(r"\s+", "", m.group(1))
    segs = [int(x) for x in re.findall(r"\d+", num_str)]
    title = stem.strip()
    return segs[0], num_str, tuple(segs), title

def catalog(folder):
    """扫描目录，返回 [(路径, first_seg, num_str, key, title), ...] 按 key 升序。"""
    out = []
    for f in os.listdir(folder):
        if not f.lower().endswith((".pdf", ".docx")) or f.startswith("~$") or f.startswith("_"):
            continue
        p = os.path.join(folder, f)
        fs, ns, k, ti = parse_stem(os.path.splitext(f)[0])
        out.append((p, fs, ns, k, ti))
    out.sort(key=lambda x: x[3])
    return out
