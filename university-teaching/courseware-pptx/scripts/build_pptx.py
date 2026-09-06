# -*- coding: utf-8 -*-
"""
第1周：Python语言导论与开发环境搭建 - 课件PPT生成脚本
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from copy import deepcopy
from lxml import etree

# ============== 主题配色（Python 风格：蓝 + 黄） ==============
PY_BLUE = RGBColor(0x30, 0x69, 0x98)       # 深蓝 - 主色
PY_BLUE_LIGHT = RGBColor(0x4B, 0x8B, 0xC8)  # 浅蓝 - 次主色
PY_YELLOW = RGBColor(0xFF, 0xD4, 0x3B)      # 标志黄 - 强调色
PY_DARK = RGBColor(0x1E, 0x2A, 0x38)        # 深灰 - 文字主色
PY_GRAY = RGBColor(0x5A, 0x66, 0x73)        # 中灰 - 副文字
PY_BG_LIGHT = RGBColor(0xF5, 0xF7, 0xFA)    # 浅灰背景
PY_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PY_CODE_BG = RGBColor(0x2B, 0x3A, 0x45)     # 代码块深色背景
PY_CODE_FG = RGBColor(0xE8, 0xE8, 0xE8)
PY_ACCENT_GREEN = RGBColor(0x37, 0xB2, 0x4D)
PY_ACCENT_RED = RGBColor(0xE6, 0x4A, 0x4A)
PY_ACCENT_ORANGE = RGBColor(0xF5, 0x9E, 0x42)

# ============== 页面尺寸 16:9 ==============
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height

BLANK_LAYOUT = prs.slide_layouts[6]

# ============== 工具函数 ==============
def add_rect(slide, x, y, w, h, fill_color, line_color=None, shadow=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(0.75)
    if not shadow:
        # 移除默认阴影
        sp = shape.shadow
        try:
            sp.inherit = False
        except Exception:
            pass
    return shape

def add_round_rect(slide, x, y, w, h, fill_color, line_color=None, corner=0.08):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(0.75)
    # 调整圆角比例
    shape.adjustments[0] = corner
    try:
        shape.shadow.inherit = False
    except Exception:
        pass
    return shape

def add_text(slide, x, y, w, h, text, font_size=18, bold=False, color=PY_DARK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font_name="Microsoft YaHei",
             line_spacing=1.2):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    lines = text.split('\n') if isinstance(text, str) else text
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = font_name
        # 设置中文字体
        rPr = run._r.get_or_add_rPr()
        eastAsian = rPr.find(qn('a:ea'))
        if eastAsian is None:
            eastAsian = etree.SubElement(rPr, qn('a:ea'))
        eastAsian.set('typeface', font_name)
    return tb

def add_bullets(slide, x, y, w, h, items, font_size=16, color=PY_DARK,
                line_spacing=1.25, bullet_char="●", bullet_color=PY_BLUE_LIGHT,
                font_name="Microsoft YaHei"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        # bullet
        bullet_run = p.add_run()
        bullet_run.text = f"{bullet_char}  "
        bullet_run.font.size = Pt(font_size)
        bullet_run.font.color.rgb = bullet_color
        bullet_run.font.bold = True
        bullet_run.font.name = font_name
        # text - support simple bold markdown via **xxx**
        if isinstance(item, tuple):
            main_text, sub_text = item
            r1 = p.add_run()
            r1.text = main_text
            r1.font.size = Pt(font_size)
            r1.font.color.rgb = color
            r1.font.bold = True
            r1.font.name = font_name
            if sub_text:
                r2 = p.add_run()
                r2.text = sub_text
                r2.font.size = Pt(font_size - 1)
                r2.font.color.rgb = PY_GRAY
                r2.font.name = font_name
        else:
            # 支持 **bold** 简单标记
            parts = item.split('**')
            for j, part in enumerate(parts):
                if not part:
                    continue
                r = p.add_run()
                r.text = part
                r.font.size = Pt(font_size)
                r.font.color.rgb = color
                r.font.bold = (j % 2 == 1)
                r.font.name = font_name
                rPr = r._r.get_or_add_rPr()
                ea = rPr.find(qn('a:ea'))
                if ea is None:
                    ea = etree.SubElement(rPr, qn('a:ea'))
                ea.set('typeface', font_name)
    return tb

def add_code_block(slide, x, y, w, h, code, font_size=12, lang="python"):
    """添加带标题栏的代码块"""
    # 顶部标签栏
    title_h = Inches(0.32)
    title = add_round_rect(slide, x, y, w, title_h, PY_CODE_BG, corner=0.5)
    # mac 风格圆点
    dot_colors = [RGBColor(0xFF,0x5F,0x56), RGBColor(0xFF,0xBD,0x2E), RGBColor(0x27,0xC9,0x3F)]
    for i, c in enumerate(dot_colors):
        d = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            x + Inches(0.18) + Inches(0.18)*i, y + Inches(0.10),
            Inches(0.13), Inches(0.13))
        d.fill.solid()
        d.fill.fore_color.rgb = c
        d.line.fill.background()
    # 文件名
    add_text(slide, x + Inches(0.85), y, w - Inches(0.9), title_h,
             lang, font_size=11, color=RGBColor(0xB8,0xC2,0xCC),
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
    # 代码主体
    code_y = y + title_h
    code_h = h - title_h
    body = add_rect(slide, x, code_y, w, code_h, PY_CODE_BG)
    tb = slide.shapes.add_textbox(x + Inches(0.18), code_y + Inches(0.08),
                                  w - Inches(0.3), code_h - Inches(0.15))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for i, line in enumerate(code.split('\n')):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        r = p.add_run()
        r.text = line if line else " "
        r.font.size = Pt(font_size)
        r.font.color.rgb = PY_CODE_FG
        r.font.name = "Consolas"
        rPr = r._r.get_or_add_rPr()
        ea = rPr.find(qn('a:ea'))
        if ea is None:
            ea = etree.SubElement(rPr, qn('a:ea'))
        ea.set('typeface', "Consolas")

def add_page_header(slide, page_no, total_pages, section_title=""):
    """添加每页通用页眉：左侧色块 + 页码"""
    # 左上色条
    add_rect(slide, 0, 0, Inches(0.25), SLIDE_H, PY_BLUE)
    # 页码标识
    if page_no and total_pages:
        add_text(slide, SLIDE_W - Inches(1.4), Inches(0.18), Inches(1.2), Inches(0.3),
                 f"{page_no:02d} / {total_pages:02d}", font_size=10,
                 color=PY_GRAY, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    # 课程名（小字）
    add_text(slide, Inches(0.45), Inches(0.15), Inches(6), Inches(0.3),
             "Python 语言程序设计  ·  第 1 周", font_size=10,
             color=PY_GRAY, anchor=MSO_ANCHOR.MIDDLE)
    # 右上角小节标识
    if section_title:
        add_text(slide, Inches(6.5), Inches(0.15), Inches(5.5), Inches(0.3),
                 section_title, font_size=10, color=PY_BLUE_LIGHT,
                 align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, bold=True)

def add_section_title(slide, title, subtitle="", y_offset=Inches(0.7)):
    """大标题：左侧色块 + 主标题 + 副标题"""
    # 主标题左侧色块
    add_rect(slide, Inches(0.6), y_offset + Inches(0.05),
             Inches(0.12), Inches(0.7), PY_YELLOW)
    # 主标题
    add_text(slide, Inches(0.85), y_offset, Inches(11.5), Inches(0.8),
             title, font_size=32, bold=True, color=PY_BLUE,
             anchor=MSO_ANCHOR.MIDDLE)
    if subtitle:
        add_text(slide, Inches(0.85), y_offset + Inches(0.85),
                 Inches(11.5), Inches(0.4),
                 subtitle, font_size=14, color=PY_GRAY,
                 anchor=MSO_ANCHOR.TOP)

def add_footer(slide):
    """页脚"""
    add_rect(slide, 0, SLIDE_H - Inches(0.04), SLIDE_W, Inches(0.04), PY_BLUE)

# ============== 创建幻灯片 ==============
TOTAL = 22  # 预估总页数
page_counter = [0]

def new_slide(section_title=""):
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    page_counter[0] += 1
    add_page_header(slide, page_counter[0], TOTAL, section_title)
    add_footer(slide)
    # 背景浅色
    bg = add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, PY_WHITE)
    # 覆盖左上色条（避免被背景覆盖）
    add_rect(slide, 0, 0, Inches(0.25), SLIDE_H, PY_BLUE)
    return slide


# ============== Slide 1：封面 ==============
def slide_cover():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    # 全幅深蓝渐变背景（用纯色+色块模拟）
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, PY_BLUE)
    # 装饰斜块
    deco = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE,
        Inches(8.5), Inches(0), Inches(4.83), Inches(7.5))
    deco.fill.solid()
    deco.fill.fore_color.rgb = PY_BLUE_LIGHT
    deco.line.fill.background()

    deco2 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE,
        Inches(10.5), Inches(0), Inches(2.83), Inches(7.5))
    deco2.fill.solid()
    deco2.fill.fore_color.rgb = PY_YELLOW
    deco2.line.fill.background()
    # 装饰小圆
    for cx, cy, sz in [(1.2, 1.2, 0.4), (1.8, 0.7, 0.18), (2.3, 1.5, 0.22)]:
        c = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            Inches(cx), Inches(cy), Inches(sz), Inches(sz))
        c.fill.solid()
        c.fill.fore_color.rgb = PY_YELLOW
        c.line.fill.background()

    # "Wk 01" 大字标
    add_text(slide, Inches(0.8), Inches(2.0), Inches(3), Inches(0.6),
             "WEEK 01", font_size=20, bold=True, color=PY_YELLOW)
    # 主标题
    add_text(slide, Inches(0.8), Inches(2.6), Inches(9.5), Inches(1.4),
             "Python 语言导论", font_size=54, bold=True, color=PY_WHITE)
    add_text(slide, Inches(0.8), Inches(3.7), Inches(9.5), Inches(1.4),
             "与开发环境搭建", font_size=54, bold=True, color=PY_WHITE)
    # 副标题分隔线
    add_rect(slide, Inches(0.8), Inches(5.05), Inches(1.2), Inches(0.06), PY_YELLOW)
    # 副标题
    add_text(slide, Inches(0.8), Inches(5.2), Inches(9.5), Inches(0.5),
             "Introduction to Python & Development Environment Setup",
             font_size=18, color=PY_YELLOW)
    add_text(slide, Inches(0.8), Inches(5.8), Inches(9.5), Inches(0.5),
             "Python 语言程序设计 · 第 1 周",
             font_size=16, color=RGBColor(0xC9,0xD8,0xE6))
    # 底部信息
    add_text(slide, Inches(0.8), Inches(6.8), Inches(9), Inches(0.4),
             "授课教师 / 课件制作", font_size=12, color=PY_YELLOW)


# ============== Slide 2：本周目标 ==============
def slide_goals():
    slide = new_slide("本周概览")
    add_section_title(slide, "本周学习目标",
                       "Knowledge Goals & AI-Assisted Learning")

    # 左卡片：知识目标
    x = Inches(0.6); y = Inches(1.85); w = Inches(5.9); h = Inches(4.7)
    card1 = add_round_rect(slide, x, y, w, h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.05)
    # 卡片标题条
    add_rect(slide, x, y, w, Inches(0.7), PY_BLUE)
    add_text(slide, x + Inches(0.3), y, Inches(2.5), Inches(0.7),
             "📘 知识目标", font_size=18, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    # 数量徽章
    badge = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        x + w - Inches(0.7), y + Inches(0.13),
        Inches(0.44), Inches(0.44))
    badge.fill.solid(); badge.fill.fore_color.rgb = PY_YELLOW
    badge.line.fill.background()
    add_text(slide, x + w - Inches(0.7), y + Inches(0.13),
             Inches(0.44), Inches(0.44), "5",
             font_size=16, bold=True, color=PY_BLUE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # 知识目标条目
    items1 = [
        "**Python 语言发展史** — 起源、设计哲学与版本演进",
        "**Python 与 Java、C++ 差异** — 类型系统、执行方式、语法、性能",
        "**Python 主要应用场景** — AI、数据科学、Web、自动化等",
        "**开发环境搭建** — Python 解释器 + VS Code + Trae",
        "**uv 虚拟环境管理** — 现代化 Python 项目依赖管理",
    ]
    add_bullets(slide, x + Inches(0.35), y + Inches(0.95),
                w - Inches(0.7), h - Inches(1.1),
                items1, font_size=15, line_spacing=1.45)

    # 右卡片：AI 辅助学习目标
    x2 = Inches(6.85); w2 = Inches(5.9)
    card2 = add_round_rect(slide, x2, y, w2, h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.05)
    add_rect(slide, x2, y, w2, Inches(0.7), PY_YELLOW)
    add_text(slide, x2 + Inches(0.3), y, Inches(3.5), Inches(0.7),
             "🤖 AI 辅助学习目标", font_size=18, bold=True, color=PY_BLUE,
             anchor=MSO_ANCHOR.MIDDLE)
    badge2 = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        x2 + w2 - Inches(0.7), y + Inches(0.13),
        Inches(0.44), Inches(0.44))
    badge2.fill.solid(); badge2.fill.fore_color.rgb = PY_BLUE
    badge2.line.fill.background()
    add_text(slide, x2 + w2 - Inches(0.7), y + Inches(0.13),
             Inches(0.44), Inches(0.44), "AI",
             font_size=11, bold=True, color=PY_WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    items2 = [
        "学会用 AI **查询 Python 版本特性、生态与历史背景**",
        "学会用 AI **排查环境配置与安装过程中的问题**",
        "掌握向 AI **描述环境报错、获取解决方案** 的方法",
        "建立 \"AI 协作学习\" 的工作流意识",
        "形成 \"Prompt → 多轮追问 → 自我复述\" 的学习闭环",
    ]
    add_bullets(slide, x2 + Inches(0.35), y + Inches(0.95),
                w2 - Inches(0.7), h - Inches(1.1),
                items2, font_size=15, line_spacing=1.45,
                bullet_color=PY_ACCENT_ORANGE)


# ============== Slide 3：课程导览 ==============
def slide_agenda():
    slide = new_slide("课程导览")
    add_section_title(slide, "本节课程导览", "Agenda · 5 个核心知识点 + 实验")

    # 时间线式导览
    items = [
        ("01", "Python 发展史", "起源、版本演进、设计哲学", PY_BLUE),
        ("02", "Python vs Java/C++", "多维度对比，建立心智模型", PY_BLUE_LIGHT),
        ("03", "Python 应用场景", "AI / 数据科学 / Web / 自动化等 9 大方向", PY_YELLOW),
        ("04", "环境搭建", "Python + VS Code + Trae", PY_ACCENT_GREEN),
        ("05", "uv 虚拟环境", "现代化 Python 项目管理工具", PY_ACCENT_ORANGE),
    ]
    # 中央垂直轴线
    line_x = Inches(1.5)
    add_rect(slide, line_x, Inches(2.0), Inches(0.04),
             Inches(4.2), RGBColor(0xD8,0xDF,0xE6))

    base_y = Inches(2.0)
    for i, (no, title, desc, color) in enumerate(items):
        y = base_y + Inches(0.85) * i
        # 圆点
        c = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            line_x - Inches(0.2), y + Inches(0.05),
            Inches(0.44), Inches(0.44))
        c.fill.solid(); c.fill.fore_color.rgb = color
        c.line.color.rgb = PY_WHITE
        c.line.width = Pt(2)
        # 编号
        add_text(slide, line_x - Inches(0.2), y + Inches(0.05),
                 Inches(0.44), Inches(0.44),
                 no, font_size=11, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, Inches(2.1), y, Inches(4.5), Inches(0.45),
                 title, font_size=20, bold=True, color=PY_BLUE,
                 anchor=MSO_ANCHOR.MIDDLE)
        # 描述
        add_text(slide, Inches(2.1), y + Inches(0.42),
                 Inches(10), Inches(0.35),
                 desc, font_size=13, color=PY_GRAY,
                 anchor=MSO_ANCHOR.TOP)

    # 右侧装饰块
    box_x = Inches(10.0); box_y = Inches(2.0)
    box = add_round_rect(slide, box_x, box_y,
                         Inches(2.85), Inches(4.2),
                         PY_BLUE, corner=0.05)
    add_text(slide, box_x + Inches(0.25), box_y + Inches(0.3),
             Inches(2.4), Inches(0.4),
             "🎯 学习节奏", font_size=14, bold=True, color=PY_YELLOW)
    add_text(slide, box_x + Inches(0.25), box_y + Inches(0.85),
             Inches(2.4), Inches(3.0),
             "概念讲解\n"
             "    ↓\n"
             "代码示例\n"
             "    ↓\n"
             "AI 辅助提问\n"
             "    ↓\n"
             "动手实验\n"
             "    ↓\n"
             "课堂练习",
             font_size=13, color=PY_WHITE, line_spacing=1.4)


# ============== Slide 4：章节分隔 - Python 发展史 ==============
def slide_section_divider(no, title, subtitle, color):
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, PY_WHITE)
    # 左侧大色块
    add_rect(slide, 0, 0, Inches(5.5), SLIDE_H, color)
    # 编号大字
    add_text(slide, Inches(0.6), Inches(2.4), Inches(5), Inches(2.0),
             no, font_size=160, bold=True, color=PY_WHITE)
    # PART label
    add_text(slide, Inches(0.6), Inches(1.6), Inches(5), Inches(0.6),
             "PART", font_size=18, bold=True, color=PY_YELLOW)
    # 右侧标题
    add_rect(slide, Inches(6.0), Inches(3.4), Inches(0.12), Inches(0.7), PY_YELLOW)
    add_text(slide, Inches(6.3), Inches(3.3), Inches(6.5), Inches(0.9),
             title, font_size=36, bold=True, color=PY_DARK)
    add_text(slide, Inches(6.3), Inches(4.15), Inches(6.5), Inches(0.6),
             subtitle, font_size=16, color=PY_GRAY)
    # 右上角页码
    page_counter[0] += 1
    add_text(slide, SLIDE_W - Inches(1.4), Inches(0.18), Inches(1.2), Inches(0.3),
             f"{page_counter[0]:02d} / {TOTAL:02d}", font_size=10,
             color=PY_GRAY, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    # 课程名
    add_text(slide, Inches(6.3), Inches(0.15), Inches(6), Inches(0.3),
             "Python 语言程序设计  ·  第 1 周", font_size=10,
             color=PY_GRAY, anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 5：Python 起源 ==============
def slide_python_origin():
    slide = new_slide("知识点 1  ·  Python 发展史")
    add_section_title(slide, "Python 的诞生",
                       "诞生于圣诞节的一个项目，至今 35 年历史")

    # 左侧：故事卡
    x = Inches(0.6); y = Inches(1.85); w = Inches(7.2); h = Inches(4.7)
    card = add_round_rect(slide, x, y, w, h, PY_WHITE,
                          line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    # 顶部装饰条
    add_rect(slide, x, y, w, Inches(0.08), PY_YELLOW)
    # 大年份
    add_text(slide, x + Inches(0.4), y + Inches(0.3),
             w - Inches(0.8), Inches(0.9),
             "1989 · Christmas", font_size=42, bold=True, color=PY_BLUE)
    add_text(slide, x + Inches(0.4), y + Inches(1.25),
             w - Inches(0.8), Inches(0.5),
             "Guido van Rossum 开始动手写一个脚本语言",
             font_size=18, color=PY_DARK)
    # 主体内容
    story_items = [
        ("🎯 起因", "荷兰人 **Guido van Rossum**（吉多·范罗苏姆）在 CWI 研究所为度过圣诞假期，决定开发一个新的脚本语言，作为 ABC 语言的继承者"),
        ("📅 发布", "**1991 年 2 月** 发布第一个公开发行版 **0.9.0**"),
        ("🐍 命名", "并非 \"蟒蛇\"，而是 Guido 喜爱的英国喜剧团体 **Monty Python**（巨蟒剧团）"),
        ("🥚 彩蛋", "社区沿袭剧团 \"Spam/鸡蛋/奶酪\" 传统，命名常埋 \"食物彩蛋\"（如旧版安装包格式 `.egg`）"),
    ]
    add_bullets(slide, x + Inches(0.4), y + Inches(1.85),
                w - Inches(0.8), h - Inches(2.0),
                story_items, font_size=13, line_spacing=1.45,
                bullet_color=PY_YELLOW)

    # 右侧：人物卡
    x2 = Inches(8.05); w2 = Inches(4.7)
    card2 = add_round_rect(slide, x2, y, w2, h, PY_BLUE, corner=0.04)
    # 头像圆形
    av = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        x2 + w2/2 - Inches(0.9), y + Inches(0.4),
        Inches(1.8), Inches(1.8))
    av.fill.solid(); av.fill.fore_color.rgb = PY_YELLOW
    av.line.color.rgb = PY_WHITE
    av.line.width = Pt(3)
    add_text(slide, x2 + w2/2 - Inches(0.9), y + Inches(0.4),
             Inches(1.8), Inches(1.8),
             "GvR", font_size=42, bold=True, color=PY_BLUE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, x2 + Inches(0.3), y + Inches(2.45),
             w2 - Inches(0.6), Inches(0.5),
             "Guido van Rossum", font_size=20, bold=True, color=PY_WHITE,
             align=PP_ALIGN.CENTER)
    add_text(slide, x2 + Inches(0.3), y + Inches(2.9),
             w2 - Inches(0.6), Inches(0.4),
             "Python 之父 · 终身仁慈独裁者（BDFL）",
             font_size=12, color=PY_YELLOW, align=PP_ALIGN.CENTER)
    # 引言
    quote_box = add_round_rect(slide, x2 + Inches(0.3), y + Inches(3.45),
                               w2 - Inches(0.6), Inches(1.05),
                               PY_WHITE, corner=0.15)
    add_text(slide, x2 + Inches(0.45), y + Inches(3.55),
             w2 - Inches(0.9), Inches(0.95),
             "「我只是想写一门比 C 更愉快的语言。」\n—— Guido van Rossum",
             font_size=12, color=PY_DARK, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 6：Python 版本演进 ==============
def slide_python_versions():
    slide = new_slide("知识点 1  ·  Python 发展史")
    add_section_title(slide, "Python 版本演进",
                       "从 1991 到 2024，三十余年持续演进")

    # 时间线表格
    rows = [
        ("0.9.0",  "1991",  "第一个公开发布版本"),
        ("2.0",    "2000",  "引入垃圾回收、Unicode 支持"),
        ("3.0",    "2008",  "不兼容升级，统一字符编码、改进整数除法等"),
        ("3.6",    "2016",  "f-string 字符串格式化、类型注解完善"),
        ("3.10",   "2021",  "结构化模式匹配（match-case）"),
        ("3.11",   "2022",  "性能大幅提升，比 3.10 快 10%–60%"),
        ("3.12",   "2023",  "更好的错误信息提示，进一步性能优化"),
        ("3.13",   "2024",  "实验性自由线程（移除 GIL）、JIT 编译器"),
    ]

    # 表头
    col_x = [Inches(0.6), Inches(1.85), Inches(2.95), Inches(4.45)]
    col_w = [Inches(1.25), Inches(1.10), Inches(1.50), Inches(8.30)]
    header_y = Inches(1.85)
    header_h = Inches(0.5)
    add_rect(slide, Inches(0.6), header_y, Inches(12.15), header_h, PY_BLUE)
    headers = ["版本", "发布年份", "重要变化"]
    for i, h in enumerate(headers):
        align = PP_ALIGN.LEFT if i == 2 else PP_ALIGN.CENTER
        add_text(slide, col_x[i], header_y, col_w[i], header_h,
                 h, font_size=14, bold=True, color=PY_WHITE,
                 align=align, anchor=MSO_ANCHOR.MIDDLE)

    # 行
    row_h = Inches(0.48)
    for i, (ver, year, desc) in enumerate(rows):
        ry = header_y + header_h + row_h * i
        bg = PY_WHITE if i % 2 == 0 else PY_BG_LIGHT
        add_rect(slide, Inches(0.6), ry, Inches(12.15), row_h, bg,
                 line_color=RGBColor(0xE5,0xE9,0xEF))
        # 版本（高亮）
        ver_color = PY_BLUE if ver == "3.0" else PY_DARK
        ver_bold = True if ver in ["3.0", "3.13"] else False
        add_text(slide, col_x[0], ry, col_w[0], row_h,
                 ver, font_size=13, bold=ver_bold, color=ver_color,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, col_x[1], ry, col_w[1], row_h,
                 year, font_size=13, color=PY_DARK,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, col_x[2], ry, col_w[2], row_h,
                 desc, font_size=13, color=PY_DARK,
                 align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

    # 底部提示条
    note_y = Inches(6.45)
    note = add_round_rect(slide, Inches(0.6), note_y,
                          Inches(12.15), Inches(0.5),
                          PY_BG_LIGHT, line_color=PY_YELLOW, corner=0.3)
    add_text(slide, Inches(0.85), note_y, Inches(11.7), Inches(0.5),
             "💡  本课程统一使用 Python 3.11 / 3.12  ·  2020-01-01 Python 2.7 已 EOL",
             font_size=13, bold=True, color=PY_BLUE,
             anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 7：Python 2 vs 3 ==============
def slide_py2_py3():
    slide = new_slide("知识点 1  ·  Python 发展史")
    add_section_title(slide, "Python 2 vs Python 3",
                       "一次长达十余年的不兼容升级")

    # 左侧：为何分裂
    x1 = Inches(0.6); y = Inches(1.85); w = Inches(6.0); h = Inches(4.7)
    card1 = add_round_rect(slide, x1, y, w, h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x1, y, w, Inches(0.7), PY_BLUE)
    add_text(slide, x1 + Inches(0.3), y, w - Inches(0.6), Inches(0.7),
             "❓  为什么必须分裂？",
             font_size=17, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    items = [
        "Python 2 发展十余年，**积累大量\"历史包袱\"**",
        "字符串与 Unicode 处理混乱、`print` 是语句而非函数",
        "整数除法语义怪异、标准库命名不统一",
        "这些\"小修小补\"已无法清理，Guido 决定以一次**不向后兼容**的大升级根除",
        "代号：**Python 3000 / Py3K**，2008 年发布",
    ]
    add_bullets(slide, x1 + Inches(0.35), y + Inches(0.95),
                w - Inches(0.7), h - Inches(1.1),
                items, font_size=14, line_spacing=1.5)

    # 右侧：核心不兼容点
    x2 = Inches(6.85); w2 = Inches(5.9)
    card2 = add_round_rect(slide, x2, y, w2, h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x2, y, w2, Inches(0.7), PY_ACCENT_RED)
    add_text(slide, x2 + Inches(0.3), y, w2 - Inches(0.6), Inches(0.7),
             "⚠️  核心不兼容点（迁移痛苦之源）",
             font_size=17, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    # 子项列表
    diff_items = [
        ("**字符串**", "2.x 的 `str` 本质是字节；3.x 统一为 `str`（Unicode）与 `bytes`"),
        ("**print**", "语句 `print x` → 函数 `print(x)`"),
        ("**整数除法**", "2.x `1/2` = `0`；3.x `1/2` = `0.5`"),
        ("**字典方法**", "`keys()/values()/items()` 返回视图而非列表"),
        ("**EOL 终点**", "**2020-01-01** Python 2.7 官方停止更新，时代结束"),
    ]
    add_bullets(slide, x2 + Inches(0.35), y + Inches(0.95),
                w2 - Inches(0.7), h - Inches(1.1),
                diff_items, font_size=13, line_spacing=1.5,
                bullet_color=PY_ACCENT_RED)


# ============== Slide 8：The Zen of Python ==============
def slide_zen():
    slide = new_slide("知识点 1  ·  Python 发展史")
    add_section_title(slide, "Python 之禅（The Zen of Python）",
                       "Tim Peters 撰写的 19 条设计哲学")

    # 左侧金句
    items = [
        ("**优美胜于丑陋**", "Beautiful is better than ugly."),
        ("**简洁胜于复杂**", "Simple is better than complex."),
        ("**可读性至上**", "Readability counts."),
        ("**显式胜于隐式**", "Explicit is better than implicit."),
        ("**…应该只有一种——且最好是唯一一种——显而易见的方法**", ""),
    ]
    x = Inches(0.6); y = Inches(1.85); w = Inches(7.5); h = Inches(4.7)
    card = add_round_rect(slide, x, y, w, h, PY_WHITE,
                          line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x, y, Inches(0.12), h, PY_YELLOW)
    add_text(slide, x + Inches(0.35), y + Inches(0.2),
             w - Inches(0.7), Inches(0.5),
             "Python 之禅 · 核心 5 条",
             font_size=18, bold=True, color=PY_BLUE)
    add_bullets(slide, x + Inches(0.35), y + Inches(0.85),
                w - Inches(0.7), h - Inches(1.0),
                items, font_size=14, line_spacing=1.6,
                bullet_color=PY_YELLOW)

    # 右侧：体验代码
    x2 = Inches(8.3); w2 = Inches(4.45); h2 = Inches(4.7)
    add_round_rect(slide, x2, y, w2, h2, PY_BG_LIGHT, corner=0.04)
    add_text(slide, x2 + Inches(0.3), y + Inches(0.2),
             w2 - Inches(0.6), Inches(0.5),
             "✨ 在解释器中体验",
             font_size=14, bold=True, color=PY_BLUE)
    add_code_block(slide, x2 + Inches(0.3), y + Inches(0.85),
                   w2 - Inches(0.6), Inches(2.5),
                   "# 在 Python 解释器交互环境里输入：\n>>> import this\n\n# 即可看到完整的 19 条 Python 之禅\n# 包括英文原文与中文译本",
                   font_size=13, lang="python")
    # 底部小贴士
    tip = add_round_rect(slide, x2 + Inches(0.3), y + Inches(3.7),
                         w2 - Inches(0.6), Inches(0.85),
                         PY_YELLOW, corner=0.2)
    add_text(slide, x2 + Inches(0.3), y + Inches(3.7),
             w2 - Inches(0.6), Inches(0.85),
             "💡  `import this` 是 Python 社区的「入职彩蛋」",
             font_size=12, bold=True, color=PY_BLUE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 9：今天的地位 ==============
def slide_python_today():
    slide = new_slide("知识点 1  ·  Python 发展史")
    add_section_title(slide, "Python 在今天的地位",
                       "TIOBE 长期前三  ·  AI 时代的事实标准语言")

    # 三个数据卡
    cards = [
        ("🥇",  "TIOBE", "长期位居编程语言排行榜前三，多次年度语言", PY_BLUE),
        ("🧠",  "AI 时代", "AI / 数据科学 / 自动化的事实标准语言", PY_BLUE_LIGHT),
        ("📦",  "PyPI", "数十万计第三方包，`pip install` 默认源", PY_YELLOW),
    ]
    card_w = Inches(4.0); card_h = Inches(2.4)
    gap = Inches(0.2)
    total_w = card_w * 3 + gap * 2
    start_x = (SLIDE_W - total_w) / 2
    y = Inches(2.0)
    for i, (icon, title, desc, color) in enumerate(cards):
        cx = start_x + (card_w + gap) * i
        c = add_round_rect(slide, cx, y, card_w, card_h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.05)
        # 顶部色条
        add_rect(slide, cx, y, card_w, Inches(0.12), color)
        # 图标
        add_text(slide, cx, y + Inches(0.35), card_w, Inches(0.9),
                 icon, font_size=44,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, cx, y + Inches(1.3), card_w, Inches(0.5),
                 title, font_size=20, bold=True, color=color,
                 align=PP_ALIGN.CENTER)
        # 描述
        add_text(slide, cx + Inches(0.3), y + Inches(1.85),
                 card_w - Inches(0.6), Inches(0.5),
                 desc, font_size=12, color=PY_GRAY,
                 align=PP_ALIGN.CENTER)

    # 底部大数据
    y2 = Inches(4.7)
    big_box = add_round_rect(slide, Inches(0.6), y2,
                             Inches(12.15), Inches(2.0),
                             PY_BLUE, corner=0.04)
    add_text(slide, Inches(0.6), y2 + Inches(0.15),
             Inches(12.15), Inches(0.5),
             "Python 为什么能成为 AI 时代首选？",
             font_size=18, bold=True, color=PY_YELLOW,
             align=PP_ALIGN.CENTER)
    reasons = [
        ("🎯",  "语法简洁", "可执行的伪代码，AI 自动生成友好"),
        ("📚",  "生态丰富", "PyTorch / TF / scikit-learn 等"),
        ("🔬",  "交互友好", "Jupyter Notebook 即写即跑"),
        ("🌐",  "跨平台",  "Win / macOS / Linux 全支持"),
    ]
    item_w = Inches(2.85)
    item_gap = Inches(0.1)
    total_item_w = item_w * 4 + item_gap * 3
    item_start = (SLIDE_W - total_item_w) / 2
    iy = y2 + Inches(0.85)
    for i, (icon, t, d) in enumerate(reasons):
        ix = item_start + (item_w + item_gap) * i
        add_text(slide, ix, iy, item_w, Inches(0.5),
                 icon, font_size=24, align=PP_ALIGN.CENTER)
        add_text(slide, ix, iy + Inches(0.55), item_w, Inches(0.4),
                 t, font_size=14, bold=True, color=PY_YELLOW,
                 align=PP_ALIGN.CENTER)
        add_text(slide, ix, iy + Inches(0.95), item_w, Inches(0.4),
                 d, font_size=10, color=PY_WHITE, align=PP_ALIGN.CENTER)


# ============== Slide 10：AI 辅助提示 ==============
def slide_ai_prompts_1():
    slide = new_slide("知识点 1  ·  AI 辅助")
    add_section_title(slide, "🤖 AI 辅助：向 AI 提问的 Prompt 示例",
                       "用 AI 加深对 Python 历史背景的理解")
    box = add_round_rect(slide, Inches(0.6), Inches(1.85),
                         Inches(12.15), Inches(4.7),
                         PY_WHITE, line_color=RGBColor(0xDD,0xE3,0xEA),
                         corner=0.04)
    add_rect(slide, Inches(0.6), Inches(1.85), Inches(12.15), Inches(0.7), PY_ACCENT_ORANGE)
    add_text(slide, Inches(0.85), Inches(1.85), Inches(11.9), Inches(0.7),
             "💬  推荐 Prompt（可直接复制到 AI 对话框）",
             font_size=16, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)

    prompts = [
        ("Prompt 1",
         "请梳理 Python 语言从 1989 年至今的关键版本和里程碑事件。"),
        ("Prompt 2",
         "Python 2 和 Python 3 主要有哪些不兼容的地方？为什么这次升级花了十几年？"),
        ("Prompt 3",
         "Python 3.13 移除 GIL 意味着什么？对普通开发者有什么影响？"),
        ("Prompt 4",
         "为什么 Python 在 AI 时代能成为首选语言？请从生态、语法、社区三个维度分析。"),
    ]
    by = Inches(2.75)
    bh = Inches(0.85)
    for i, (label, p) in enumerate(prompts):
        ry = by + (bh + Inches(0.05)) * i
        # 标签
        tag = add_round_rect(slide, Inches(0.85), ry + Inches(0.1),
                             Inches(1.2), Inches(0.6),
                             PY_ACCENT_ORANGE, corner=0.3)
        add_text(slide, Inches(0.85), ry + Inches(0.1),
                 Inches(1.2), Inches(0.6),
                 label, font_size=11, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # Prompt 内容
        add_text(slide, Inches(2.25), ry, Inches(10.3), bh,
                 p, font_size=14, color=PY_DARK,
                 anchor=MSO_ANCHOR.MIDDLE)
        # 底部分割线
        if i < len(prompts) - 1:
            add_rect(slide, Inches(0.85), ry + bh,
                     Inches(11.6), Inches(0.01),
                     RGBColor(0xE5,0xE9,0xEF))


# ============== Slide 11：Python vs Java/C++ 对比表 ==============
def slide_compare_table():
    slide = new_slide("知识点 2  ·  Python vs Java/C++")
    add_section_title(slide, "三语言核心维度对比",
                       "帮助学过 Java/C++ 的同学快速建立 Python 心智模型")

    # 表格
    headers = ["维度", "C++", "Java", "Python"]
    rows = [
        ("类型系统",       "静态、强类型",         "静态、强类型",     "动态、强类型"),
        ("执行方式",       "编译为机器码",         "编译为字节码 + JVM", "解释执行（先编译 .pyc）"),
        ("内存管理",       "手动（new/delete）",   "JVM 垃圾回收",     "引用计数 + GC"),
        ("语法冗余",       "较高",                "较高",             "很低（\"可执行的伪代码\"）"),
        ("运行性能",       "最快",                "较快",             "较慢（约为 C++ 的 1/10 ~ 1/3）"),
        ("典型用途",       "系统、游戏、嵌入式",   "企业后端、Android", "AI / 数据科学 / 脚本 / Web"),
    ]

    col_x = [Inches(0.6), Inches(2.55), Inches(5.40), Inches(8.40)]
    col_w = [Inches(1.95), Inches(2.85), Inches(3.00), Inches(4.35)]
    header_y = Inches(1.85)
    header_h = Inches(0.55)

    # 表头
    add_rect(slide, Inches(0.6), header_y, Inches(12.15), header_h, PY_BLUE)
    for i, h in enumerate(headers):
        color = PY_YELLOW if h in ["Python"] else PY_WHITE
        bold = h in ["Python"]
        add_text(slide, col_x[i], header_y, col_w[i], header_h,
                 h, font_size=15, bold=True, color=color,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # 行
    row_h = Inches(0.62)
    for i, row in enumerate(rows):
        ry = header_y + header_h + row_h * i
        bg = PY_WHITE if i % 2 == 0 else PY_BG_LIGHT
        add_rect(slide, Inches(0.6), ry, Inches(12.15), row_h, bg,
                 line_color=RGBColor(0xE5,0xE9,0xEF))
        for j, cell in enumerate(row):
            is_python_col = (j == 3)
            add_text(slide, col_x[j], ry, col_w[j], row_h,
                     cell,
                     font_size=13,
                     bold=(j == 0 or is_python_col),
                     color=PY_BLUE if is_python_col else PY_DARK,
                     align=PP_ALIGN.CENTER if j != 0 else PP_ALIGN.LEFT,
                     anchor=MSO_ANCHOR.MIDDLE)

    # 底部 takeaway
    ty = Inches(6.4)
    take = add_round_rect(slide, Inches(0.6), ty,
                          Inches(12.15), Inches(0.55),
                          PY_BG_LIGHT, line_color=PY_YELLOW, corner=0.3)
    add_text(slide, Inches(0.85), ty, Inches(11.7), Inches(0.55),
             "🎯  一句话总结：Python = \"**简洁语法 + 动态类型 + 慢但开发快**\"——用性能换生产力",
             font_size=14, bold=True, color=PY_BLUE,
             anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 12：Hello World 三语言对比 ==============
def slide_hello_compare():
    slide = new_slide("知识点 2  ·  Python vs Java/C++")
    add_section_title(slide, "Hello World 三语言对照",
                       "感受 Python \"可执行伪代码\" 的简洁")

    # 三个并排的代码卡
    codes = [
        ("C++", "cpp", PY_BLUE,
         "// C++\n"
         "#include <iostream>\n"
         "int main() {\n"
         "    std::cout << \"Hello, World!\"\n"
         "              << std::endl;\n"
         "    return 0;\n"
         "}"),
        ("Java", "java", PY_ACCENT_ORANGE,
         "// Java\n"
         "public class Hello {\n"
         "    public static void main(\n"
         "            String[] args) {\n"
         "        System.out.println(\n"
         "            \"Hello, World!\");\n"
         "    }\n"
         "}"),
        ("Python", "python", PY_ACCENT_GREEN,
         "# Python\n"
         "print(\"Hello, World!\")"),
    ]
    cw = Inches(4.0); gap = Inches(0.18); ch = Inches(4.5)
    total_w = cw * 3 + gap * 2
    start_x = (SLIDE_W - total_w) / 2
    y = Inches(1.85)
    for i, (lang, ext, color, code) in enumerate(codes):
        cx = start_x + (cw + gap) * i
        card = add_round_rect(slide, cx, y, cw, ch, PY_WHITE,
                              line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.03)
        # 顶部语言标签
        add_rect(slide, cx, y, cw, Inches(0.45), color)
        add_text(slide, cx, y, cw, Inches(0.45),
                 lang, font_size=16, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 代码块
        add_code_block(slide, cx + Inches(0.15), y + Inches(0.6),
                       cw - Inches(0.3), ch - Inches(0.75),
                       code, font_size=11, lang=f"hello.{ext}")

    # 底部对比说明
    by = Inches(6.5)
    lines = [
        ("📝", "C++ 需要头文件 + main 函数 + 命名空间，共 7 行"),
        ("📝", "Java 需要类 + main 方法 + 大括号对齐，共 7 行"),
        ("✨", "Python 仅 1 行：print(\"Hello, World!\")"),
    ]
    for i, (icon, t) in enumerate(lines):
        lx = Inches(0.6) + Inches(4.18) * i
        color = PY_ACCENT_GREEN if i == 2 else PY_GRAY
        add_text(slide, lx, by, Inches(4.0), Inches(0.4),
                 f"{icon}  {t}",
                 font_size=12, color=color,
                 anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 13：变量与类型 + 循环 对比 ==============
def slide_type_loop():
    slide = new_slide("知识点 2  ·  Python vs Java/C++")
    add_section_title(slide, "变量声明与循环对比",
                       "更直观的类型差异  ·  更简洁的语法")

    # 左侧：变量与类型
    x = Inches(0.6); y = Inches(1.85); w = Inches(6.0); h = Inches(4.7)
    card = add_round_rect(slide, x, y, w, h, PY_WHITE,
                          line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.03)
    add_rect(slide, x, y, w, Inches(0.5), PY_BLUE)
    add_text(slide, x + Inches(0.3), y, w - Inches(0.6), Inches(0.5),
             "📌  变量与类型声明",
             font_size=15, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    # 子标题
    add_text(slide, x + Inches(0.3), y + Inches(0.6),
             w - Inches(0.6), Inches(0.3),
             "C++ / Java：必须显式声明类型",
             font_size=12, bold=True, color=PY_GRAY)
    add_code_block(slide, x + Inches(0.3), y + Inches(0.95),
                   w - Inches(0.6), Inches(1.05),
                   "// C++\n"
                   "int age = 20;\n"
                   "std::string name = \"张三\";\n\n"
                   "// Java\n"
                   "int age = 20;\n"
                   "String name = \"张三\";",
                   font_size=11, lang="typed")
    add_text(slide, x + Inches(0.3), y + Inches(2.1),
             w - Inches(0.6), Inches(0.3),
             "Python：自动推断，同一变量可重新指向不同类型",
             font_size=12, bold=True, color=PY_ACCENT_GREEN)
    add_code_block(slide, x + Inches(0.3), y + Inches(2.45),
                   w - Inches(0.6), Inches(1.5),
                   "# Python\n"
                   "age = 20          # int\n"
                   "age = \"张三\"      # 现在变成 str\n"
                   "# （允许，但不建议这样写）",
                   font_size=12, lang="python")
    # 小贴士
    add_text(slide, x + Inches(0.3), y + Inches(4.0),
             w - Inches(0.6), Inches(0.5),
             "💡  Python 3.6+ 支持**类型注解**，可读性 + 静态检查",
             font_size=11, color=PY_BLUE)

    # 右侧：循环
    x2 = Inches(6.85); w2 = Inches(5.9); h2 = Inches(4.7)
    card2 = add_round_rect(slide, x2, y, w2, h2, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.03)
    add_rect(slide, x2, y, w2, Inches(0.5), PY_ACCENT_GREEN)
    add_text(slide, x2 + Inches(0.3), y, w2 - Inches(0.6), Inches(0.5),
             "🔁  循环：求 1 到 10 的平方",
             font_size=15, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, x2 + Inches(0.3), y + Inches(0.6),
             w2 - Inches(0.6), Inches(0.3),
             "C++ / Java：3 行起步",
             font_size=12, bold=True, color=PY_GRAY)
    add_code_block(slide, x2 + Inches(0.3), y + Inches(0.95),
                   w2 - Inches(0.6), Inches(1.4),
                   "// C++\n"
                   "for (int i = 1; i <= 10; i++) {\n"
                   "    std::cout << i * i << \" \";\n"
                   "}\n\n"
                   "// Java\n"
                   "for (int i = 1; i <= 10; i++) {\n"
                   "    System.out.print(i * i + \" \");\n"
                   "}",
                   font_size=11, lang="typed")
    add_text(slide, x2 + Inches(0.3), y + Inches(2.45),
             w2 - Inches(0.6), Inches(0.3),
             "Python：仅 2 行，无须手动管理 i",
             font_size=12, bold=True, color=PY_ACCENT_GREEN)
    add_code_block(slide, x2 + Inches(0.3), y + Inches(2.8),
                   w2 - Inches(0.6), Inches(1.0),
                   "# Python\n"
                   "for i in range(1, 11):\n"
                   "    print(i * i, end=\" \")",
                   font_size=13, lang="python")
    add_text(slide, x2 + Inches(0.3), y + Inches(3.85),
             w2 - Inches(0.6), Inches(0.5),
             "💡  `range(1, 11)` 左闭右开：包含 1，不包含 11",
             font_size=11, color=PY_BLUE)


# ============== Slide 14：AI 辅助提示 2 ==============
def slide_ai_prompts_2():
    slide = new_slide("知识点 2  ·  AI 辅助")
    add_section_title(slide, "🤖 AI 辅助：跨语言对比的 Prompt",
                       "用 AI 加深对 Python 与 Java/C++ 差异的理解")
    box = add_round_rect(slide, Inches(0.6), Inches(1.85),
                         Inches(12.15), Inches(4.7),
                         PY_WHITE, line_color=RGBColor(0xDD,0xE3,0xEA),
                         corner=0.04)
    add_rect(slide, Inches(0.6), Inches(1.85), Inches(12.15), Inches(0.7), PY_ACCENT_ORANGE)
    add_text(slide, Inches(0.85), Inches(1.85), Inches(11.9), Inches(0.7),
             "💬  推荐 Prompt",
             font_size=16, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    prompts = [
        ("Prompt 1",
         "同一段功能分别用 Python、Java、C++ 实现，并对比它们的语法差异。"),
        ("Prompt 2",
         "Python 是解释执行的，为什么还能有 .pyc 文件？"),
        ("Prompt 3",
         "我已经会 Java，请列出我学 Python 时最易出错的 5 个点。"),
        ("Prompt 4",
         "为什么 Python 被称为\"可执行的伪代码\"？它和伪代码的本质区别是什么？"),
    ]
    by = Inches(2.75)
    bh = Inches(0.85)
    for i, (label, p) in enumerate(prompts):
        ry = by + (bh + Inches(0.05)) * i
        tag = add_round_rect(slide, Inches(0.85), ry + Inches(0.1),
                             Inches(1.2), Inches(0.6),
                             PY_ACCENT_ORANGE, corner=0.3)
        add_text(slide, Inches(0.85), ry + Inches(0.1),
                 Inches(1.2), Inches(0.6),
                 label, font_size=11, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, Inches(2.25), ry, Inches(10.3), bh,
                 p, font_size=14, color=PY_DARK,
                 anchor=MSO_ANCHOR.MIDDLE)
        if i < len(prompts) - 1:
            add_rect(slide, Inches(0.85), ry + bh,
                     Inches(11.6), Inches(0.01),
                     RGBColor(0xE5,0xE9,0xEF))


# ============== Slide 15：Python 应用场景总览 ==============
def slide_applications():
    slide = new_slide("知识点 3  ·  Python 应用场景")
    add_section_title(slide, "Python 主要应用场景",
                       "Python 之所以流行——9 大领域的成熟生态")

    apps = [
        ("🧠", "AI / ML / DL",   "PyTorch · TensorFlow\nHugging Face", PY_ACCENT_RED),
        ("📊", "数据科学",       "NumPy · Pandas\nMatplotlib · Jupyter", PY_BLUE),
        ("🌍", "Web 开发",       "Django · Flask · FastAPI", PY_ACCENT_GREEN),
        ("🤖", "自动化脚本",     "文件 / Excel / Word\n批处理 \"胶水\" 脚本", PY_ACCENT_ORANGE),
        ("🕷️", "网络爬虫",       "requests · BeautifulSoup\nScrapy · aiohttp", PY_BLUE_LIGHT),
        ("🔬", "科学计算",       "SciPy · SymPy\nAstropy · BioPython", PY_BLUE),
        ("⚙️", "DevOps 运维",    "Ansible · Fabric\n自动化部署", PY_GRAY),
        ("📡", "嵌入式 / IoT",   "MicroPython\nCircuitPython + 树莓派 Pico", PY_YELLOW),
        ("🎮", "GUI / 游戏",     "PyQt · Tkinter\nPygame（2D 游戏）", RGBColor(0x9B,0x59,0xB6)),
    ]

    # 3x3 网格
    cols = 3
    cw = Inches(4.0); ch = Inches(1.45)
    gap_x = Inches(0.15); gap_y = Inches(0.12)
    grid_w = cw * cols + gap_x * (cols - 1)
    start_x = (SLIDE_W - grid_w) / 2
    start_y = Inches(1.85)
    for i, (icon, title, desc, color) in enumerate(apps):
        r = i // cols
        c = i % cols
        x = start_x + c * (cw + gap_x)
        y = start_y + r * (ch + gap_y)
        card = add_round_rect(slide, x, y, cw, ch, PY_WHITE,
                              line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.08)
        # 左侧色块
        add_rect(slide, x, y, Inches(0.12), ch, color)
        # 图标
        add_text(slide, x + Inches(0.25), y, Inches(0.9), ch,
                 icon, font_size=32,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, x + Inches(1.2), y + Inches(0.18),
                 cw - Inches(1.4), Inches(0.4),
                 title, font_size=15, bold=True, color=PY_DARK,
                 anchor=MSO_ANCHOR.MIDDLE)
        # 描述
        add_text(slide, x + Inches(1.2), y + Inches(0.6),
                 cw - Inches(1.4), Inches(0.8),
                 desc, font_size=11, color=PY_GRAY, line_spacing=1.2)


# ============== Slide 16：自动化脚本代码示例 ==============
def slide_automation_code():
    slide = new_slide("知识点 3  ·  代码示例")
    add_section_title(slide, "代码示例：自动文件分类归档",
                       "10+ 行 Python 代码替代 10 分钟手工整理")

    # 左侧：场景说明
    x = Inches(0.6); y = Inches(1.85); w = Inches(4.3); h = Inches(4.7)
    card = add_round_rect(slide, x, y, w, h, PY_WHITE,
                          line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x, y, w, Inches(0.5), PY_ACCENT_ORANGE)
    add_text(slide, x + Inches(0.3), y, w - Inches(0.6), Inches(0.5),
             "🎯  场景",
             font_size=15, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, x + Inches(0.3), y + Inches(0.7),
             w - Inches(0.6), Inches(0.7),
             "下载文件夹里文件乱七八糟，\n按后缀自动分类归档",
             font_size=14, bold=True, color=PY_DARK)
    items = [
        "✅ 同样功能用 Windows 批处理又长又难读",
        "✅ Python **10+ 行**搞定",
        "✅ **跨平台**：Win / Mac / Linux 通用",
        "✅ 自动化是 Python 最经典的应用之一",
    ]
    add_bullets(slide, x + Inches(0.3), y + Inches(1.6),
                w - Inches(0.6), h - Inches(1.7),
                items, font_size=12, line_spacing=1.5,
                bullet_color=PY_ACCENT_ORANGE)

    # 右侧：代码
    x2 = Inches(5.1); w2 = Inches(7.65)
    code_text = (
        'import os, shutil, sys\n'
        'from pathlib import Path\n\n'
        "# 让 Windows 控制台正确显示中文\n"
        "sys.stdout.reconfigure(encoding='utf-8')\n\n"
        "# 分类规则：后缀 → 目标文件夹\n"
        'rules = {\n'
        '    ".jpg.jpeg.png.gif.bmp":  "图片",\n'
        '    ".doc.docx.pdf.txt.md":   "文档",\n'
        '    ".xls.xlsx.csv":          "表格",\n'
        '    ".mp4.avi.mov.mp3.wav":   "音视频",\n'
        '    ".zip.rar.7z":            "压缩包",\n'
        '}\n\n'
        'downloads = Path.cwd() / "downloads_demo"\n'
        'downloads.mkdir(exist_ok=True)\n\n'
        'for file in downloads.iterdir():\n'
        '    if not file.is_file(): continue\n'
        '    for suffixes, target in rules.items():\n'
        '        if file.suffix.lower() in suffixes:\n'
        '            target_dir = downloads / target\n'
        '            target_dir.mkdir(exist_ok=True)\n'
        '            shutil.move(str(file),\n'
        '                        str(target_dir / file.name))\n'
        '            print(f"移动 {file.name} → {target}/")\n'
        '            break'
    )
    add_code_block(slide, x2, y, w2, h, code_text, font_size=10, lang="auto_organize.py")


# ============== Slide 17：AI 辅助提示 3 ==============
def slide_ai_prompts_3():
    slide = new_slide("知识点 3  ·  AI 辅助")
    add_section_title(slide, "🤖 AI 辅助：场景化选型 Prompt",
                       "让 AI 帮你选择合适的库")
    box = add_round_rect(slide, Inches(0.6), Inches(1.85),
                         Inches(12.15), Inches(4.7),
                         PY_WHITE, line_color=RGBColor(0xDD,0xE3,0xEA),
                         corner=0.04)
    add_rect(slide, Inches(0.6), Inches(1.85), Inches(12.15), Inches(0.7), PY_ACCENT_ORANGE)
    add_text(slide, Inches(0.85), Inches(1.85), Inches(11.9), Inches(0.7),
             "💬  推荐 Prompt",
             font_size=16, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    prompts = [
        ("Prompt 1", "我想做 {XX 任务}，Python 里有哪些主流库？该如何选择？"),
        ("Prompt 2", "PyTorch 和 TensorFlow 有什么区别？初学者该学哪个？"),
        ("Prompt 3", "用 Python 自动整理一个文件夹里的 Excel 文件，需要哪些库？"),
        ("Prompt 4", "我想做 Web 后端，Django / Flask / FastAPI 该如何选？"),
    ]
    by = Inches(2.75)
    bh = Inches(0.85)
    for i, (label, p) in enumerate(prompts):
        ry = by + (bh + Inches(0.05)) * i
        tag = add_round_rect(slide, Inches(0.85), ry + Inches(0.1),
                             Inches(1.2), Inches(0.6),
                             PY_ACCENT_ORANGE, corner=0.3)
        add_text(slide, Inches(0.85), ry + Inches(0.1),
                 Inches(1.2), Inches(0.6),
                 label, font_size=11, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, Inches(2.25), ry, Inches(10.3), bh,
                 p, font_size=14, color=PY_DARK,
                 anchor=MSO_ANCHOR.MIDDLE)
        if i < len(prompts) - 1:
            add_rect(slide, Inches(0.85), ry + bh,
                     Inches(11.6), Inches(0.01),
                     RGBColor(0xE5,0xE9,0xEF))


# ============== Slide 18：环境搭建步骤总览 ==============
def slide_env_steps():
    slide = new_slide("知识点 4  ·  Python 开发环境")
    add_section_title(slide, "Python 开发环境搭建 4 步走",
                       "Python 解释器 + VS Code + Trae  ·  课程统一工具链")

    steps = [
        ("1", "安装 Python 解释器",
         "方式 A：官网安装包\n方式 B：uv 一键管理（推荐）",
         PY_BLUE, "https://www.python.org/downloads/"),
        ("2", "安装 VS Code 与扩展",
         "下载 VS Code\n安装 Python 扩展（Microsoft）\n安装 Trae 插件",
         PY_BLUE_LIGHT, "https://code.visualstudio.com/"),
        ("3", "配置 Trae AI 助手",
         "Ctrl+Shift+X 安装插件\n登录账号 → 选模型 Doubao-1.5-pro\nCtrl+Shift+T 测试对话",
         PY_YELLOW, None),
        ("4", "编写第一个 Python 程序",
         "新建 hello.py\nprint(\"Hello, Python!\")\n终端运行 python hello.py",
         PY_ACCENT_GREEN, None),
    ]
    # 时间线横向布局
    total_w = Inches(11.5)
    step_w = Inches(2.7); gap = Inches(0.18)
    total_used = step_w * 4 + gap * 3
    start_x = (SLIDE_W - total_used) / 2
    y = Inches(1.95)
    h = Inches(4.7)
    for i, (no, title, desc, color, url) in enumerate(steps):
        x = start_x + (step_w + gap) * i
        # 卡片
        card = add_round_rect(slide, x, y, step_w, h, PY_WHITE,
                              line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
        # 顶部色块 + 编号
        add_rect(slide, x, y, step_w, Inches(1.1), color)
        # 编号圆
        nc = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            x + step_w/2 - Inches(0.5), y + Inches(0.25),
            Inches(1.0), Inches(1.0))
        nc.fill.solid(); nc.fill.fore_color.rgb = PY_WHITE
        nc.line.color.rgb = color; nc.line.width = Pt(3)
        add_text(slide, x + step_w/2 - Inches(0.5), y + Inches(0.25),
                 Inches(1.0), Inches(1.0),
                 no, font_size=36, bold=True, color=color,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, x + Inches(0.15), y + Inches(1.3),
                 step_w - Inches(0.3), Inches(0.55),
                 title, font_size=15, bold=True, color=PY_DARK,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 描述
        add_text(slide, x + Inches(0.15), y + Inches(1.95),
                 step_w - Inches(0.3), h - Inches(2.3),
                 desc, font_size=12, color=PY_GRAY,
                 align=PP_ALIGN.CENTER, line_spacing=1.4)
        # URL 链接（如果有）
        if url:
            add_text(slide, x + Inches(0.1), y + h - Inches(0.55),
                     step_w - Inches(0.2), Inches(0.4),
                     url, font_size=10, color=PY_BLUE_LIGHT,
                     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 19：pip vs uv ==============
def slide_pip_vs_uv():
    slide = new_slide("知识点 4  ·  pip 与 uv")
    add_section_title(slide, "pip 与 uv 的关系",
                       "uv 兼容 pip、速度更快、能力更全")

    # 左侧：pip 介绍
    x = Inches(0.6); y = Inches(1.85); w = Inches(6.0); h = Inches(4.7)
    card = add_round_rect(slide, x, y, w, h, PY_WHITE,
                          line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x, y, w, Inches(0.5), PY_BLUE)
    add_text(slide, x + Inches(0.3), y, w - Inches(0.6), Inches(0.5),
             "📦  pip  ·  Python 官方包安装器",
             font_size=15, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    pip_items = [
        "Python 官方默认包安装器",
        "适合简单装包/卸包",
        "⚠️  **直接全局 `pip install` 易污染系统 Python**",
        "推荐：**始终在虚拟环境中装包**",
    ]
    add_bullets(slide, x + Inches(0.3), y + Inches(0.7),
                w - Inches(0.6), Inches(2.5),
                pip_items, font_size=13, line_spacing=1.4)
    # pip 命令代码块
    add_text(slide, x + Inches(0.3), y + Inches(2.85),
             w - Inches(0.6), Inches(0.3),
             "常用命令：",
             font_size=12, bold=True, color=PY_GRAY)
    add_code_block(slide, x + Inches(0.3), y + Inches(3.2),
                   w - Inches(0.6), Inches(1.3),
                   "pip install requests    # 安装\n"
                   "pip uninstall requests  # 卸载\n"
                   "pip list                # 查看已安装",
                   font_size=12, lang="bash")

    # 右侧：uv 介绍
    x2 = Inches(6.85); w2 = Inches(5.9)
    card2 = add_round_rect(slide, x2, y, w2, h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x2, y, w2, Inches(0.5), PY_YELLOW)
    add_text(slide, x2 + Inches(0.3), y, w2 - Inches(0.6), Inches(0.5),
             "⚡  uv  ·  Astral 公司（Rust 实现）的一体化工具",
             font_size=15, bold=True, color=PY_BLUE,
             anchor=MSO_ANCHOR.MIDDLE)
    uv_items = [
        "**内置兼容 pip**——原 `pip install xxx` 改写为 `uv pip install xxx`",
        "速度比 pip 快 **10–100 倍**",
        "**接管 Python 解释器 / 虚拟环境 / 项目依赖**",
        "课程统一采用 uv",
    ]
    add_bullets(slide, x2 + Inches(0.3), y + Inches(0.7),
                w2 - Inches(0.6), Inches(2.5),
                uv_items, font_size=13, line_spacing=1.4,
                bullet_color=PY_ACCENT_ORANGE)
    # 对比表
    add_text(slide, x2 + Inches(0.3), y + Inches(2.85),
             w2 - Inches(0.6), Inches(0.3),
             "能力对比：",
             font_size=12, bold=True, color=PY_GRAY)
    # 简易对比表
    table_data = [
        ("装/卸包",        "✅",     "✅（更快）"),
        ("安装 Python",    "—",      "uv python install"),
        ("创建虚拟环境",    "—",      "uv venv"),
        ("依赖锁定",        "—",      "uv lock / uv sync"),
    ]
    trow_h = Inches(0.34)
    tw0 = Inches(2.2); tw1 = Inches(1.3); tw2 = Inches(1.9)
    for i, row in enumerate(table_data):
        ry = y + Inches(3.2) + trow_h * i
        bg = PY_BG_LIGHT if i % 2 == 0 else PY_WHITE
        add_rect(slide, x2 + Inches(0.3), ry,
                 tw0 + tw1 + tw2, trow_h, bg,
                 line_color=RGBColor(0xE5,0xE9,0xEF))
        add_text(slide, x2 + Inches(0.35), ry, tw0, trow_h,
                 row[0], font_size=11, color=PY_DARK,
                 anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, x2 + Inches(0.35) + tw0, ry, tw1, trow_h,
                 row[1], font_size=11, color=PY_GRAY,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, x2 + Inches(0.35) + tw0 + tw1, ry, tw2, trow_h,
                 row[2], font_size=11, color=PY_ACCENT_GREEN, bold=True,
                 anchor=MSO_ANCHOR.MIDDLE)


# ============== Slide 20：uv 虚拟环境管理 ==============
def slide_uv_venv():
    slide = new_slide("知识点 5  ·  uv 虚拟环境")
    add_section_title(slide, "使用 uv 进行虚拟环境管理",
                       "为什么需要  ·  如何创建  ·  如何使用")

    # 上方：为什么 + 为什么 uv
    ty = Inches(1.85)
    # 左：为什么
    x = Inches(0.6); w = Inches(6.0); h = Inches(2.0)
    card1 = add_round_rect(slide, x, ty, w, h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.05)
    add_rect(slide, x, ty, Inches(0.12), h, PY_BLUE)
    add_text(slide, x + Inches(0.3), ty + Inches(0.15),
             w - Inches(0.6), Inches(0.5),
             "❓  为什么需要虚拟环境？",
             font_size=15, bold=True, color=PY_BLUE)
    items = [
        "不同项目依赖同一个包的不同版本",
        "避免污染系统全局 Python 环境",
        "让项目依赖**可复现**，别人能一键装出相同环境",
    ]
    add_bullets(slide, x + Inches(0.3), ty + Inches(0.65),
                w - Inches(0.6), h - Inches(0.8),
                items, font_size=12, line_spacing=1.4)

    # 右：为什么 uv
    x2 = Inches(6.85); w2 = Inches(5.9)
    card2 = add_round_rect(slide, x2, ty, w2, h, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.05)
    add_rect(slide, x2, ty, Inches(0.12), h, PY_ACCENT_ORANGE)
    add_text(slide, x2 + Inches(0.3), ty + Inches(0.15),
             w2 - Inches(0.6), Inches(0.5),
             "⚡  为什么选 uv？",
             font_size=15, bold=True, color=PY_ACCENT_ORANGE)
    items2 = [
        "Astral 公司用 **Rust** 编写的下一代工具",
        "速度比传统 pip/virtualenv **快 10–100 倍**",
        "一个工具统一 Python / venv / 依赖 / 打包",
    ]
    add_bullets(slide, x2 + Inches(0.3), ty + Inches(0.65),
                w2 - Inches(0.6), h - Inches(0.8),
                items2, font_size=12, line_spacing=1.4,
                bullet_color=PY_ACCENT_ORANGE)

    # 下方：6 步流程
    flow_y = Inches(4.05)
    add_text(slide, Inches(0.6), flow_y, Inches(12), Inches(0.4),
             "🚀  uv 使用 6 步流程",
             font_size=16, bold=True, color=PY_BLUE)
    flow_steps = [
        ("安装 uv",   "curl/powershell\n安装脚本"),
        ("创建 venv", "uv venv"),
        ("激活 venv", ".venv\\Scripts\\activate"),
        ("装依赖",     "uv pip install"),
        ("项目化",     "uv add / uv sync"),
        ("运行",       "uv run script.py"),
    ]
    flow_w = Inches(2.0); flow_gap = Inches(0.06)
    flow_total = flow_w * 6 + flow_gap * 5
    flow_start = (SLIDE_W - flow_total) / 2
    for i, (t, c) in enumerate(flow_steps):
        fx = flow_start + (flow_w + flow_gap) * i
        fy = flow_y + Inches(0.55)
        # 卡片
        add_round_rect(slide, fx, fy, flow_w, Inches(2.0),
                       PY_WHITE, line_color=RGBColor(0xDD,0xE3,0xEA),
                       corner=0.1)
        # 顶部色
        add_rect(slide, fx, fy, flow_w, Inches(0.45), PY_BLUE_LIGHT)
        add_text(slide, fx, fy, flow_w, Inches(0.45),
                 f"Step {i+1}", font_size=11, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, fx + Inches(0.1), fy + Inches(0.5),
                 flow_w - Inches(0.2), Inches(0.45),
                 t, font_size=13, bold=True, color=PY_DARK,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 代码
        add_code_block(slide, fx + Inches(0.1), fy + Inches(1.0),
                       flow_w - Inches(0.2), Inches(0.95),
                       c, font_size=10, lang=f"step{i+1}")
        # 箭头
        if i < 5:
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                fx + flow_w + Inches(0.005), fy + Inches(0.9),
                Inches(0.05), Inches(0.2))
            arr.fill.solid(); arr.fill.fore_color.rgb = PY_BLUE_LIGHT
            arr.line.fill.background()


# ============== Slide 21：uv 速查表 + 实验 ==============
def slide_uv_cheatsheet():
    slide = new_slide("知识点 5  ·  uv 速查表")
    add_section_title(slide, "uv 速查表  &  本周实验",
                       "命令汇总  ·  动手实践  ·  验证环境")

    # 左侧：速查表
    x = Inches(0.6); y = Inches(1.85); w = Inches(6.0); h = Inches(4.7)
    card = add_round_rect(slide, x, y, w, h, PY_WHITE,
                          line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x, y, w, Inches(0.5), PY_BLUE)
    add_text(slide, x + Inches(0.3), y, w - Inches(0.6), Inches(0.5),
             "📋  uv 速查表",
             font_size=15, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
    rows = [
        ("安装 Python 版本",    "uv python install 3.12"),
        ("创建虚拟环境",         "uv venv"),
        ("激活 venv（Windows）", ".venv\\Scripts\\activate"),
        ("安装包（pip 风格）",    "uv pip install requests"),
        ("添加项目依赖",         "uv add requests"),
        ("同步项目依赖",         "uv sync"),
        ("运行脚本",            "uv run hello.py"),
        ("查看已装包",          "uv pip list"),
    ]
    row_h = Inches(0.42)
    for i, (t, c) in enumerate(rows):
        ry = y + Inches(0.65) + row_h * i
        bg = PY_BG_LIGHT if i % 2 == 0 else PY_WHITE
        add_rect(slide, x + Inches(0.2), ry, w - Inches(0.4), row_h, bg,
                 line_color=RGBColor(0xE5,0xE9,0xEF))
        add_text(slide, x + Inches(0.3), ry, Inches(2.3), row_h,
                 t, font_size=12, color=PY_DARK,
                 anchor=MSO_ANCHOR.MIDDLE)
        # 代码风格
        code_box = add_round_rect(slide, x + Inches(2.65), ry + Inches(0.06),
                                  Inches(3.0), row_h - Inches(0.12),
                                  PY_CODE_BG, corner=0.25)
        add_text(slide, x + Inches(2.75), ry + Inches(0.06),
                 Inches(2.9), row_h - Inches(0.12),
                 c, font_size=11, color=PY_CODE_FG,
                 font_name="Consolas",
                 anchor=MSO_ANCHOR.MIDDLE)

    # 右侧：3 个实验
    x2 = Inches(6.85); w2 = Inches(5.9); h2 = Inches(4.7)
    card2 = add_round_rect(slide, x2, y, w2, h2, PY_WHITE,
                           line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
    add_rect(slide, x2, y, w2, Inches(0.5), PY_ACCENT_GREEN)
    add_text(slide, x2 + Inches(0.3), y, w2 - Inches(0.6), Inches(0.5),
             "🧪  本周 3 个实验",
             font_size=15, bold=True, color=PY_WHITE,
             anchor=MSO_ANCHOR.MIDDLE)

    experiments = [
        ("实验 1", "安装并验证 Python 与 uv",
         "• 安装 Python 3.11/3.12（勾选 Add to PATH）\n"
         "• 安装 uv，运行 `uv --version`\n"
         "• 运行 `python --version` 验证"),
        ("实验 2", "创建第一个虚拟环境项目",
         "• mkdir week1_hello && cd week1_hello\n"
         "• uv venv --python 3.12\n"
         "• uv pip install requests\n"
         "• deactivate 退出"),
        ("实验 3", "用项目化方式管理（进阶）",
         "• uv init week1_proj\n"
         "• uv add requests\n"
         "• uv run python -c \"...\""),
    ]
    ey = y + Inches(0.7)
    eh = Inches(1.25)
    for i, (label, title, content) in enumerate(experiments):
        ry = ey + (eh + Inches(0.1)) * i
        # 左侧标号
        tag = add_round_rect(slide, x2 + Inches(0.2), ry + Inches(0.15),
                             Inches(0.65), Inches(0.4),
                             PY_ACCENT_GREEN, corner=0.3)
        add_text(slide, x2 + Inches(0.2), ry + Inches(0.15),
                 Inches(0.65), Inches(0.4),
                 label, font_size=10, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, x2 + Inches(0.95), ry + Inches(0.1),
                 w2 - Inches(1.1), Inches(0.4),
                 title, font_size=13, bold=True, color=PY_DARK)
        # 内容
        add_text(slide, x2 + Inches(0.95), ry + Inches(0.5),
                 w2 - Inches(1.1), Inches(0.75),
                 content, font_size=11, color=PY_GRAY, line_spacing=1.3)


# ============== Slide 22：课堂练习 ==============
def slide_exercises():
    slide = new_slide("课堂练习")
    add_section_title(slide, "课堂练习",
                       "完成以下 4 题，巩固环境与 Python 心智模型")

    exercises = [
        ("【1】", "多版本解释器切换",
         "用官网安装包安装 Python 3.10 与 3.11，用 `uv python install` 安装 3.13 与 3.14。\n新建 `week1_proj`，分别用不同解释器跑同一段脚本，打印 `sys.version`，体会多版本切换。",
         "20 min", PY_BLUE),
        ("【2】", "虚拟环境依赖隔离",
         "① 用标准库 `venv` 创建虚拟环境，安装 numpy；\n② 用 `uv` 创建并激活虚拟环境，安装 numpy；\n③ 退出虚拟环境，全局环境安装 numpy。\n对比三条安装路径的差异，说明虚拟环境如何隔离依赖。",
         "25 min", PY_BLUE_LIGHT),
        ("【3】", "跑通本课示例",
         "跑通本课对应的所有示例代码（hello world、文件归档、环境检测等）。\n写下你思考的内容：哪些代码让你眼前一亮？哪些地方卡住了？",
         "15 min", PY_ACCENT_GREEN),
        ("【4】", "AI 多轮追问",
         "阅读本节内容，挑出有疑惑的部分，向 AI 聊天工具提问。\n通过多轮追问深入理解，然后将你的理解陈述给 AI，请它判断你是否理解正确。\n最后将聊天记录截图提交。",
         "20 min", PY_ACCENT_ORANGE),
    ]
    # 2x2 网格
    cw = Inches(6.05); ch = Inches(2.55)
    gx = Inches(0.15); gy = Inches(0.15)
    start_x = Inches(0.6); start_y = Inches(1.85)
    for i, (label, title, desc, time, color) in enumerate(exercises):
        r = i // 2
        c = i % 2
        x = start_x + c * (cw + gx)
        y = start_y + r * (ch + gy)
        card = add_round_rect(slide, x, y, cw, ch, PY_WHITE,
                              line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.04)
        # 左侧色块
        add_rect(slide, x, y, Inches(0.12), ch, color)
        # 题号
        tag = add_round_rect(slide, x + Inches(0.3), y + Inches(0.2),
                             Inches(0.85), Inches(0.45),
                             color, corner=0.25)
        add_text(slide, x + Inches(0.3), y + Inches(0.2),
                 Inches(0.85), Inches(0.45),
                 label, font_size=12, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, x + Inches(1.3), y + Inches(0.18),
                 cw - Inches(2.5), Inches(0.5),
                 title, font_size=16, bold=True, color=PY_DARK,
                 anchor=MSO_ANCHOR.MIDDLE)
        # 时间
        time_tag = add_round_rect(slide, x + cw - Inches(1.1), y + Inches(0.25),
                                  Inches(0.95), Inches(0.35),
                                  PY_BG_LIGHT, corner=0.3)
        add_text(slide, x + cw - Inches(1.1), y + Inches(0.25),
                 Inches(0.95), Inches(0.35),
                 f"⏱  {time}", font_size=10, bold=True, color=PY_BLUE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 描述
        add_text(slide, x + Inches(0.3), y + Inches(0.85),
                 cw - Inches(0.6), ch - Inches(1.0),
                 desc, font_size=12, color=PY_DARK, line_spacing=1.45)


# ============== Slide 23：总结 ==============
def slide_summary():
    slide = new_slide("本节总结")
    add_section_title(slide, "本节小结",
                       "一张图回顾 5 个核心知识点")

    # 5 个小卡
    items = [
        ("01", "发展史",      "1989 起，Python 3 主流，EOL 已过",      PY_BLUE),
        ("02", "语言对比",    "动态类型 + 简洁语法 + 慢但开发快",        PY_BLUE_LIGHT),
        ("03", "应用场景",    "AI / 数据科学 / Web / 自动化等 9 大方向",  PY_YELLOW),
        ("04", "环境搭建",    "Python + VS Code + Trae 工具链",          PY_ACCENT_GREEN),
        ("05", "uv 虚拟环境", "统一管理 Python / 依赖 / 项目",            PY_ACCENT_ORANGE),
    ]
    # 横向 5 列
    cw = Inches(2.4); ch = Inches(2.8); gap = Inches(0.12)
    total_w = cw * 5 + gap * 4
    start_x = (SLIDE_W - total_w) / 2
    y = Inches(1.95)
    for i, (no, title, desc, color) in enumerate(items):
        x = start_x + (cw + gap) * i
        card = add_round_rect(slide, x, y, cw, ch, PY_WHITE,
                              line_color=RGBColor(0xDD,0xE3,0xEA), corner=0.06)
        add_rect(slide, x, y, cw, Inches(0.12), color)
        # 编号圆
        nc = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            x + cw/2 - Inches(0.45), y + Inches(0.3),
            Inches(0.9), Inches(0.9))
        nc.fill.solid(); nc.fill.fore_color.rgb = color
        nc.line.fill.background()
        add_text(slide, x + cw/2 - Inches(0.45), y + Inches(0.3),
                 Inches(0.9), Inches(0.9),
                 no, font_size=24, bold=True, color=PY_WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 标题
        add_text(slide, x + Inches(0.1), y + Inches(1.3),
                 cw - Inches(0.2), Inches(0.5),
                 title, font_size=16, bold=True, color=PY_DARK,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 描述
        add_text(slide, x + Inches(0.2), y + Inches(1.85),
                 cw - Inches(0.4), Inches(0.9),
                 desc, font_size=11, color=PY_GRAY,
                 align=PP_ALIGN.CENTER, line_spacing=1.3)

    # 底部金句
    by = Inches(5.1)
    quote_box = add_round_rect(slide, Inches(0.6), by,
                               Inches(12.15), Inches(1.5),
                               PY_BLUE, corner=0.04)
    add_text(slide, Inches(0.6), by + Inches(0.2),
             Inches(12.15), Inches(0.5),
             "下周预告",
             font_size=14, bold=True, color=PY_YELLOW,
             align=PP_ALIGN.CENTER)
    add_text(slide, Inches(0.6), by + Inches(0.6),
             Inches(12.15), Inches(0.8),
             "第 2 周  ·  Python 基础语法：变量、数据类型、运算符、流程控制\n（动手写更多 Python 代码，从「Hello World」走向「能用的程序」）",
             font_size=16, color=PY_WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.4)


# ============== Slide 24：答疑 & 致谢 ==============
def slide_qa():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, PY_WHITE)
    # 左侧大色块
    add_rect(slide, 0, 0, Inches(6.5), SLIDE_H, PY_BLUE)
    # 装饰
    deco = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        Inches(5.5), Inches(-1.0), Inches(3.5), Inches(3.5))
    deco.fill.solid(); deco.fill.fore_color.rgb = PY_BLUE_LIGHT
    deco.line.fill.background()
    deco2 = slide.shapes.add_shape(MSO_SHAPE.OVAL,
        Inches(5.8), Inches(5.5), Inches(2.5), Inches(2.5))
    deco2.fill.solid(); deco2.fill.fore_color.rgb = PY_YELLOW
    deco2.line.fill.background()

    # 大字 Q&A
    add_text(slide, Inches(0.7), Inches(2.0), Inches(6), Inches(1.5),
             "Q & A", font_size=110, bold=True, color=PY_WHITE)
    add_rect(slide, Inches(0.85), Inches(3.85), Inches(1.5), Inches(0.08), PY_YELLOW)
    add_text(slide, Inches(0.7), Inches(4.0), Inches(6), Inches(0.6),
             "提问 · 讨论 · 交流", font_size=24, color=PY_YELLOW)
    add_text(slide, Inches(0.7), Inches(4.7), Inches(6), Inches(0.5),
             "Questions & Discussions",
             font_size=14, color=RGBColor(0xC9,0xD8,0xE6))
    add_text(slide, Inches(0.7), Inches(6.4), Inches(6), Inches(0.4),
             "感谢聆听  ·  Thank You",
             font_size=16, bold=True, color=PY_WHITE)

    # 右侧金句
    add_text(slide, Inches(7.0), Inches(1.8), Inches(5.8), Inches(0.5),
             "今日一句",
             font_size=14, bold=True, color=PY_YELLOW)
    add_text(slide, Inches(7.0), Inches(2.3), Inches(5.8), Inches(2.0),
             "「Readability counts.」",
             font_size=30, bold=True, color=PY_BLUE)
    add_text(slide, Inches(7.0), Inches(3.4), Inches(5.8), Inches(1.0),
             "「可读性至上。」",
             font_size=22, color=PY_DARK)
    add_rect(slide, Inches(7.0), Inches(4.6), Inches(1.0), Inches(0.06), PY_YELLOW)
    add_text(slide, Inches(7.0), Inches(4.8), Inches(5.8), Inches(0.5),
             "—— The Zen of Python",
             font_size=14, color=PY_GRAY)

    # 联系方式
    add_text(slide, Inches(7.0), Inches(5.6), Inches(5.8), Inches(0.4),
             "📚  课程资源", font_size=14, bold=True, color=PY_BLUE)
    add_text(slide, Inches(7.0), Inches(6.0), Inches(5.8), Inches(0.4),
             "课件代码 · 课堂练习 · AI Prompt 模板",
             font_size=12, color=PY_DARK)


# ============== 主流程 ==============
if __name__ == "__main__":
    slide_cover()                            # 1. 封面
    slide_goals()                            # 2. 本周目标
    slide_agenda()                           # 3. 课程导览
    slide_section_divider("01", "Python 发展史", "Origin · Versions · Zen", PY_BLUE)  # 4
    slide_python_origin()                    # 5
    slide_python_versions()                  # 6
    slide_py2_py3()                          # 7
    slide_zen()                              # 8
    slide_python_today()                     # 9
    slide_ai_prompts_1()                     # 10

    slide_section_divider("02", "Python vs Java/C++", "Multi-dimension Comparison", PY_BLUE_LIGHT)  # 11
    slide_compare_table()                    # 12
    slide_hello_compare()                    # 13
    slide_type_loop()                        # 14
    slide_ai_prompts_2()                     # 15

    slide_section_divider("03", "Python 应用场景", "AI · Data Science · Web · …", PY_YELLOW)  # 16
    slide_applications()                     # 17
    slide_automation_code()                  # 18
    slide_ai_prompts_3()                     # 19

    slide_section_divider("04", "开发环境搭建", "Python + VS Code + Trae", PY_ACCENT_GREEN)  # 20
    slide_env_steps()                        # 21
    slide_pip_vs_uv()                        # 22

    slide_section_divider("05", "uv 虚拟环境", "Modern Python Project Management", PY_ACCENT_ORANGE)  # 23
    slide_uv_venv()                          # 24
    slide_uv_cheatsheet()                    # 25

    slide_exercises()                        # 26
    slide_summary()                          # 27
    slide_qa()                               # 28

    # 保存
    import os, sys
    output_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.getcwd(), "第1周_Python导论与环境搭建.pptx")
    out_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(out_dir, exist_ok=True)
    prs.save(output_path)
    # 设置 stdout 编码为 utf-8
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(f"[OK] PPT generated successfully! Total slides: {len(prs.slides)}")
    print(f"[PATH] {output_path}")