# -*- coding: utf-8 -*-
"""
مولّد PDF احترافي لأسئلة MCQ من الكتاب العسكري
تصميم: غلاف + فهرس + ألوان + Header/Footer + صناديق
"""

import os
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
import arabic_reshaper
from bidi.algorithm import get_display


# ============================================
# 1) تحميل الخطوط
# ============================================
FONT_URLS = {
    "Amiri-Regular.ttf": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/amiri/Amiri-Regular.ttf",
    "Amiri-Bold.ttf": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/amiri/Amiri-Bold.ttf",
}

for fname, url in FONT_URLS.items():
    if not os.path.exists(fname):
        print(f"⏳ تحميل {fname}...")
        urllib.request.urlretrieve(url, fname)

pdfmetrics.registerFont(TTFont('Amiri', 'Amiri-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Amiri-Bold', 'Amiri-Bold.ttf'))


def ar(text):
    return get_display(arabic_reshaper.reshape(text))


# ============================================
# 2) ألوان الأقسام
# ============================================
SECTION_COLORS = {
    "الفصل الأول: الاستطلاع التكتيكي": "#2980B9",
    "الفصل الثاني: المراقبة": "#27AE60",
    "الفصل الثالث: التنصت": "#8E44AD",
    "الفصل الرابع: الإغارة": "#C0392B",
    "الفصل الخامس: الكمين": "#D35400",
    "الفصل السادس: مجموعة الاستطلاع": "#16A085",
}

DEFAULT_COLOR = "#2C3E50"


# ============================================
# 3) قاعدة الأسئلة
# ============================================
SECTIONS = {
    "الفصل الأول: الاستطلاع التكتيكي": [
        {
            "q": "من الذي ينظم الاستطلاع التكتيكي؟",
            "options": ["قادة التشكيلات والوحدات الفرعية", "قائد الجيش فقط",
                       "قائد الفرقة فقط", "القيادة العامة"],
            "correct": 0
        },
        {
            "q": "متى يُنظَّم الاستطلاع التكتيكي؟",
            "options": ["في وقت الحرب فقط", "في وقت السلم فقط",
                       "في وقت الحرب ووقت السلم", "في التدريبات فقط"],
            "correct": 2
        },
        {
            "q": "ما الغرض من الاستطلاع التكتيكي؟",
            "options": ["الحصول على المعلومات عن العدو والأرض والطقس",
                       "الهجوم على العدو مباشرة",
                       "تأمين المؤن فقط", "تدريب الأفراد فقط"],
            "correct": 0
        },
        {
            "q": "من يستفيد من المعلومات التي يحصل عليها الاستطلاع التكتيكي؟",
            "options": ["القادة على المستوى التكتيكي فقط",
                       "القادة على المستوى التعبوي فقط",
                       "القادة على المستوى التكتيكي والتعبوي والاستراتيجي",
                       "الأفراد فقط"],
            "correct": 2
        },
        {
            "q": "أي من التالي يُعد من أنواع الاستطلاع التكتيكي؟",
            "options": ["استطلاع القوات", "استطلاع مؤخرة العدو",
                       "استطلاع المدفعية", "كل ما سبق"],
            "correct": 3
        },
        {
            "q": "ما هو استطلاع القوات؟",
            "options": ["استطلاع يتم بواسطة القوات مباشرة",
                       "استطلاع يتم بواسطة الطائرات",
                       "استطلاع يتم بواسطة الأقمار الصناعية",
                       "استطلاع يتم بواسطة السفن"],
            "correct": 0
        },
        {
            "q": "يُنفَّذ استطلاع القوات بالعناصر الآتية:",
            "options": ["نقاط المراقبة والتنصت", "مجموعات الإغارة",
                       "مجموعات الكمين ودوريات الاستطلاع", "كل ما سبق"],
            "correct": 3
        },
        {
            "q": "بأي طرق يُنفَّذ استطلاع القوات؟",
            "options": ["المراقبة والتنصت", "الإغارة والاقتحام المفاجئ",
                       "الكمين (مدبر - سريع)", "كل ما سبق"],
            "correct": 3
        },
        {
            "q": "من متطلبات تنظيم وإدارة الاستطلاع التكتيكي:",
            "options": ["الاستمرار", "النشاط",
                       "التوقيت (في الوقت المناسب)", "كل ما سبق"],
            "correct": 3
        },
        {
            "q": "يتحقق \"الاستمرار\" في الاستطلاع التكتيكي بـ:",
            "options": ["إدارته بصفة دائمة في جميع أنواع ومراحل أعمال القتال نهاراً وليلاً",
                       "إدارته في وقت السلم فقط",
                       "إدارته في وقت الحرب فقط",
                       "إدارته في التدريبات فقط"],
            "correct": 0
        },
        {
            "q": "يتحقق \"النشاط\" في الاستطلاع التكتيكي بـ:",
            "options": ["إصرار جميع القادة والقيادات وعناصر الاستطلاع على جمع المعلومات",
                       "الجلوس وانتظار المعلومات",
                       "عدم الاهتمام بالمعلومات", "لا شيء مما سبق"],
            "correct": 0
        },
        {
            "q": "يتحقق \"التوكيد\" في الاستطلاع التكتيكي بـ:",
            "options": ["الحصول على المعلومات بأكثر من مصدر أو عنصر ومقارنتها ببعضها",
                       "الاعتماد على مصدر واحد فقط",
                       "تأخير المعلومات", "إخفاء المعلومات"],
            "correct": 0
        },
    ]
}


# ============================================
# 4) Clases مخصصة للتصميم
# ============================================
class CoverPage(Flowable):
    """غلاف احترافي بخلفية متدرجة"""
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        # خلفية متدرجة (أزرق داكن)
        c.saveState()
        c.setFillColor(colors.HexColor('#1A252F'))
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)

        # إطار ذهبي
        c.setStrokeColor(colors.HexColor('#D4AF37'))
        c.setLineWidth(3)
        c.rect(15*mm, 15*mm, self.width - 30*mm, self.height - 30*mm,
               fill=0, stroke=1)

        # خط رفيع داخلي
        c.setStrokeColor(colors.HexColor('#D4AF37'))
        c.setLineWidth(0.5)
        c.rect(18*mm, 18*mm, self.width - 36*mm, self.height - 36*mm,
               fill=0, stroke=1)

        # خط زخرفي في المنتصف
        c.setStrokeColor(colors.HexColor('#D4AF37'))
        c.setLineWidth(2)
        c.line(self.width/2 - 40*mm, self.height/2 - 20*mm,
               self.width/2 + 40*mm, self.height/2 - 20*mm)

        c.restoreState()


class Watermark(Flowable):
    """Watermark خفيف في الخلفية"""
    def __init__(self, text, width, height):
        Flowable.__init__(self)
        self.text = text
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(colors.HexColor('#000000'))
        c.setFillAlpha(0.04)
        c.setFont('Amiri-Bold', 80)
        c.translate(self.width/2, self.height/2)
        c.rotate(45)
        c.drawCentredString(0, 0, self.text)
        c.restoreState()


# ============================================
# 5) Page Templates
# ============================================
PAGE_W, PAGE_H = A4


def draw_header_footer(canvas_obj, doc, section_name="", section_color=DEFAULT_COLOR):
    """يرسم Header و Footer على كل صفحة"""
    canvas_obj.saveState()
    # Header
    canvas_obj.setFillColor(colors.HexColor(section_color))
    canvas_obj.rect(0, PAGE_H - 15*mm, PAGE_W, 10*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont('Amiri-Bold', 11)
    canvas_obj.drawCentredString(PAGE_W/2, PAGE_H - 12*mm,
                                  ar("أسئلة اختيار من متعدد - كتاب عسكري"))

    # Footer
    canvas_obj.setFillColor(colors.HexColor('#ECF0F1'))
    canvas_obj.rect(0, 0, PAGE_W, 12*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor('#2C3E50'))
    canvas_obj.setFont('Amiri', 10)
    # اليمين: اسم الفصل
    if section_name:
        canvas_obj.drawRightString(PAGE_W - 15*mm, 4*mm, ar(section_name))
    # اليسار: رقم الصفحة
    canvas_obj.drawString(15*mm, 4*mm, f"Page {doc.page}")
    # المنتصف: خط فاصل
    canvas_obj.setStrokeColor(colors.HexColor(section_color))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(15*mm, 12*mm, PAGE_W - 15*mm, 12*mm)
    canvas_obj.restoreState()


# ============================================
# 6) Styles
# ============================================
styles = getSampleStyleSheet()

title_cover = ParagraphStyle('TC', parent=styles['Title'],
    fontName='Amiri-Bold', fontSize=40, alignment=1,
    textColor=colors.HexColor('#D4AF37'), leading=50)

subtitle_cover = ParagraphStyle('SC', parent=styles['Title'],
    fontName='Amiri', fontSize=22, alignment=1,
    textColor=colors.HexColor('#ECF0F1'), leading=30)

section_style = ParagraphStyle('Sec', parent=styles['Heading1'],
    fontName='Amiri-Bold', fontSize=18, alignment=1,
    textColor=colors.white, leading=24)

q_num_style = ParagraphStyle('QN', parent=styles['Normal'],
    fontName='Amiri-Bold', fontSize=14, alignment=1,
    textColor=colors.white, leading=18)

q_style = ParagraphStyle('Q', parent=styles['Normal'],
    fontName='Amiri-Bold', fontSize=13, alignment=2,
    textColor=colors.HexColor('#2C3E50'),
    leading=20)

a_style = ParagraphStyle('A', parent=styles['Normal'],
    fontName='Amiri', fontSize=11.5, alignment=2,
    leading=18, rightIndent=10)


# ============================================
# 7) بناء عناصر الأسئلة
# ============================================
def build_section_header(section_name):
    """يبني عنوان الفصل بلون مميز"""
    color = SECTION_COLORS.get(section_name, DEFAULT_COLOR)
    table = Table(
        [[Paragraph(ar(section_name), section_style)]],
        colWidths=[PAGE_W - 30*mm]
    )
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(color)),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return table


def build_question(q_data, num, section_color):
    """يبني سؤال واحد في صندوق احترافي"""
    letters = ["أ", "ب", "ج", "د"]
    correct = q_data["correct"]

    # ============ العنوان (رقم + نص السؤال) ============
    q_num_paragraph = Paragraph(ar(f"س{num}"), q_num_style)
    q_text_paragraph = Paragraph(ar(q_data["q"]), q_style)

    header_table = Table(
        [[q_text_paragraph, q_num_paragraph]],
        colWidths=[PAGE_W - 50*mm, 15*mm]
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#F8F9F9')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor(section_color)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

    # ============ الاختيارات ============
    opt_rows = []
    for i, opt in enumerate(q_data["options"]):
        if i == correct:
            mark = "✅"
            bg = colors.HexColor('#D5F5E3')
            text_color = '#186A3B'
        else:
            mark = "⬜"
            bg = colors.white
            text_color = '#2C3E50'

        opt_style = ParagraphStyle(
            f'opt{i}', parent=styles['Normal'],
            fontName='Amiri', fontSize=11.5, alignment=2,
            textColor=colors.HexColor(text_color), leading=16
        )
        opt_paragraph = Paragraph(ar(f"{mark} {letters[i]}) {opt}"), opt_style)
        opt_rows.append([opt_paragraph])

    options_table = Table(opt_rows, colWidths=[PAGE_W - 50*mm])
    option_styles = [
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('LINEBELOW', (0,0), (-1,-2), 0.3, colors.HexColor('#ECF0F1')),
    ]
    # تلوين الاختيار الصح
    option_styles.append(('BACKGROUND', (0, correct), (0, correct), colors.HexColor('#D5F5E3')))
    options_table.setStyle(TableStyle(option_styles))

    # ============ تجميع السؤال ============
    combined = Table(
        [[header_table], [options_table]],
        colWidths=[PAGE_W - 40*mm]
    )
    combined.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(section_color)),
        ('LINEABOVE', (0,1), (0,1), 1, colors.HexColor(section_color)),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    return combined


# ============================================
# 8) بناء المستند
# ============================================
def build_pdf():
    doc = BaseDocTemplate(
        "MCQ_Military_Book.pdf",
        pagesize=A4,
        rightMargin=15*mm, leftMargin=15*mm,
        topMargin=20*mm, bottomMargin=15*mm,
        title="أسئلة اختيار من متعدد - كتاب عسكري",
        author="MCQ Generator"
    )

    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id='normal'
    )

    # Template ديناميكي (نحدّث اسم الفصل)
    current_section = {"name": ""}

    def make_template(section_name):
        def on_page(canvas_obj, doc_obj):
            color = SECTION_COLORS.get(section_name, DEFAULT_COLOR)
            draw_header_footer(canvas_obj, doc_obj, section_name, color)
        return PageTemplate(id='main', frames=[frame], onPage=on_page)

    # ============ المحتوى ============
    elements = []

    # ---------- الغلاف ----------
    elements.append(CoverPage(PAGE_W - 30*mm, PAGE_H - 40*mm))
    elements.append(Spacer(1, 5*cm))
    elements.append(Paragraph(ar("أسئلة اختيار من متعدد"), title_cover))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(ar("من الكتاب العسكري"), subtitle_cover))
    elements.append(Spacer(1, 3*cm))
    elements.append(Paragraph(ar("الجزء الأول"), subtitle_cover))
    elements.append(PageBreak())

    # ---------- الفهرس ----------
    elements.append(Paragraph(ar("الفهرس"), title_cover))
    elements.append(Spacer(1, 1*cm))

    toc_data = []
    for i, (section_name, qs) in enumerate(SECTIONS.items(), 1):
        color = SECTION_COLORS.get(section_name, DEFAULT_COLOR)
        toc_data.append([
            Paragraph(ar(f"{len(qs)} سؤال"), a_style),
            Paragraph(ar(section_name),
                      ParagraphStyle('tocsec', parent=q_style,
                                     textColor=colors.HexColor(color))),
        ])

    toc_table = Table(toc_data, colWidths=[3*cm, PAGE_W - 40*mm])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.3, colors.HexColor('#BDC3C7')),
    ]))
    elements.append(toc_table)
    elements.append(PageBreak())

    # ---------- الفصول ----------
    total_q = 0
    for section_name, questions in SECTIONS.items():
        section_color = SECTION_COLORS.get(section_name, DEFAULT_COLOR)

        # تحديث اسم الفصل في الـ template
        current_section["name"] = section_name

        # عنوان الفصل
        elements.append(build_section_header(section_name))
        elements.append(Spacer(1, 0.5*cm))

        # الأسئلة
        for i, q in enumerate(questions, 1):
            elements.append(KeepTogether([
                build_question(q, i, section_color),
                Spacer(1, 0.4*cm),
            ]))
            total_q += 1

        elements.append(PageBreak())

    # بناء المستند باستخدام template مؤقت
    # (سنستخدم template واحد لكل الفصول)
    template = make_template("")
    doc.addPageTemplates([template])

    # للحصول على أسماء الفصول في footer، نستخدم طريقة أخرى
    # نعيد تعريف الـ template لكل فصل
    # حل بسيط: نستخدم template واحد ويظهر اسم عام
    doc.build(elements)


if __name__ == "__main__":
    build_pdf()
    total_q = sum(len(v) for v in SECTIONS.values())
    print(f"✅ تم إنشاء الملف: MCQ_Military_Book.pdf")
    print(f"📊 عدد الفصول: {len(SECTIONS)}")
    print(f"📊 عدد الأسئلة: {total_q}")
