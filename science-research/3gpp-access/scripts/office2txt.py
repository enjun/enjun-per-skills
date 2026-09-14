#!/usr/bin/env python3
"""Extract text from docx/pptx files inside a (possibly nested) zip.

Usage: office2txt.py <file.docx|file.pptx|file.zip>  → text to stdout
"""
import io
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')


def xml_text(xml_bytes, para_tag, run_tag):
    xml = xml_bytes.decode('utf-8', errors='ignore')
    paras = []
    for p in re.findall(rf'<{para_tag}[ >].*?</{para_tag}>', xml, re.S):
        runs = re.findall(rf'<{run_tag}[^>]*>(.*?)</{run_tag}>', p, re.S)
        line = ''.join(re.sub(r'<[^>]+>', '', r) for r in runs)
        for a, b in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")):
            line = line.replace(a, b)
        if line.strip():
            paras.append(line.strip())
    return paras


def from_inner(data):
    """data = bytes of a docx/pptx (itself a zip). Return text lines."""
    zf = zipfile.ZipFile(io.BytesIO(data))
    if any(n.endswith('word/document.xml') for n in zf.namelist()):
        return xml_text(zf.read('word/document.xml'), 'w:p', 'w:t')
    slides = sorted((n for n in zf.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                    key=lambda n: int(re.search(r'(\d+)\.xml', n).group(1)))
    out = []
    for i, n in enumerate(slides, 1):
        out.append(f'--- Slide {i} ---')
        out.extend(xml_text(zf.read(n), 'a:p', 'a:t'))
    return out


def main():
    path = sys.argv[1]
    with zipfile.ZipFile(path) as zf:
        targets = [n for n in zf.namelist() if n.lower().endswith(('.docx', '.pptx'))
                   and not n.startswith('__MACOSX')]
        if not targets:
            sys.exit(f'no docx/pptx inside {path}')
        for t in sorted(targets):
            if len(targets) > 1:
                print(f'\n===== {t} =====')
            try:
                lines = from_inner(zf.read(t))
            except zipfile.BadZipFile:
                print(f'({t}: not a readable office file)', file=sys.stderr)
                continue
            for line in lines:
                print(line)


if __name__ == '__main__':
    main()
