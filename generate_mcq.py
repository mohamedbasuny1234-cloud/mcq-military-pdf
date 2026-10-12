# -*- coding: utf-8 -*-
"""
مولّد PDF لأسئلة MCQ من الكتاب العسكري
الفصل الأول: الاستطلاع التكتيكي
"""

import os
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

# ============================================
# 1) تحميل الخط العربي
# ============================================
FONT_URL = "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/amiri/Amiri-Regular.ttf"
FONT_PATH = "Amiri-Regular.ttf"

if not os.path.exists(FONT_PATH):
    print("⏳ جاري تحميل الخط العربي...")
    urllib.request.urlretrieve(FONT_URL, FONT_PATH)
    print("✅ تم تحميل الخط")

pdfmetrics.registerFont(TTFont('Arabic', FONT_PATH))


def ar(text):
    return get_display(arabic_reshaper.reshape(text))


# ============================================
# 2) قاعدة الأسئلة (MCQ)
# ============================================
# كل سؤال: (نص السؤال، [الاختيارات], رقم الإجابة الصح)
QUESTIONS = [
    # --- الفصل الأول: الاستطلاع التكتيكي ---
    ("من الذي ينظم الاستطلاع التكتيكي؟",
     ["قادة التشكيلات والوحدات الفرعية", "قائد الجيش فقط", "قائد الفرقة فقط", "القيادة العامة"],
     0),

    ("متى يُنظَّم الاستطلاع التكتيكي؟",
     ["في وقت الحرب فقط", "في وقت السلم فقط", "في وقت الحرب ووقت السلم", "في التدريبات فقط"],
     0),

    ("ما الغرض من الاستطلاع التكتيكي؟",
     ["الحصول على المعلومات عن العدو والأرض والطقس", "الهجوم على العدو مباشرة",
      "تأمين المؤن فقط", "تدريب الأفراد فقط"],
     0),

    ("من يستفيد من المعلومات التي يحصل عليها الاستطلاع التكتيكي؟",
     ["القادة على المستوى التكتيكي فقط", "القادة على المستوى التعبوي فقط",
      "القادة على المستوى التكتيكي والتعبوي والاستراتيجي", "الأفراد فقط"],
     2),

    ("أي من التالي يُعد من أنواع الاستطلاع التكتيكي؟",
     ["استطلاع القوات", "استطلاع مؤخرة العدو", "استطلاع المدفعية", "كل ما سبق"],
     3),

    ("ما هو استطلاع القوات؟",
     ["استطلاع يتم بواسطة القوات مباشرة", "استطلاع يتم بواسطة الطائرات",
      "استطلاع يتم بواسطة الأقمار الصناعية", "استطلاع يتم بواسطة السفن"],
     0),

    ("ما هو استطلاع مؤخرة العدو؟",
     ["استطلاع المناطق الأمامية", "استطلاع المناطق الخلفية للعدو",
      "استطلاع المناطق الجوية", "استطلاع المناطق البحرية"],
     1),

    ("يُنفَّذ استطلاع القوات بالعناصر الآتية:",
     ["نقاط المراقبة والتنصت", "مجموعات الإغارة",
      "مجموعات الكمين ودوريات الاستطلاع", "كل ما سبق"],
     3),

    ("من العناصر التي تُنفّذ استطلاع القوات:",
     ["مجموعات الاستطلاع", "مجموعات استطلاع الضباط",
      "المجموعات المكلفة بتنفيذ الاستطلاع بقوة", "كل ما سبق"],
     3),

    ("بأي طرق يُنفَّذ استطلاع القوات؟",
     ["المراقبة والتنصت", "الإغارة والاقتحام المفاجئ",
      "الكمين (مدبر - سريع)", "كل ما سبق"],
     3),

    ("أي من الطرق التالية تُستخدم في استطلاع القوات؟",
     ["البحث والتفتيش", "الفحص والتصوير الأرضي", "الاستطلاع بقوة", "كل ما سبق"],
     3),

    ("من طرق استطلاع القوات أيضاً:",
     ["الاستطلاع بالقتال", "استجواب الأسرى وسؤال السكان المحليين", "كل ما سبق", "لا شيء مما سبق"],
     2),

    ("يُنظَّم الاستطلاع التكتيكي بواسطة:",
     ["قادة التشكيلات والوحدات الفرعية", "قائد الجيش", "القيادة العامة", "المنطقة العسكرية"],
     0),

    ("من متطلبات تنظيم وإدارة الاستطلاع التكتيكي:",
     ["الاستمرار", "النشاط", "التوقيت (في الوقت المناسب)", "كل ما سبق"],
     3),

    ("يتحقق \"الاستمرار\" في الاستطلاع التكتيكي بـ:",
     ["إدارته بصفة دائمة في جميع أنواع ومراحل أعمال القتال نهاراً وليلاً",
      "إدارته في وقت السلم فقط", "إدارته في وقت الحرب فقط", "إدارته في التدريبات فقط"],
     0),

    ("يتحقق \"الاستمرار\" أيضاً بـ:",
     ["الاستغلال الكامل لإمكانيات قوات ووسائل الاستطلاع المتيسرة",
      "السيطرة والمتابعة المستمرة لعناصر الاستطلاع", "كل ما سبق", "لا شيء مما سبق"],
     2),

    ("يتحقق \"النشاط\" في الاستطلاع التكتيكي بـ:",
     ["إصرار جميع القادة والقيادات وعناصر الاستطلاع على جمع المعلومات",
      "الجلوس وانتظار المعلومات", "عدم الاهتمام بالمعلومات", "لا شيء مما سبق"],
     0),

    ("يتحقق \"التوقيت (في الوقت المناسب)\" بـ:",
     ["تحديد الحد الأقصى لوقت وصول المعلومات للقادة",
      "تخطيط وتنفيذ الاستطلاع في وقت مبكر لعمق كبير من العدو",
      "تحقيق الاتصال المستمر بين عناصر الاستطلاع العاملة وقياداتها", "كل ما سبق"],
     3),

    ("يتحقق \"التوكيد\" في الاستطلاع التكتيكي بـ:",
     ["الحصول على المعلومات بأكثر من مصدر أو عنصر ومقارنتها ببعضها",
      "الاعتماد على مصدر واحد فقط", "تأخير المعلومات", "إخفاء المعلومات"],
     0),

    ("يتحقق \"التوكيد\" أيضاً بـ:",
     ["تحقيق وتأكيد المعلومات المشكوك فيها وإجراء استطلاع إضافي",
      "الإلمام بعقائد وتكتيكات العدو للتمكن من اكتشاف نواياه",
      "كل ما سبق", "لا شيء مما سبق"],
     2),

    ("يشمل تأمين عناصر الاستطلاع من أعمال العدو المضادة:",
     ["المحافظة على سرية التخطيط للاستطلاع",
      "مراعاة السرية التامة في تحضير وتجهيز ودفع عناصر الاستطلاع",
      "تأمين عناصر الاستطلاع أثناء تنفيذها لمهامها", "كل ما سبق"],
     3),

    ("يتحقق \"الهدف\" في الاستطلاع التكتيكي بـ:",
     ["أن يتماشى استخدام جهود الاستطلاع المختلفة مع مهام القتال للوحدات",
      "تشتيت الجهود", "إهمال المهام", "لا شيء مما سبق"],
     0),
]


# ============================================
# 3) بناء PDF
# ============================================
doc = SimpleDocTemplate(
    "MCQ_Military_Book.pdf",
    pagesize=A4,
    rightMargin=1.5*cm, leftMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('T', parent=styles['Title'],
    fontName='Arabic', fontSize=22, alignment=1,
    textColor=colors.HexColor('#2C3E50'), leading=30)

section_style = ParagraphStyle('Sec', parent=styles['Heading1'],
    fontName='Arabic', fontSize=16, alignment=2,
    textColor=colors.HexColor('#2980B9'),
    spaceAfter=10, spaceBefore=10)

q_style = ParagraphStyle('Q', parent=styles['Normal'],
    fontName='Arabic', fontSize=12, alignment=2,
    textColor=colors.HexColor('#2C3E50'),
    spaceBefore=8, spaceAfter=6, leading=18)

a_style = ParagraphStyle('A', parent=styles['Normal'],
    fontName='Arabic', fontSize=11, alignment=2,
    leading=16, rightIndent=15)


def build_answer(key, options, correct):
    """يبني جدول الاختيارات مع علامة ✓ على الصح"""
    letters = ["أ", "ب", "ج", "د"]
    rows = []
    for i, opt in enumerate(options):
        mark = "✅" if i == correct else "⬜"
        rows.append([
            Paragraph(ar(f"{mark} {letters[i]}) {opt}"), a_style)
        ])
    table = Table(rows, colWidths=[16*cm])
    table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('BACKGROUND', (0, correct), (0, correct), colors.HexColor('#D5F5E3')),
    ]))
    return table


elements = []

# الغلاف
elements.append(Spacer(1, 5*cm))
elements.append(Paragraph(ar("أسئلة اختيار من متعدد"), title_style))
elements.append(Spacer(1, 0.5*cm))
elements.append(Paragraph(ar("من الكتاب العسكري"), title_style))
elements.append(Spacer(1, 1*cm))
elements.append(Paragraph(ar("الفصل الأول: الاستطلاع التكتيكي"), title_style))
elements.append(Spacer(1, 0.5*cm))
elements.append(Paragraph(ar(f"عدد الأسئلة: {len(QUESTIONS)}"), title_style))
elements.append(PageBreak())

# الفصل
elements.append(Paragraph(ar("الفصل الأول: الاستطلاع التكتيكي"), section_style))
elements.append(Spacer(1, 0.3*cm))

for i, (q, opts, correct) in enumerate(QUESTIONS, 1):
    elements.append(Paragraph(ar(f"س{i}: {q}"), q_style))
    elements.append(build_answer(i, opts, correct))
    elements.append(Spacer(1, 0.3*cm))

doc.build(elements)

print(f"✅ تم إنشاء الملف: MCQ_Military_Book.pdf")
print(f"📊 عدد الأسئلة: {len(QUESTIONS)}")
