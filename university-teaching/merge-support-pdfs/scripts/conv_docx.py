# -*- coding: utf-8 -*-
"""批量 docx→PDF（Word COM 单实例）。跳过已存在的PDF；--force 全部重转。
用法: python conv_docx.py --folder <材料目录> [--out <PDF目录>] [--force] [--skip-prefix a,b]
经验：Word COM 传正斜杠路径会静默失败——路径必须 os.path.normpath；
     导出后立即被杀毒/索引器占用会报“只读文件”——export_with_retry 重试；
     脚本崩溃会遗留隐藏 WINWORD 占用文件——taskkill /F /IM WINWORD.EXE 后重试。
"""
import argparse, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
import win32com.client

ap = argparse.ArgumentParser()
ap.add_argument("--folder", required=True)
ap.add_argument("--out", default=None, help="PDF输出目录，默认 <folder>/_pdf")
ap.add_argument("--force", action="store_true", help="删除已转换PDF后全部重转")
ap.add_argument("--skip-prefix", default="~$", help="逗号分隔的跳过文件前缀")
a = ap.parse_args()

SRC = os.path.normpath(a.folder)
DST = os.path.normpath(a.out or os.path.join(SRC, "_pdf"))
os.makedirs(DST, exist_ok=True)
skip = tuple(p for p in a.skip_prefix.split(",") if p)

def numkey(f):
    m = re.match(r"^(\d+)", f)
    return int(m.group(1)) if m else 10**9

docx_files = sorted(
    [f for f in os.listdir(SRC)
     if f.lower().endswith(".docx") and not f.startswith(skip)],
    key=lambda f: (numkey(f), f))

if a.force:
    for f in docx_files:
        p = os.path.join(DST, os.path.splitext(f)[0] + ".pdf")
        if os.path.exists(p):
            os.remove(p)

def export_with_retry(doc, path, tries=4, wait=2):
    """导出后立即被杀毒/索引器瞬时占用会报“只读文件”——重试若干次"""
    last = None
    for k in range(tries):
        try:
            doc.ExportAsFixedFormat(os.path.normpath(path), 17)  # 17 = PDF
            return
        except Exception as e:
            last = e
            time.sleep(wait)
    raise last

w = win32com.client.Dispatch("Word.Application")
w.Visible = False
w.DisplayAlerts = 0
fail = []
for f in docx_files:
    out = os.path.join(DST, os.path.splitext(f)[0] + ".pdf")
    if os.path.exists(out):
        print("skip:", f[:44]); continue
    try:
        d = w.Documents.Open(os.path.normpath(os.path.join(SRC, f)), ReadOnly=True)
        export_with_retry(d, out)
        d.Close(False)
        print("ok:", f[:44])
    except Exception as e:
        fail.append(f)
        print("FAIL:", f[:44], str(e)[:90])
try:
    w.Quit()
except Exception:
    pass
print("完成，失败数:", len(fail))
sys.exit(1 if fail else 0)
