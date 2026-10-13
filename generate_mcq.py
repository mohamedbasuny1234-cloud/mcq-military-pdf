# -*- coding: utf-8 -*-
"""
مولّد PDF احترافي لأسئلة MCQ من الكتاب العسكري
الإصدار: 3.0 - الفصول: 1 + 2 + 3 + 4
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
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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

    # ============================
    # الفصل الأول: الاستطلاع التكتيكي
    # ============================
    "الفصل الأول: الاستطلاع التكتيكي": [
        {"q": "من الذي ينظم الاستطلاع التكتيكي؟",
         "options": ["قادة التشكيلات والوحدات الفرعية", "قائد الجيش فقط",
                    "قائد الفرقة فقط", "القيادة العامة"], "correct": 0},
        {"q": "متى يُنظَّم الاستطلاع التكتيكي؟",
         "options": ["في وقت الحرب فقط", "في وقت السلم فقط",
                    "في وقت الحرب ووقت السلم", "في التدريبات فقط"], "correct": 2},
        {"q": "ما الغرض من الاستطلاع التكتيكي؟",
         "options": ["الحصول على المعلومات عن العدو والأرض والطقس",
                    "الهجوم على العدو مباشرة", "تأمين المؤن فقط",
                    "تدريب الأفراد فقط"], "correct": 0},
        {"q": "من يستفيد من المعلومات التي يحصل عليها الاستطلاع التكتيكي؟",
         "options": ["القادة على المستوى التكتيكي فقط",
                    "القادة على المستوى التعبوي فقط",
                    "القادة على المستوى التكتيكي والتعبوي والاستراتيجي",
                    "الأفراد فقط"], "correct": 2},
        {"q": "أي من التالي يُعد من أنواع الاستطلاع التكتيكي؟",
         "options": ["استطلاع القوات", "استطلاع مؤخرة العدو",
                    "استطلاع المدفعية", "كل ما سبق"], "correct": 3},
        {"q": "ما هو استطلاع القوات؟",
         "options": ["استطلاع يتم بواسطة القوات مباشرة",
                    "استطلاع يتم بواسطة الطائرات",
                    "استطلاع يتم بواسطة الأقمار الصناعية",
                    "استطلاع يتم بواسطة السفن"], "correct": 0},
        {"q": "يُنفَّذ استطلاع القوات بالعناصر الآتية:",
         "options": ["نقاط المراقبة والتنصت", "مجموعات الإغارة",
                    "مجموعات الكمين ودوريات الاستطلاع", "كل ما سبق"], "correct": 3},
        {"q": "بأي طرق يُنفَّذ استطلاع القوات؟",
         "options": ["المراقبة والتنصت", "الإغارة والاقتحام المفاجئ",
                    "الكمين (مدبر - سريع)", "كل ما سبق"], "correct": 3},
        {"q": "من متطلبات تنظيم وإدارة الاستطلاع التكتيكي:",
         "options": ["الاستمرار", "النشاط",
                    "التوقيت (في الوقت المناسب)", "كل ما سبق"], "correct": 3},
        {"q": "يتحقق \"الاستمرار\" في الاستطلاع التكتيكي بـ:",
         "options": ["إدارته بصفة دائمة في جميع أنواع ومراحل أعمال القتال نهاراً وليلاً",
                    "إدارته في وقت السلم فقط", "إدارته في وقت الحرب فقط",
                    "إدارته في التدريبات فقط"], "correct": 0},
        {"q": "يتحقق \"النشاط\" في الاستطلاع التكتيكي بـ:",
         "options": ["إصرار جميع القادة والقيادات وعناصر الاستطلاع على جمع المعلومات",
                    "الجلوس وانتظار المعلومات", "عدم الاهتمام بالمعلومات",
                    "لا شيء مما سبق"], "correct": 0},
        {"q": "يتحقق \"التوكيد\" في الاستطلاع التكتيكي بـ:",
         "options": ["الحصول على المعلومات بأكثر من مصدر أو عنصر ومقارنتها ببعضها",
                    "الاعتماد على مصدر واحد فقط",
                    "تأخير المعلومات", "إخفاء المعلومات"], "correct": 0},
    ],

    # ============================
    # الفصل الثاني: المراقبة
    # ============================
    "الفصل الثاني: المراقبة": [
        {"q": "ما هي المراقبة؟",
         "options": ["من أهم طرق الاستطلاع للحصول على المعلومات وتُستخدم في جميع صور المعركة",
                    "طريقة للهجوم على العدو", "طريقة لتأمين المؤن",
                    "طريقة للتدريب فقط"], "correct": 0},
        {"q": "أين تُستخدم المراقبة؟",
         "options": ["في المواجهة فقط", "على الأجناب والعمق فقط",
                    "في جميع الأوقات وفي كافة المستويات",
                    "في وقت السلم فقط"], "correct": 2},
        {"q": "ما هي مهام نقطة المراقبة؟",
         "options": ["تأكيد وجود العدو وتحديد قوته وتشكيله ومتابعة نشاطه",
                    "الهجوم على العدو مباشرة",
                    "تأمين الإمدادات", "تدريب الأفراد فقط"], "correct": 0},
        {"q": "من مهام نقطة المراقبة أيضاً:",
         "options": ["اكتشاف النقاط القوية وتجمعات القوات والوسائل",
                    "تحديد أماكن مراكز السيطرة ونقاط المراقبة المعادية",
                    "اكتشاف طبيعة الأرض والمشاتل الهندسية والموانع",
                    "كل ما سبق"], "correct": 3},
        {"q": "كم عدد أفراد نقطة المراقبة؟",
         "options": ["(2 - 3) فرد", "(5 - 6) أفراد",
                    "(10 - 12) فرد", "فرد واحد فقط"], "correct": 0},
        {"q": "من يعين حكمداراً لنقطة المراقبة؟",
         "options": ["أقدمهم", "أصغرهم", "قائد الوحدة", "أي فرد منهم"], "correct": 0},
        {"q": "قد تدعم نقطة المراقبة بـ:",
         "options": ["أفراد م/ع وكيما", "أفراد مشاة فقط",
                    "أفراد مدرعات فقط", "لا أحد"], "correct": 0},
        {"q": "من الشروط الواجب توافرها في نقطة المراقبة:",
         "options": ["أن يكون أمامها ميدان جيد للمراقبة والاستنار لعمق كبير",
                    "أن تكون محمية بنيران قواتنا",
                    "أن يكون لها طريق اقتراب مخفي ومستور",
                    "كل ما سبق"], "correct": 3},
        {"q": "من شروط نقطة المراقبة أيضاً:",
         "options": ["أن يكون لها نقطة تبادلية تشرف على نفس قطاع المراقبة",
                    "أن تسمح مساحة النقطة لعمل الأفراد بحرية ويسر",
                    "أن تكون في الميول الأمامية للهيئات",
                    "كل ما سبق"], "correct": 3},
        {"q": "من شروط نقطة المراقبة:",
         "options": ["أن تكون بعيدة عن الأغراض الشهيرة",
                    "أن توفر الإخفاء والاستنار لأفراد نقطة المراقبة",
                    "كل ما سبق", "لا شيء مما سبق"], "correct": 2},
        {"q": "من المعدات التي يجب توافرها بنقطة المراقبة:",
         "options": ["التسليح الشخصي والذخيرة اللازمة",
                    "مهمات الوقاية الفردية وعلب التطهير الفردي",
                    "وسيلة رؤية نهارية وليلية", "كل ما سبق"], "correct": 3},
        {"q": "من المعدات أيضاً:",
         "options": ["بوصلة", "ساعة ميقاتية",
                    "وسائل اتصال (خطي - لاسلكي - طبنجة إشارة - بيارق)",
                    "كل ما سبق"], "correct": 3},
        {"q": "من الوثائق التي يجب توافرها في نقطة المراقبة:",
         "options": ["خريطة ذات مقياس رسم كبير أو كروكي للمنطقة",
                    "سجل نقطة المراقبة",
                    "سجل الخدمة للمراقبين وسجل الأسماء الكودية",
                    "كل ما سبق"], "correct": 3},
        {"q": "من الوثائق أيضاً:",
         "options": ["سجل المرور وكروكي النقاط الإشارية",
                    "كروكي نقطة المراقبة وسجل الإشارات",
                    "نوت تمييز أسلحة ومعدات العدو وسجل إشارات التعارف",
                    "كل ما سبق"], "correct": 3},
        {"q": "ينفَّذ التنصت ليلاً وفي أحوال الرؤية الصعبة عند:",
         "options": ["عدم إمكان تنفيذ الاستطلاع بالمراقبة",
                    "توفير الوقت", "الحاجة للمعلومات فقط",
                    "تدريب الأفراد"], "correct": 0},
        {"q": "ما هي مهام نقطة التنصت؟",
         "options": ["اكتشاف وجود قوات للعدو وتحديد محلاتها وطبيعة نشاطها",
                    "اكتشاف تحركات قوات العدو بأنواعها المختلفة",
                    "اكتشاف وتحديد محلات أسلحة العدو",
                    "كل ما سبق"], "correct": 3},
        {"q": "أين تقع نقاط التنصت؟",
         "options": ["في مواقع قواتنا", "قد تدفع للأمام أقرب ما يمكن من مواقع العدو",
                    "كل ما سبق", "لا شيء مما سبق"], "correct": 2},
    ],

    # ============================
    # الفصل الثالث: التنصت
    # ============================
    "الفصل الثالث: التنصت": [
        {"q": "ينفَّذ التنصت ليلاً وفي أحوال الرؤية الصعبة عند:",
         "options": ["عدم إمكان تنفيذ الاستطلاع بالمراقبة",
                    "توفير الوقت", "الحاجة للمعلومات فقط",
                    "تدريب الأفراد"], "correct": 0},
        {"q": "ما هي مهام نقطة التنصت؟",
         "options": ["اكتشاف وجود قوات للعدو وتحديد محلاتها وطبيعة نشاطها",
                    "اكتشاف تحركات قوات العدو بأنواعها المختلفة",
                    "اكتشاف وتحديد محلات أسلحة العدو", "كل ما سبق"], "correct": 3},
        {"q": "أين تقع نقاط التنصت؟",
         "options": ["في مواقع قواتنا فقط",
                    "قد تدفع للأمام أقرب ما يمكن من مواقع العدو",
                    "في المؤخرة فقط", "خارج مسرح العمليات"], "correct": 1},
        {"q": "من مهام نقطة التنصت اكتشاف:",
         "options": ["محلات المدفعية والهاونات",
                    "أصوات المواتير والجنازير",
                    "محلات أسلحة العدو بالتعرف على الأصوات",
                    "كل ما سبق"], "correct": 3},
        {"q": "من أين تُبلغ نتائج التنصت؟",
         "options": ["تبلغ المعلومات العادية بعد العودة أو في التوقيت المحدد للتبليغ",
                    "تبلغ المعلومات الهامة فوراً",
                    "كل ما سبق", "لا شيء مما سبق"], "correct": 2},
        {"q": "أسلوب العمل في نقطة التنصت يعتمد على:",
         "options": ["دراسة مواقع الأرض في منطقة العمل",
                    "التنقل بحذر إلى نقطة التنصت",
                    "تنظيم التنصت في تشكيل حرف (Y) وقيام كل فرد بالتنصت",
                    "كل ما سبق"], "correct": 3},
        {"q": "متى تتحرك المجموعة إلى نقطة التنصت؟",
         "options": ["عند حلول الظلام (سقوط الضباب)",
                    "في منتصف النهار", "في الصباح الباكر",
                    "في أي وقت"], "correct": 0},
        {"q": "يراعى أفراد نقطة التنصت أثناء التنصت:",
         "options": ["النواحي الفنية في التنصت",
                    "تجنب صدى الصوت في المناطق الجبلية",
                    "سرعة إدارة الرأس عند سماع صوت",
                    "كل ما سبق"], "correct": 3},
        {"q": "ما هو الغرض من الاستطلاع بالمراقبة؟",
         "options": ["الحصول على المعلومات عن العدو والأرض والطقس",
                    "تحديد الأهداف للضرب", "كل ما سبق", "لا شيء مما سبق"], "correct": 2},
        {"q": "من طرق تقدير مسافة الأهداف عند سماع صوتها:",
         "options": ["حسب نوع الصوت وشدته",
                    "حسب زمن وصول الصوت", "كل ما سبق", "لا شيء مما سبق"], "correct": 2},
    ],

    # ============================
    # الفصل الرابع: الإغارة
    # ============================
    "الفصل الرابع: الإغارة": [
        {"q": "ما هي الإغارة؟",
         "options": ["أحد طرق الاستطلاع للحصول على المعلومات عن العدو",
                    "طريقة للهجوم المباشر",
                    "طريقة لتأمين الإمدادات",
                    "طريقة للتدريب فقط"], "correct": 0},
        {"q": "متى تُنفَّذ الإغارة؟",
         "options": ["في جميع صور المعركة فقط",
                    "في أوقات معينة فقط",
                    "في جميع الأوقات ليلاً ونهاراً وفي أحوال الرؤية الصعبة",
                    "في الليل فقط"], "correct": 2},
        {"q": "ما هو الاقتحام المفاجئ؟",
         "options": ["حالة تُنفَّذ فيها الإغارة على هدف منعزل في عمق تشكيل قتال العدو",
                    "حالة للهجوم العام", "حالة للدفاع",
                    "حالة للتراجع"], "correct": 0},
        {"q": "ما هو هدف الإغارة؟",
         "options": ["أفراد نقط المراقبة للعدو",
                    "أطقم الأسلحة التي تتواجد في منطقة منعزلة",
                    "المجموعات الصغيرة من الأفراد",
                    "كل ما سبق"], "correct": 3},
        {"q": "بأي قوة تُنفَّذ الإغارة عادةً؟",
         "options": ["بواسطة وحدة فرعية مشاة (استطلاع عند الضرورة)",
                    "بقوة كتيبة كاملة", "بقوة لواء كامل",
                    "بقوة فرد واحد"], "correct": 0},
        {"q": "كم عدد المجموعات الفرعية التي تنقسم إليها مجموعات الإغارة؟",
         "options": ["مجموعتان", "ثلاث مجموعات",
                    "أربع مجموعات", "خمس مجموعات"], "correct": 1},
        {"q": "ما هي المجموعات الفرعية للإغارة؟",
         "options": ["مجموعة الاقتحام", "مجموعة الوقاية",
                    "مجموعة التطهير وفتح الثغرة", "كل ما سبق"], "correct": 3},
        {"q": "من مهام مجموعة الاقتحام:",
         "options": ["تنفيذ مهمة الإغارة بخطف الأسير أو الاستيلاء على وثائق",
                    "الهجوم على العدو مباشرة",
                    "تأمين الإمدادات", "تدريب الأفراد فقط"], "correct": 0},
        {"q": "كم عدد أفراد مجموعة الاقتحام؟",
         "options": ["(2 - 3) فرد", "(8 - 6) أفراد",
                    "(10 - 12) فرد", "فرد واحد فقط"], "correct": 0},
        {"q": "بماذا تسلح مجموعة الاقتحام؟",
         "options": ["بالبنادق الآلية والقنابل الهجومية وكمامات ورباط الأسير",
                    "بالأسلحة الثقيلة فقط",
                    "بالأسلحة الخفيفة فقط",
                    "لا شيء مما سبق"], "correct": 0},
        {"q": "من مهام مجموعة الوقاية:",
         "options": ["تأمين تحرك قوة الكمين من الأمام",
                    "ستر أعمال مجموعة الاقتحام وتأمين تحرك المجموعة وارتدادها",
                    "الهجوم على العدو مباشرة",
                    "تأمين الإمدادات"], "correct": 1},
        {"q": "كم عدد أفراد مجموعة الوقاية؟",
         "options": ["(2 - 3) فرد", "(8 - 6) أفراد",
                    "(10 - 12) فرد", "فرد واحد فقط"], "correct": 1},
        {"q": "من مهام مجموعة التطهير وفتح الثغرة:",
         "options": ["فتح ثغرة في حقول الألغام",
                    "تأمين تحرك قوة الإغارة من الأمام",
                    "الهجوم على العدو مباشرة",
                    "لا شيء مما سبق"], "correct": 0},
        {"q": "ما هي عوامل نجاح الإغارة؟",
         "options": ["تخصيص المهمة لقائد مجموعة الإغارة في توقيت مبكر",
                    "سرية إجراءات التنظيم",
                    "توفير المعاونة النيرانية الكافية",
                    "كل ما سبق"], "correct": 3},
        {"q": "من عوامل نجاح الإغارة أيضاً:",
         "options": ["التخطيط الجيد والدراسة الكاملة لهدف الإغارة",
                    "الأعمال الجريئة الحاسمة والتصميم",
                    "كل ما سبق", "لا شيء مما سبق"], "correct": 2},
    ],
}


# ============================================
# 4) الغلاف الاحترافي
# ============================================
class CoverPage(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()

        # خلفية داكنة
        c.setFillColor(colors.HexColor('#1A252F'))
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)

        # إطار ذهبي خارجي
        c.setStrokeColor(colors.HexColor('#D4AF37'))
        c.setLineWidth(3)
        c.rect(8*mm, 8*mm, self.width - 16*mm, self.height - 16*mm,
               fill=0, stroke=1)

        # إطار ذهبي داخلي
        c.setLineWidth(0.8)
        c.rect(12*mm, 12*mm, self.width - 24*mm, self.height - 24*mm,
               fill=0, stroke=1)

        # العنوان الرئيسي
        c.setFillColor(colors.HexColor('#D4AF37'))
        c.setFont('Amiri-Bold', 36)
        c.drawCentredString(self.width / 2, self.height - 70*mm,
                            ar("أسئلة اختيار من متعدد"))

        # خط ذهبي
        c.setStrokeColor(colors.HexColor('#D4AF37'))
        c.setLineWidth(2)
        c.line(self.width / 2 - 40*mm, self.height - 85*mm,
               self.width / 2 + 40*mm, self.height - 85*mm)

        # العنوان الفرعي
        c.setFillColor(colors.HexColor('#ECF0F1'))
        c.setFont('Amiri', 20)
        c.drawCentredString(self.width / 2, self.height - 100*mm,
                            ar("من الكتاب العسكري"))

        # الجزء الأول
        c.setFillColor(colors.HexColor('#D4AF37'))
        c.setFont('Amiri-Bold', 22)
        c.drawCentredString(self.width / 2, 40*mm,
                            ar("الجزء الأول"))

        c.restoreState()


# ============================================
# 5) Header & Footer
# ============================================
PAGE_W, PAGE_H = A4


def draw_header_footer(canvas_obj, doc, section_name="", section_color=DEFAULT_COLOR):
    canvas_obj.saveState()

    # Header
    canvas_obj.setFillColor(colors.HexColor(section_color))
    canvas_obj.rect(0, PAGE_H - 15 * mm, PAGE_W, 10 * mm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.setFont('Amiri-Bold', 11)
    canvas_obj.drawCentredString(PAGE_W / 2, PAGE_H - 12 * mm,
                                 ar("أسئلة اختيار من متعدد - كتاب عسكري"))

    # Footer
    canvas_obj.setFillColor(colors.HexColor('#ECF0F1'))
    canvas_obj.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor('#2C3E50'))
    canvas_obj.setFont('Amiri', 10)
    if section_name:
        canvas_obj.drawRightString(PAGE_W - 15 * mm, 4 * mm, ar(section_name))
    canvas_obj.drawString(15 * mm, 4 * mm, f"Page {doc.page}")

    canvas_obj.setStrokeColor(colors.HexColor(section_color))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(15 * mm, 12 * mm, PAGE_W - 15 * mm, 12 * mm)

    canvas_obj.restoreState()


# ============================================
# 6) Styles
# ============================================
styles = getSampleStyleSheet()

title_toc = ParagraphStyle('ToC', parent=styles['Title'],
    fontName='Amiri-Bold', fontSize=28, alignment=1,
    textColor=colors.HexColor('#2C3E50'), leading=40)

section_style = ParagraphStyle('Sec', parent=styles['Heading1'],
    fontName='Amiri-Bold', fontSize=18, alignment=1,
    textColor=colors.white, leading=24)

q_num_style = ParagraphStyle('QN', parent=styles['Normal'],
    fontName='Amiri-Bold', fontSize=14, alignment=1,
    textColor=colors.white, leading=18)

q_style = ParagraphStyle('Q', parent=styles['Normal'],
    fontName='Amiri-Bold', fontSize=13, alignment=2,
    textColor=colors.HexColor('#2C3E50'), leading=20)

a_style = ParagraphStyle('A', parent=styles['Normal'],
    fontName='Amiri', fontSize=11.5, alignment=2,
    leading=18, rightIndent=10)


# ============================================
# 7) بناء العناصر
# ============================================
def build_section_header(section_name):
    color = SECTION_COLORS.get(section_name, DEFAULT_COLOR)
    table = Table(
        [[Paragraph(ar(section_name), section_style)]],
        colWidths=[PAGE_W - 30 * mm]
    )
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(color)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    return table


def build_question(q_data, num, section_color):
    letters = ["أ", "ب", "ج", "د"]
    correct = q_data["correct"]

    q_num_paragraph = Paragraph(ar(f"س{num}"), q_num_style)
    q_text_paragraph = Paragraph(ar(q_data["q"]), q_style)

    header_table = Table(
        [[q_text_paragraph, q_num_paragraph]],
        colWidths=[PAGE_W - 50 * mm, 15 * mm]
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#F8F9F9')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor(section_color)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    opt_rows = []
    for i, opt in enumerate(q_data["options"]):
        if i == correct:
            mark = "✅"
            text_color = '#186A3B'
        else:
            mark = "⬜"
            text_color = '#2C3E50'

        opt_style = ParagraphStyle(
            f'opt{i}', parent=styles['Normal'],
            fontName='Amiri', fontSize=11.5, alignment=2,
            textColor=colors.HexColor(text_color), leading=16
        )
        opt_paragraph = Paragraph(ar(f"{mark} {letters[i]}) {opt}"), opt_style)
        opt_rows.append([opt_paragraph])

    options_table = Table(opt_rows, colWidths=[PAGE_W - 50 * mm])
    option_styles = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, colors.HexColor('#ECF0F1')),
        ('BACKGROUND', (0, correct), (0, correct), colors.HexColor('#D5F5E3')),
    ]
    options_table.setStyle(TableStyle(option_styles))

    combined = Table(
        [[header_table], [options_table]],
        colWidths=[PAGE_W - 40 * mm]
    )
    combined.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(section_color)),
        ('LINEABOVE', (0, 1), (0, 1), 1, colors.HexColor(section_color)),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    return combined


# ============================================
# 8) بناء المستند
# ============================================
def build_pdf():
    doc = BaseDocTemplate(
        "MCQ_Military_Book.pdf",
        pagesize=A4,
        rightMargin=15 * mm, leftMargin=15 * mm,
        topMargin=20 * mm, bottomMargin=15 * mm,
        title="أسئلة اختيار من متعدد - كتاب عسكري",
        author="MCQ Generator"
    )

    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id='normal'
    )

    def on_page(canvas_obj, doc_obj):
        draw_header_footer(canvas_obj, doc_obj, "", DEFAULT_COLOR)

    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=on_page)])

    elements = []

    # الغلاف
    elements.append(CoverPage(PAGE_W - 30 * mm, PAGE_H - 40 * mm))
    elements.append(PageBreak())

    # الفهرس
    elements.append(Paragraph(ar("الفهرس"), title_toc))
    elements.append(Spacer(1, 1 * cm))

    toc_data = []
    for section_name, qs in SECTIONS.items():
        color = SECTION_COLORS.get(section_name, DEFAULT_COLOR)
        toc_data.append([
            Paragraph(ar(f"{len(qs)} سؤال"), a_style),
            Paragraph(ar(section_name),
                      ParagraphStyle('tocsec', parent=q_style,
                                     textColor=colors.HexColor(color))),
        ])

    toc_table = Table(toc_data, colWidths=[3 * cm, PAGE_W - 40 * mm])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, colors.HexColor('#BDC3C7')),
    ]))
    elements.append(toc_table)
    elements.append(PageBreak())

    # الفصول
    total_q = 0
    for section_name, questions in SECTIONS.items():
        section_color = SECTION_COLORS.get(section_name, DEFAULT_COLOR)

        elements.append(build_section_header(section_name))
        elements.append(Spacer(1, 0.5 * cm))

        for i, q in enumerate(questions, 1):
            elements.append(KeepTogether([
                build_question(q, i, section_color),
                Spacer(1, 0.4 * cm),
            ]))
            total_q += 1

        elements.append(PageBreak())

    doc.build(elements)
    print(f"✅ تم إنشاء الملف: MCQ_Military_Book.pdf")
    print(f"📊 عدد الفصول: {len(SECTIONS)}")
    print(f"📊 عدد الأسئلة: {total_q}")


if __name__ == "__main__":
    build_pdf()
