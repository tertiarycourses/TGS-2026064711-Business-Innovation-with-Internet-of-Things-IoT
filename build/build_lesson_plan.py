#!/usr/bin/env python3
"""Generate the IoT with Raspberry Pi (TGS-2020505433) Lesson Plan (LP) DOCX
in the Tertiary house format.

Cover page + Document Version Control Record + auto TOC + Arial 11pt body +
colour-coded schedule table + page numbers.

TWO training days of 8 hours each (9:30am-6:30pm with a 1-hour lunch). The
component split is fixed by the approved Course Proposal (CA-WSQ-2020-010764):
    Classroom Facilitation   540 min  (9.0 h, tea breaks counted within)
    Practical / Practicum    300 min  (5.0 h — Topic 2/3/4 IoTFlow labs)
    Assessment               120 min  (2.0 h — WA 60 min + PP 60 min, per the approved Assessment Plan)
    ----------------------------------
    Total training           960 min  (16.0 h, excluding the 1-hour lunch each day)

The build asserts this split, so the LP can never silently drift out of
alignment with the accredited proposal.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5
import prodoc
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
HEADER_FILL="1F6FEB"; TOPIC_FILL="E8F0FE"; BREAK_FILL="FFF4E5"; LUNCH_FILL="FDE9D9"
ASSESS_FILL="E8F7EE"; LAB_FILL="E6FAF3"

LAB_LIST="; ".join(f"Lab {a['num']}: {a['title']}" for a in ACT)

# ------------------------------------------------ schedule (single source of truth for timing)
# (start, end, minutes, kind, activity_text)   kind: admin/topic/lab/break/lunch/assess
def _labs_for(*topics):
    """Lab list for the given topic numbers, used inside the schedule text."""
    return "; ".join(f"Lab {a['num']}: {a['title']}" for a in ACT if a["topic"] in topics)

# ---- Day 1: 9:30am–6:30pm, 8 training hours (1-hour lunch excluded) --------
SCHEDULE_D1 = [
    ("9:30am","9:45am",15,"admin","Welcome, trainer and learner introductions, ground rules, and mandatory digital attendance (AM)"),
    ("9:45am","10:00am",15,"admin",f"Learning outcomes, course outline and Skills Framework (TSC {C.TSC_CODE}) briefing"),
    ("10:00am","10:45am",45,"topic","Topic 1 — Overview of Internet of Things (IoT), part 1: the 4th Industrial Revolution, what IoT is, the four building blocks of an IoT system, and how IoT works.  (LO1 / A1, K1)"),
    ("10:45am","11:00am",15,"break","Tea break"),
    ("11:00am","11:55am",55,"topic","Topic 1 — Overview of Internet of Things (IoT), part 2: sensors and actuators, wireless technologies for IoT, types of IoT and IIoT, and IoT use cases across industry.  (LO1 / A1, K1)"),
    ("11:55am","12:30pm",35,"topic","Topic 1 — Facilitated discussion 'Analyse an IoT Use Case' and topic recap.  (LO1 / A1, K1)"),
    ("12:30pm","1:30pm",60,"lunch","Lunch break"),
    ("1:30pm","1:40pm",10,"admin","Mandatory digital attendance (PM)"),
    ("1:40pm","2:35pm",55,"topic","Topic 2 — Collect and Post Environmental Data to Cloud (concepts): cloud computing for IoT, the IoTFlow platform, the Raspberry Pi as an IoT gateway, environmental sensors, device tokens, and the HTTP REST and MQTT uplink.  (LO2 / A2, K2, K3)"),
    ("2:35pm","3:20pm",45,"lab","Topic 2 — HANDS-ON PRACTICAL on IoTFlow (https://iot.tertiaryinfotech.com). "+_labs_for(2).split(";")[0].strip()),
    ("3:20pm","3:35pm",15,"break","Tea break"),
    ("3:35pm","5:35pm",120,"lab","Topic 2 — HANDS-ON PRACTICAL (continued). "+_labs_for(2).split(";")[1].strip()),
    ("5:35pm","6:10pm",35,"topic","Topic 2 — Reviewing the uplink: verifying telemetry arrival, troubleshooting connectivity, running the sensor script unattended, and topic recap.  (LO2 / A2, K2, K3)"),
    ("6:10pm","6:30pm",20,"admin","Day 1 recap, Q&A, and preview of Day 2"),
]

# ---- Day 2: 9:30am–6:30pm, 8 training hours (1-hour lunch excluded) --------
SCHEDULE_D2 = [
    ("9:30am","9:40am",10,"admin","Mandatory digital attendance (AM) and Day 1 recap"),
    ("9:40am","10:35am",55,"topic","Topic 3 — IoT Data Analytics and Visualization (concepts): why visualise, display widgets, analysing telemetry history for trends and drift, alert rules, and recording performance.  (LO3 / A3, K4, K5)"),
    ("10:35am","10:50am",15,"break","Tea break"),
    ("10:50am","12:05pm",75,"lab","Topic 3 — HANDS-ON PRACTICAL on IoTFlow. "+_labs_for(3)),
    ("12:05pm","12:30pm",25,"topic","Topic 3 — Facilitated discussion 'Design Your Monitoring Dashboard' and topic recap.  (LO3 / A3, K4, K5)"),
    ("12:30pm","1:30pm",60,"lunch","Lunch break"),
    ("1:30pm","1:40pm",10,"admin","Mandatory digital attendance (PM)"),
    ("1:40pm","2:35pm",55,"topic","Topic 4 — Monitor Data to Trigger Control from Cloud (concepts): reading data back over REST and MQTT, downlink control and virtual pins, automation with n8n, monitoring effectiveness, and IoT security.  (LO4 / A4, K6, K7)"),
    ("2:35pm","3:35pm",60,"lab","Topic 4 — HANDS-ON PRACTICAL on IoTFlow. "+_labs_for(4)),
    ("3:35pm","3:50pm",15,"break","Tea break"),
    ("3:50pm","4:15pm",25,"topic","Topic 4 — Facilitated discussion 'Monitor Effectiveness and Manage Risk', IoT guidelines and communication standards, and topic recap.  (LO4 / A4, K6, K7)"),
    ("4:15pm","4:30pm",15,"admin","Course summary and Q&A, TRAQOM survey, Assessment digital attendance, and Briefing for Assessment"),
    ("4:30pm","5:30pm",60,"assess","Written Assessment (WA) — Short-Answer Questions (Q&A), 60 minutes, open book. Assesses knowledge K1–K7."),
    ("5:30pm","6:30pm",60,"assess","Practical Performance (PP) — 60 minutes, open book, individually completed. Assesses abilities A1–A4."),
]

SCHEDULES = {1: SCHEDULE_D1, 2: SCHEDULE_D2}
SCHEDULE = SCHEDULE_D1 + SCHEDULE_D2

# Component split, computed from the schedules above so the Course Information
# table can never contradict the per-day totals printed under each schedule.
def _split():
    cls=lab=ass=0
    for day in SCHEDULES.values():
        for _s,_e,mins,kind,_t in day:
            if kind in ("topic","admin","break"): cls+=mins
            elif kind=="lab": lab+=mins
            elif kind=="assess": ass+=mins
    return cls,lab,ass
_CLS,_LAB,_ASS = _split()
COMPONENTS_TEXT = (f"Classroom Facilitation {_CLS/60:.1f} h · "
                   f"Practical / Practicum {_LAB/60:.1f} h · "
                   f"Assessment {_ASS/60:.1f} h")

# Which topics carry a facilitated discussion — read from the single source of
# truth so this can never name a topic the course no longer has.
_dt = sorted(d["topic"] for d in C.DISCUSSIONS)
DISC_TOPICS = ("Topics " + ", ".join(str(x) for x in _dt[:-1]) + f" and {_dt[-1]}") if len(_dt) > 1 else f"Topic {_dt[0]}"

# ------------------------------------------------ build document
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)

prodoc.add_cover_page(doc,"LESSON PLAN",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=None, course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("14.0","20 February 2023","Previous release — 'Mastering Raspberry Pi: Hands-On Practical Applications for Beginners', "
  "2-day structure with ThingSpeak, MATLAB, Node-RED, Adafruit IO and IFTTT practical activities.",C.TRAINER),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Major revision. Course retitled from 'Mastering Raspberry Pi: Hands-On Practical Applications "
  "for Beginners' to 'IoT with Raspberry Pi'. All practical activities replaced with four hands-on "
  "labs on the IoTFlow platform (https://iot.tertiaryinfotech.com); the legacy ThingSpeak, MATLAB, "
  "Node-RED, Adafruit IO and IFTTT lab set retired. Deck rebuilt to the current house visual "
  "standard. Assessment stated as WA (Q&A) 60 min plus Practical Performance 60 min.",C.TRAINER),
])
prodoc.add_toc(doc)

def H(text,level=1):
    return doc.add_heading(text,level=level)

H("Course Information",1)
info=[("Course Title",C.TITLE),("WSQ Course Reference",C.COURSE_CODE),
      ("Training Provider",C.ORG+"  ("+C.UEN.replace('UEN: ','UEN ')+")"),
      ("TSC Title / Code",f"{C.TSC_TITLE}  ·  {C.TSC_CODE}  (Level 4)"),
      ("Duration",f"{C.DAYS} days · 16 training hours (excluding a 1-hour lunch break each day)"),
      ("Daily Timing","9:30 am – 6:30 pm (1-hour lunch; tea breaks counted within training time)"),
      ("Course Components",COMPONENTS_TEXT),
      ("Mode","Instructor-led classroom facilitation with hands-on IoT labs on the IoTFlow cloud platform"),
      ("Platform",f"{C.PLATFORM} — {C.PLATFORM_URL}"),
      ("Trainer",C.TRAINER)]
t=doc.add_table(rows=0,cols=2); t.style="Table Grid"
for k,v in info:
    c=t.add_row().cells; c[0].text=""; r=c[0].paragraphs[0].add_run(k); r.bold=True; r.font.size=Pt(10)
    prodoc._shade_cell(c[0],TOPIC_FILL)
    c[1].text=""; c[1].paragraphs[0].add_run(v).font.size=Pt(10)

H("Learning Outcomes",1)
doc.add_paragraph("On completion of this course, learners will be able to:")
for lo in C.LEARNING_OUTCOMES:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(lo).font.size=Pt(10.5)

H(f"Skills Framework Mapping (TSC {C.TSC_CODE} {C.TSC_TITLE})",1)
doc.add_paragraph(C.TSC_DESC)
tm=doc.add_table(rows=0,cols=2); tm.style="Table Grid"
hdr=tm.add_row().cells
for i,htext in enumerate(["Abilities (assessed by the Practical Performance)","Knowledge (assessed by the Written Assessment)"]):
    cell=hdr[i]; cell.text=""
    r=cell.paragraphs[0].add_run(htext); r.bold=True; r.font.size=Pt(10)
    r.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); prodoc._shade_cell(cell,HEADER_FILL)
for i in range(max(len(C.ABILITIES),len(C.KNOWLEDGE))):
    cells=tm.add_row().cells
    for j,src in enumerate((C.ABILITIES,C.KNOWLEDGE)):
        cells[j].text=""
        if i<len(src):
            code,txt=src[i]
            p=cells[j].paragraphs[0]
            rb=p.add_run(code+" — "); rb.bold=True; rb.font.size=Pt(9.5)
            p.add_run(txt).font.size=Pt(9.5)

H("Assessment",1)
for a in [C.ASSESSMENT["written"],C.ASSESSMENT["practical"],
          "Format: Open Book — course slides, Learner Guide and approved materials only.",
          "The assessment is conducted at the end of Day 2, from 5:10 pm.",
          "Assessor-to-learner ratio: 1:3 to 1:10 for both the WA (Q&A) and the Practical Performance.",
          C.ASSESSMENT["note"]]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(a).font.size=Pt(10.5)

def set_cell(cell,text,bold=False,size=9.5,color=None,fill=None,align=None):
    cell.text=""; p=cell.paragraphs[0]
    if align: p.alignment=align
    r=p.add_run(text); r.bold=bold; r.font.size=Pt(size); r.font.name="Arial"
    if color: r.font.color.rgb=color
    if fill: prodoc._shade_cell(cell,fill)

KIND_FILL={"topic":TOPIC_FILL,"break":BREAK_FILL,"lunch":LUNCH_FILL,"assess":ASSESS_FILL,
           "admin":"F3F5F8","lab":LAB_FILL}

H("Course Schedule",1)
totals={"training":0,"classroom":0,"practical":0,"assessment":0}
for day in sorted(SCHEDULES):
    H(f"Day {day} — {C.DAY_THEMES[day]}",2)
    tbl=doc.add_table(rows=0,cols=3); tbl.style="Table Grid"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    hdr=tbl.add_row().cells
    for i,htext in enumerate(["Time","Duration","Topic / Activity"]):
        set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
    training=classroom=practical=assessment=0
    for start,end,mins,kind,text in SCHEDULES[day]:
        cells=tbl.add_row().cells; fill=KIND_FILL.get(kind)
        set_cell(cells[0],f"{start}–{end}",bold=(kind in ("topic","assess","lab")),size=9.5,fill=fill)
        set_cell(cells[1],f"{mins} min",size=9.5,fill=fill)
        set_cell(cells[2],text,bold=(kind in ("topic","assess","lab")),size=9.5,fill=fill)
        if kind!="lunch": training+=mins
        if kind in ("topic","admin","break"): classroom+=mins
        elif kind=="lab": practical+=mins
        elif kind=="assess": assessment+=mins
    for row in tbl.rows:
        row.cells[0].width=Inches(1.15); row.cells[1].width=Inches(0.9); row.cells[2].width=Inches(4.75)
    p=doc.add_paragraph()
    r=p.add_run(f"Day {day} training time: {training} minutes ({training/60:.0f} hours), excluding the 1-hour lunch break. "
                f"Classroom Facilitation {classroom} min · Practical/Practicum {practical} min"
                +(f" · Assessment {assessment} min." if assessment else "."))
    r.italic=True; r.font.size=Pt(9.5); r.font.color.rgb=GREY
    totals["training"]+=training; totals["classroom"]+=classroom
    totals["practical"]+=practical; totals["assessment"]+=assessment

p=doc.add_paragraph()
r=p.add_run(f"Course total: {totals['training']} minutes ({totals['training']/60:.0f} hours) across {C.DAYS} training days, "
            f"excluding lunch breaks. Classroom Facilitation {totals['classroom']} min ({totals['classroom']/60:.1f} h) · "
            f"Practical/Practicum {totals['practical']} min ({totals['practical']/60:.1f} h) · "
            f"Assessment {totals['assessment']} min ({totals['assessment']/60:.1f} h).")
r.bold=True; r.font.size=Pt(9.5); r.font.color.rgb=GREY

# Guard: the LP can never drift from the accredited structure.
# 2 training days of 8 h = 960 min, of which 120 min is the final assessment.
assert totals["training"]==960,   f"Training minutes = {totals['training']}, expected 960"
assert totals["assessment"]==120, f"Assessment minutes = {totals['assessment']}, expected 120"
assert totals["practical"]==300,  f"Practical minutes = {totals['practical']}, expected 300"
assert totals["classroom"]+totals["practical"]+totals["assessment"]==totals["training"], "Component split does not sum"

H("Topic and Activity Reference",1)
tt=doc.add_table(rows=0,cols=3); tt.style="Table Grid"
hdr=tt.add_row().cells
for i,htext in enumerate(["Topic / Learning Unit","Outcome & TSC mapping","In-class activity"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
DISC_BY_TOPIC={d["topic"]:d for d in C.DISCUSSIONS}
for tp in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==tp["num"]]
    cells=tt.add_row().cells
    set_cell(cells[0],f"Topic {tp['code']}: {tp['title']}",bold=True,size=9.5,fill=TOPIC_FILL)
    set_cell(cells[1],tp["weighting"],size=9.5,fill=TOPIC_FILL)
    if acts:
        act=", ".join(f"Lab {a['num']}: {a['title']}" for a in acts)
    else:
        d=DISC_BY_TOPIC.get(tp["num"])
        act=f"{d['title']} ({d['mins']} min facilitated discussion)" if d else "Lecture and didactic questioning"
    set_cell(cells[2],act,size=9.5)

H("Hands-On Labs (Topics 2–4 — Practical / Practicum, 300 minutes)",1)
doc.add_paragraph(
    f"All labs run on {C.PLATFORM} ({C.PLATFORM_URL}). Full step-by-step instructions are in the "
    f"Learner Guide; the slide deck presents each lab's purpose and outcome only.")
tl=doc.add_table(rows=0,cols=3); tl.style="Table Grid"
hdr=tl.add_row().cells
for i,htext in enumerate(["Lab","Title","What the learner builds"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
for a in ACT:
    cells=tl.add_row().cells
    set_cell(cells[0],f"Lab {a['num']}",bold=True,size=9.5,fill=LAB_FILL)
    set_cell(cells[1],a["title"],size=9.5)
    set_cell(cells[2],a["build"],size=9.5)
for row in tl.rows:
    row.cells[0].width=Inches(0.7); row.cells[1].width=Inches(2.5); row.cells[2].width=Inches(3.6)

H("Instructional Methods",1)
for m in ["Lecture — trainer-led explanation of concepts with visual slides.",
          "Didactic questioning — the trainer poses questions to check and deepen understanding.",
          f"Facilitated discussion — learners apply each topic to their own organisation ({DISC_TOPICS}).",
          "Demonstration — the trainer demonstrates each IoTFlow workflow before the learners attempt it.",
          "Hands-on practical — learners complete Labs 1–4 on their own IoTFlow project (Topics 2–4)."]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(m).font.size=Pt(10.5)

H("Resources Required",1)
for m in ["Classroom with projector or large screen, whiteboard and high-speed WiFi.",
          "One laptop per learner with a modern web browser (spare laptops are available).",
          f"A free learner account on {C.PLATFORM} ({C.PLATFORM_URL}).",
          "Python 3 with the IoTFlow client (pip install \"iotflow[mqtt]\") for the optional scripted labs.",
          "IoT hardware (ESP32/ESP8266) is optional — every lab can be completed from the browser and terminal.",
          "Course slides, Learner Guide and Lesson Plan available on https://lms-tms.tertiaryinfotech.com."]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(m).font.size=Pt(10.5)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
OUT=os.path.join(REPO,"courseware",f"LP-{C.SHORT_TITLE}.docx")
doc.save(OUT)
print("Saved",OUT)
print(f"  training={totals['training']} classroom={totals['classroom']} "
      f"practical={totals['practical']} assessment={totals['assessment']}  ({C.DAYS} days)")
