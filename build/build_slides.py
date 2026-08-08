#!/usr/bin/env python3
"""Generate the IoT with Raspberry Pi (TGS-2020505433) slide deck
(all-white Tertiary house style).

Design helpers are the same set used by the tertiary-course-slides skill that
produced the n8n reference deck (cover, section, content, two_col, cards3,
big_statement, tile_grid, flow_h, trainer_slide, brk). Content is driven
entirely by course_data.py + data_domainN.py so the deck stays 100% aligned
with the LP, LG and labs.

DECK POLICY FOR THIS COURSE
  * NO step-by-step slides. The deck shows each lab's purpose, what the learner
    builds and why it matters to the business; the numbered commands live ONLY
    in the Learner Guide and labs/*.md. (step_slide is intentionally unused.)
  * High visual density: tile grids, flow diagrams, cards and stat bands
    instead of bullet walls.
"""
import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
ACTIVITIES = DOMAIN1 + DOMAIN2 + DOMAIN3 + DOMAIN4 + DOMAIN5

def _find_repo(start):
    """Locate the course repo (a dir containing both courseware/ and labs/).
    Env COURSE_REPO overrides. Keeps the build working wherever the skill lives."""
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env):
        return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(HERE))
REPO = _find_repo(HERE)
ASSETS = os.path.join(os.path.dirname(HERE), "assets")   # co-located with the skill
# Course diagrams & screenshots. Depending on how the repo is laid out the
# assets folder sits either beside this build/ dir or under courseware/, so
# take the first candidate that actually exists rather than assuming one.
IMG = next((p for p in (os.path.join(os.path.dirname(HERE), "assets"),
                        os.path.join(REPO, "courseware", "assets"),
                        os.path.join(REPO, "assets"))
            if os.path.isdir(p)),
           os.path.join(REPO, "courseware", "assets"))

# ---------------- palette (matches reference) ----------------
BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81); AMBER=RGBColor(0xF5,0x9E,0x0B)
INK=RGBColor(0x16,0x1B,0x26); GREY=RGBColor(0x5B,0x63,0x72); LIGHT=RGBColor(0xF5,0xF8,0xFC)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0); VIOLET=RGBColor(0x7C,0x3A,0xED)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(1,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
    sp.shadow.inherit=False; return sp
def oval(s,x,y,w,h,color):
    sp=s.shapes.add_shape(9,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    for i,line in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space)
        for t,sz,col,bold in line:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
            r.font.color.rgb=col; r.font.name="Arial"
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
        lvl=it[1] if isinstance(it,tuple) else 0
        text=it[0] if isinstance(it,tuple) else it
        r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
        r.font.size=Pt(size if lvl==0 else size-2); r.font.color.rgb=color if lvl==0 else GREY
        r.font.name="Arial"; r.font.bold=(lvl==0 and isinstance(it,tuple) and len(it)>2 and it[2])
    return tb

PAGE={"n":1}   # slide 1 is the cover (no footer); slide 2 prints "2"
def footer(s):
    PAGE["n"]+=1
    txt(s,Inches(0.4),Inches(7.05),Inches(7.5),Inches(0.35),
        [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",9,GREY,False)]])
    txt(s,Inches(5.0),Inches(7.05),Inches(3.3),Inches(0.35),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd",9,GREY,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(12.4),Inches(7.05),Inches(0.6),Inches(0.35),
        [[(str(PAGE["n"]),9,GREY,False)]],align=PP_ALIGN.RIGHT)
def head(s,title,kicker=None,kcolor=BLUE):
    rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),Inches(1.55),kcolor)
    if kicker: txt(s,Inches(0.85),Inches(0.5),Inches(11.6),Inches(0.4),[[(kicker,14,kcolor,True)]])
    # Auto-shrink long titles so they never wrap past the header rule into the
    # slide body. ~52 chars fits on one line at 29pt across the 11.9in box.
    n=len(title)
    size=29 if n<=52 else (25 if n<=68 else (22 if n<=84 else 20))
    txt(s,Inches(0.85),Inches(0.9),Inches(11.9),Inches(0.9),[[(title,size,INK,True)]],
        anchor=MSO_ANCHOR.MIDDLE)
    rect(s,Inches(0.85),Inches(1.7),Inches(11.63),Inches(0.02),LINE)
    return s
def _logo(name):
    p=os.path.join(ASSETS,name)
    return p if os.path.exists(p) else None

# ---------------- slide templates ----------------
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE); rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    org=_logo("tertiary-infotech-logo.png")
    if org: s.shapes.add_picture(org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    # course badge (top-right) — IoTFlow platform badge, else a drawn IoT node mark
    badge=_logo("iotflow-logo.png")
    if badge:
        s.shapes.add_picture(badge,Inches(10.05),Inches(0.6),width=Inches(2.5))
    else:
        bx,by=Inches(10.75),Inches(0.62)
        rect(s,bx,by,Inches(1.85),Inches(1.2),BLUE)
        # drawn IoT mark: a hub with four connected nodes
        cx,cy=int(bx+Inches(0.925)),int(by+Inches(0.44))
        d=Inches(0.2)
        for dx,dy in ((-Inches(0.5),-Inches(0.24)),(Inches(0.5),-Inches(0.24)),
                      (-Inches(0.5),Inches(0.24)),(Inches(0.5),Inches(0.24))):
            rect(s,int(cx+(dx*0.55)),int(cy+(dy*0.55)),Inches(0.5),Inches(0.03),
                 RGBColor(0x8F,0xC2,0xFF))
            oval(s,int(cx+dx-d/2),int(cy+dy-d/2),d,d,RGBColor(0x8F,0xC2,0xFF))
        oval(s,int(cx-Inches(0.16)),int(cy-Inches(0.16)),Inches(0.32),Inches(0.32),WHITE)
        txt(s,bx,by+Inches(0.78),Inches(1.85),Inches(0.4),
            [[("IoT · IoTFlow",10,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.85),Inches(12.0),Inches(1.9),[[(C.TITLE,40,INK,True)]])
    rect(s,Inches(0.92),Inches(4.75),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(5.05),Inches(12),Inches(1.4),
        [[(f"WSQ Course Code: {C.COURSE_CODE}",16,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)]],space=6)
    txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),[[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,GREY,False)]])
    txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),[[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

def section(kicker,title,n,sub=""):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,BLUE)
    rect(s,Inches(0.85),Inches(2.5),Inches(0.14),Inches(2.0),TEAL)
    txt(s,Inches(1.25),Inches(2.55),Inches(11),Inches(0.6),[[(kicker,18,BLUE,True)]])
    txt(s,Inches(1.25),Inches(3.0),Inches(11.4),Inches(1.6),[[(title,40,INK,True)]])
    if sub: txt(s,Inches(1.27),Inches(4.55),Inches(11),Inches(0.8),[[(sub,16,GREY,False)]])
    txt(s,Inches(10.0),Inches(0.7),Inches(2.8),Inches(1.6),[[(n,72,RGBColor(0xE2,0xE8,0xF0),True)]],align=PP_ALIGN.RIGHT)
    footer(s)
def content(title,items,kicker=None,size=20):
    s=head(slide(),title,kicker); bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def two_col(title,left,right,kicker=None,lhead="",rhead=""):
    s=head(slide(),title,kicker)
    rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(4.7),LIGHT); rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(4.7),LIGHT)
    if lhead: txt(s,Inches(1.1),Inches(2.15),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
    if rhead: txt(s,Inches(7.2),Inches(2.15),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
    bullets(s,Inches(1.1),Inches(2.7),Inches(5.2),Inches(3.8),left,size=16)
    bullets(s,Inches(7.2),Inches(2.7),Inches(5.05),Inches(3.8),right,size=16,mcolor=TEAL); footer(s); return s
def cards3(title,cards,kicker):
    s=head(slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
    for i,c in enumerate(cards[:3]):
        x=xs[i]; col=c[0]
        rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT); rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
        txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.6),[[(c[1],19,col,True)]])
        bullets(s,x+Inches(0.25),Inches(2.95),Inches(3.2),Inches(3.4),c[2],size=14,mcolor=col,gap=9)
    footer(s); return s
def big_statement(line1,line2,kicker,color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,color)
    txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[(kicker,16,color,True)]])
    txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(2.4),[[(line1,38,INK,True)]])
    if line2: txt(s,Inches(1.12),Inches(4.9),Inches(11),Inches(1.2),[[(line2,20,GREY,False)]])
    footer(s); return s
import math
PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
    """Grid of light panels, each with a coloured icon/number badge + text.
    items: list of strings (or (title,caption) tuples). Much richer than a bullet list."""
    s=head(slide(),title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    bd=Inches(0.6)
    for i,it in enumerate(items):
        r=i//cols; c=i%cols
        x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,Inches(0.1),ch,col)
        oval(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,col)
        ic=icons[i] if icons else str(i+1)
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        if isinstance(it,tuple):
            txt(s,tx,int(y+Inches(0.14)),tw,int(ch-Inches(0.2)),
                [[(it[0],size+2,INK,True)],[(it[1],size-2,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
        else:
            txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def flow_h(title,steps,kicker=None,color=BLUE):
    """Horizontal numbered flow: coloured chips connected by chevrons."""
    s=head(slide(),title,kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),[[(st,14,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.04)),int(y+ch/2-Inches(0.3)),int(gap+Inches(0.08)),Inches(0.6),
                [[("▶",15,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    """Profile-card layout: avatar badge + name/role panel on the left, labelled
    info tiles on the right. rows: list of (LABEL, value); blank value → fill-in line."""
    s=head(slide(),"About the Trainer",kicker,kcolor=accent)
    lx=Inches(0.85); lw=Inches(3.65)
    rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
    bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
    oval(s,ax,Inches(2.5),bd,bd,accent)
    txt(s,ax,Inches(2.5),bd,bd,[[(initials,44,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,lx+Inches(0.15),Inches(4.55),lw-Inches(0.3),Inches(0.6),[[(name,21,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,lx+Inches(0.15),Inches(5.2),lw-Inches(0.3),Inches(1.2),[[(role,13,GREY,False)]],align=PP_ALIGN.CENTER)
    rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
    n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
    for i,(label,val) in enumerate(rows):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.1),th,col)
        vruns=[(val,14,INK,False)] if val else [("____________________________________________",13,LINE,False)]
        txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,
            [[(label.upper(),11,col,True)],vruns],anchor=MSO_ANCHOR.MIDDLE,space=3)
    footer(s); return s
def activity_overview(tag,title,desc,build,services,kicker):
    s=head(slide(),title,kicker,kcolor=TEAL)
    rect(s,Inches(0.85),Inches(1.85),Inches(1.7),Inches(0.5),TEAL)
    txt(s,Inches(0.85),Inches(1.9),Inches(1.7),Inches(0.4),[[(tag,16,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.85),Inches(2.55),Inches(11.7),Inches(1.6),[[(desc,21,INK,False)]])
    rect(s,Inches(0.85),Inches(4.3),Inches(11.7),Inches(2.0),LIGHT)
    txt(s,Inches(1.1),Inches(4.5),Inches(11),Inches(0.4),[[("You'll build",14,BLUE,True)]])
    txt(s,Inches(1.1),Inches(4.9),Inches(11),Inches(0.6),[[(build,18,INK,True)]])
    txt(s,Inches(1.1),Inches(5.6),Inches(11.2),Inches(0.6),[[("Tools:  ",13,GREY,True),(services,13,GREY,False)]]); footer(s); return s
def step_slide(kicker,act_title,n,total,text,cmd=""):
    s=head(slide(),act_title,kicker,TEAL)
    oval(s,Inches(0.85),Inches(2.5),Inches(1.4),Inches(1.4),TEAL)
    txt(s,Inches(0.85),Inches(2.74),Inches(1.4),Inches(0.9),[[(str(n),38,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.95),Inches(1.95),Inches(11),Inches(0.4),[[(f"STEP {n} OF {total}",13,GREY,True)]])
    txt(s,Inches(2.55),Inches(2.4),Inches(10.1),Inches(1.3),[[(text,23,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    if cmd:
        rect(s,Inches(2.55),Inches(4.15),Inches(10.1),Inches(0.95),RGBColor(0x0B,0x12,0x20))
        txt(s,Inches(2.8),Inches(4.28),Inches(9.7),Inches(0.7),[[("$ "+cmd,13,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def test_slide(act_title,text,kicker):
    s=head(slide(),act_title,kicker,TEAL)
    rect(s,Inches(0.85),Inches(2.3),Inches(11.7),Inches(2.6),RGBColor(0xE8,0xF7,0xEE))
    txt(s,Inches(1.2),Inches(2.6),Inches(11),Inches(0.5),[[("✅  Test it",20,RGBColor(0x12,0x7A,0x3E),True)]])
    txt(s,Inches(1.2),Inches(3.3),Inches(11),Inches(1.4),[[(text,18,INK,False)]]); footer(s); return s
def lab_outcome(a,kicker):
    """Visual lab slide — what you build, the tools, and why the business cares.
    Deliberately replaces per-step slides: the commands live only in the LG."""
    s=head(slide(),a["title"],kicker,kcolor=TEAL)
    rect(s,Inches(0.85),Inches(1.85),Inches(1.75),Inches(0.5),TEAL)
    txt(s,Inches(0.85),Inches(1.9),Inches(1.75),Inches(0.4),
        [[(f"LAB {a['num']}",16,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(2.8),Inches(1.87),Inches(9.7),Inches(0.55),
        [[(a["objective"],13,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,Inches(0.85),Inches(2.55),Inches(11.7),Inches(1.25),[[(a["desc"],17,INK,False)]])
    # two outcome panels: what you build  |  why it matters to the business
    py=Inches(3.95); ph=Inches(1.75)
    rect(s,Inches(0.85),py,Inches(5.72),ph,LIGHT); rect(s,Inches(0.85),py,Inches(5.72),Inches(0.1),BLUE)
    txt(s,Inches(1.1),py+Inches(0.22),Inches(5.2),Inches(0.35),[[("YOU'LL BUILD",11,BLUE,True)]])
    txt(s,Inches(1.1),py+Inches(0.6),Inches(5.25),Inches(1.05),[[(a["build"],15,INK,True)]])
    rect(s,Inches(6.8),py,Inches(5.72),ph,LIGHT); rect(s,Inches(6.8),py,Inches(5.72),Inches(0.1),VIOLET)
    txt(s,Inches(7.05),py+Inches(0.22),Inches(5.2),Inches(0.35),[[("WHY THE BUSINESS CARES",11,VIOLET,True)]])
    txt(s,Inches(7.05),py+Inches(0.6),Inches(5.25),Inches(1.05),
        [[(a.get("business",""),13,GREY,False)]])
    # tools strip
    rect(s,Inches(0.85),Inches(5.95),Inches(11.67),Inches(0.62),RGBColor(0xEE,0xF4,0xFF))
    txt(s,Inches(1.1),Inches(5.95),Inches(11.2),Inches(0.62),
        [[("TOOLS   ",10,BLUE,True),(a["services"],12,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s

def discussion_slide(d,kicker):
    """Facilitated-discussion activity slide for the lecture-only topics."""
    s=head(slide(),d["title"],kicker,kcolor=AMBER)
    rect(s,Inches(0.85),Inches(1.85),Inches(2.5),Inches(0.5),AMBER)
    txt(s,Inches(0.85),Inches(1.9),Inches(2.5),Inches(0.4),
        [[(f"DISCUSSION · {d['mins']} MIN",13,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.85),Inches(2.6),Inches(11.7),Inches(0.95),[[(d["brief"],17,INK,False)]])
    n=len(d["prompts"]); X0=Inches(0.85); TOTW=Inches(11.67); gx=Inches(0.28)
    cw=int((TOTW-gx*(n-1))/n); y=Inches(3.75); ch=Inches(1.95); bd=Inches(0.56)
    for i,p in enumerate(d["prompts"]):
        x=int(X0+(cw+gx)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.09),col)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.28)),bd,bd,col)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.28)),bd,bd,
            [[(str(i+1),19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(0.98)),cw-Inches(0.32),int(ch-Inches(1.1)),
            [[(p,11,INK,False)]],align=PP_ALIGN.CENTER)
    rect(s,Inches(0.85),Inches(5.95),Inches(11.67),Inches(0.62),RGBColor(0xE8,0xF7,0xEE))
    txt(s,Inches(1.1),Inches(5.95),Inches(11.2),Inches(0.62),
        [[("YOUR OUTPUT   ",10,RGBColor(0x12,0x7A,0x3E),True),(d["output"],12,INK,False)]],
        anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s

def download_material(kicker="COURSE PORTAL"):
    """Visual 'Download Course Material' slide — a drawn browser mock of the
    LMS/TMS portal plus the numbered download path (not a bare text link)."""
    s=head(slide(),"Download Your Course Material",kicker,kcolor=BLUE)
    # browser chrome mock
    bx,by,bw,bh=Inches(0.85),Inches(1.95),Inches(6.5),Inches(4.55)
    rect(s,bx,by,bw,bh,WHITE,line=LINE)
    rect(s,bx,by,bw,Inches(0.52),RGBColor(0xEE,0xF2,0xF7))
    for i,c in enumerate([RGBColor(0xFF,0x5F,0x57),RGBColor(0xFE,0xBC,0x2E),RGBColor(0x28,0xC8,0x40)]):
        oval(s,bx+Inches(0.2)+Inches(0.28)*i,by+Inches(0.17),Inches(0.17),Inches(0.17),c)
    rect(s,bx+Inches(1.15),by+Inches(0.12),bw-Inches(1.45),Inches(0.29),WHITE,line=LINE)
    txt(s,bx+Inches(1.28),by+Inches(0.12),bw-Inches(1.6),Inches(0.29),
        [[("🔒  lms-tms.tertiaryinfotech.com",10,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
    # portal header + course row
    rect(s,bx,by+Inches(0.52),bw,Inches(0.72),BLUE)
    txt(s,bx+Inches(0.28),by+Inches(0.52),bw-Inches(0.5),Inches(0.72),
        [[("Tertiary Infotech  ·  LMS / TMS",14,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,bx+Inches(0.28),by+Inches(1.42),bw-Inches(0.56),Inches(0.35),
        [[("MY COURSES",10,GREY,True)]])
    rect(s,bx+Inches(0.28),by+Inches(1.78),bw-Inches(0.56),Inches(0.78),LIGHT)
    rect(s,bx+Inches(0.28),by+Inches(1.78),Inches(0.08),Inches(0.78),TEAL)
    txt(s,bx+Inches(0.52),by+Inches(1.78),bw-Inches(1.1),Inches(0.78),
        [[(C.TITLE,11,INK,True)],[(C.COURSE_CODE,9,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=2)
    # download rows
    for i,(label,ext) in enumerate([("Learner Slides","PDF"),("Learner Guide","PDF"),("Lesson Plan","PDF")]):
        ry=by+Inches(2.75)+Inches(0.56)*i
        rect(s,bx+Inches(0.28),ry,bw-Inches(0.56),Inches(0.46),WHITE,line=LINE)
        rect(s,bx+Inches(0.36),ry+Inches(0.07),Inches(0.42),Inches(0.32),BLUE)
        txt(s,bx+Inches(0.36),ry+Inches(0.07),Inches(0.42),Inches(0.32),
            [[(ext,8,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,bx+Inches(0.9),ry,Inches(3.2),Inches(0.46),[[(label,11,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
        rect(s,bx+bw-Inches(1.35),ry+Inches(0.08),Inches(0.95),Inches(0.3),TEAL)
        txt(s,bx+bw-Inches(1.35),ry+Inches(0.08),Inches(0.95),Inches(0.3),
            [[("⤓ Download",8,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    # numbered path on the right
    steps=[("Go to lms-tms.tertiaryinfotech.com","Open the portal in any browser."),
           ("Log in with your registered email","The same address used to enrol."),
           ("Open this course",f"{C.TITLE}."),
           ("Download the material","Slides, Learner Guide and Lesson Plan."),
           ("Keep them open in class","The assessment is open book.")]
    rx=Inches(7.72); rw=Inches(4.8); ry0=Inches(1.95); rh=Inches(4.55)
    gy=Inches(0.16); th=int((rh-gy*(len(steps)-1))/len(steps)); bd=Inches(0.46)
    for i,(t1,t2) in enumerate(steps):
        y=int(ry0+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.09),th,col)
        oval(s,rx+Inches(0.24),int(y+th/2-bd/2),bd,bd,col)
        txt(s,rx+Inches(0.24),int(y+th/2-bd/2),bd,bd,
            [[(str(i+1),15,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,rx+Inches(0.86),y,rw-Inches(1.1),th,
            [[(t1,12,INK,True)],[(t2,10,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=2)
    footer(s); return s

def stat_band(title,stats,kicker,color=BLUE):
    """Big-number band — n large figures with captions. Pure visual impact."""
    s=head(slide(),title,kicker,kcolor=color)
    n=len(stats); X0=Inches(0.85); TOTW=Inches(11.63); gx=Inches(0.3)
    cw=int((TOTW-gx*(n-1))/n); y=Inches(2.4); ch=Inches(3.4)
    for i,(big,cap) in enumerate(stats):
        x=int(X0+(cw+gx)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.12),col)
        txt(s,x+Inches(0.2),y+Inches(0.75),cw-Inches(0.4),Inches(1.15),
            [[(big,44,col,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.24),y+Inches(2.0),cw-Inches(0.48),Inches(1.2),
            [[(cap,13,INK,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s

def brk(kind,dur,color=AMBER):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),color); rect(s,0,Inches(7.28),SW,Inches(0.22),color)
    rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
    txt(s,0,Inches(2.75),SW,Inches(1.2),[[(kind,48,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,0,Inches(4.05),SW,Inches(0.8),[[(dur,22,color,True)]],align=PP_ALIGN.CENTER); PAGE["n"]+=1


MISSING_IMAGES=[]
def _img(name):
    p=os.path.join(IMG,name)
    if os.path.exists(p): return p
    MISSING_IMAGES.append(name)          # collected and reported at the end
    return None

def picture_slide(title,image,caption="",kicker=None,accent=BLUE):
    """Full-bleed visual slide: one large diagram/screenshot with a caption.
    Silently degrades to a caption-only slide if the asset is missing."""
    s=head(slide(),title,kicker,kcolor=accent)
    path=_img(image)
    top=Inches(1.9); avail_w=Inches(11.63)
    # Reserve a caption strip only when there is a caption, so tall portrait
    # screenshots can use nearly the full slide height instead of a thin band.
    avail_h=Inches(4.55) if caption else Inches(5.05)
    if path:
        from PIL import Image as _PILImage
        try:
            iw,ih=_PILImage.open(path).size
            ar=iw/ih
        except Exception:
            ar=16/9
        w=avail_w; h=int(w/ar)
        if h>avail_h:
            h=avail_h; w=int(h*ar)
        x=int(Inches(0.85)+(avail_w-w)/2); y=int(top+(avail_h-h)/2)
        s.shapes.add_picture(path,x,y,width=w,height=h)
    if caption:
        txt(s,Inches(0.85),Inches(6.55),Inches(11.63),Inches(0.45),
            [[(caption,12,GREY,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s

# ============================================================ BUILD
cover()

# ---------------- ADMIN (front) ----------------
section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
flow_h("Digital Attendance (Mandatory)",[
 "MORNING (AM)\nScan on arrival",
 "AFTERNOON (PM)\nScan after lunch",
 "ASSESSMENT\nScan before you begin"],kicker="TRAQOM · SSG DIGITAL ATTENDANCE",color=VIOLET)
tile_grid("How Digital Attendance Works",[
 ("Mandatory for WSQ funding","AM, PM and Assessment attendance must all be taken, on both training days."),
 ("The QR code","The trainer or administrator displays the QR code generated from the SSG portal."),
 ("How to submit","Scan the QR code with your mobile phone camera and submit your attendance."),
 ("75% minimum","At least 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=14,accent=VIOLET)
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
trainer_slide("YOUR TRAINER",C.TRAINER,"Principal Trainer\nTertiary Infotech Academy Pte Ltd",
 [("Role","Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
  ("Expertise","Internet of Things, embedded systems and cloud-connected devices."),
  ("Delivers","WSQ courses on IoT, Raspberry Pi, microcontrollers, AI and data analytics."),
  ("Founder","Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
 initials="AA",accent=BLUE)
content("Let's Know Each Other",[
 "Your name, organisation and role.",
 "Your experience with Raspberry Pi, electronics or programming — beginners are very welcome.",
 "One thing you would like to measure, monitor or control by the end of this course."],kicker="ICE-BREAKER")
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.","One conversation at a time.",
 "Be punctual; return from breaks on time.","75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
download_material()

# Skills Framework
tile_grid("Skills Framework — TSC",[
 ("TSC Title",C.TSC_TITLE),
 ("TSC Code",C.TSC_CODE),
 ("Sector","Environmental Services"),
 ("Proficiency","Level 4 — Manage the deployment of IoT solutions to monitor and control equipment and the environment, and to drive process improvement."),
],kicker="SKILLS FRAMEWORK",cols=2,size=14)
tile_grid("TSC Abilities — Assessed by the Practical Performance",
 [(c,t) for c,t in C.ABILITIES],
 kicker="WHAT THIS COURSE DEVELOPS  ·  A1–A4",cols=1,size=14)
# K1-K7 is seven items: at one column they are too short for the two-line
# title+description to fit, so split across two slides (4 + 3) instead of
# clipping the descriptions.
tile_grid("TSC Knowledge — Assessed by the Written Assessment",
 [(c,t) for c,t in C.KNOWLEDGE[:4]],
 kicker="WHAT THIS COURSE DEVELOPS  ·  K1–K4",cols=1,size=13,accent=TEAL)
tile_grid("TSC Knowledge — Assessed by the Written Assessment (cont.)",
 [(c,t) for c,t in C.KNOWLEDGE[4:]],
 kicker="WHAT THIS COURSE DEVELOPS  ·  K5–K7",cols=1,size=13,accent=TEAL)

# Lesson plan / outline
two_col("Lesson Plan — Day 1",
 [("Digital Attendance (AM) · Introductions",1),
  ("Learning outcomes, outline & TSC briefing",1),
  ("Topic 1: Overview of IoT  (LO1)",1),
  ("Discussion — Analyse an IoT Use Case",1),
  ("Lunch Break — 1 hour",1)],
 [("Digital Attendance (PM)",1),
  ("Topic 2: Collect & Post Data to Cloud  (LO2)",1),
  ("Lab 1: Register Your Raspberry Pi",1),
  ("Lab 2: Collect & Post Environmental Data",1),
  ("Day 1 recap and Q&A",1)],
 kicker="SCHEDULE · DAY 1 · 9:30am – 6:30pm",lhead="Morning  ·  9:30am – 12:30pm",rhead="Afternoon  ·  1:30pm – 6:30pm")
two_col("Lesson Plan — Day 2",
 [("Digital Attendance (AM) · Day 1 recap",1),
  ("Topic 3: Data Analytics & Visualization  (LO3)",1),
  ("Lab 3: Analyse & Visualise Your IoT Data",1),
  ("Discussion — Design Your Dashboard",1),
  ("Lunch Break — 1 hour",1)],
 [("Digital Attendance (PM)",1),
  ("Topic 4: Monitor Data & Trigger Control  (LO4)",1),
  ("Lab 4: Monitor Data and Trigger Control",1),
  ("TRAQOM Survey · Assessment attendance",1),
  ("Final Assessment — WA (60 min) + PP (60 min)",1)],
 kicker="SCHEDULE · DAY 2 · 9:30am – 6:30pm",lhead="Morning  ·  9:30am – 12:30pm",rhead="Afternoon  ·  1:30pm – 6:30pm")
tile_grid("Learning Outcomes",[
 ("LO1 · Analyse IoT technologies","Analyse the uses and functions of IoT technologies. (A1, K1)"),
 ("LO2 · Collect and post data","Collect environment data with Raspberry Pi and post it to cloud computing. (A2, K2, K3)"),
 ("LO3 · Analyse and visualise","Use cloud computing to analyse and visualise IoT data. (A3, K4, K5)"),
 ("LO4 · Monitor and control","Monitor data and trigger control on devices. (A4, K6, K7)")],
 kicker="WHAT YOU'LL ACHIEVE",cols=1,size=15)
tile_grid("Course Outline",[
 ("Topic 1 — Overview of IoT","Industry 4.0, what IoT is, sensors and actuators, wireless technologies, use cases."),
 ("Topic 2 — Collect & Post Data","Cloud platforms, Raspberry Pi as gateway, device tokens, HTTP REST and MQTT uplink."),
 ("Topic 3 — Analytics & Visualization","Dashboards, widgets, telemetry history, trends and alert rules."),
 ("Topic 4 — Monitor & Trigger Control","Downlink control, virtual pins, n8n automation, effectiveness and IoT security.")],
 kicker="FOUR TOPICS · TWO DAYS · FOUR HANDS-ON LABS",cols=1,size=15)
cards3(f"Hands-On Labs on {C.PLATFORM}",[
 (BLUE,"Day 1 · Labs 1–2",["Register your Raspberry Pi","Collect and post sensor data","HTTP REST and MQTT uplink"]),
 (TEAL,"Day 2 · Lab 3",["Build a live dashboard","Analyse telemetry history","Create alert rules"]),
 (VIOLET,"Day 2 · Lab 4",["Remote control over virtual pins","n8n automation and AI","Close the monitor-act loop"])],
 kicker=f"WHAT YOU'LL BUILD  ·  {C.PLATFORM_URL}")
tile_grid("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.",
 "No discussion during the assessment.",
 "Use a black or blue pen for hard-copy assessments.",
 "No liquid paper or correction tape.",
 "Scripts are collected when the time is up."],
 kicker="BEFORE YOU BEGIN",cols=2,size=15,accent=AMBER)
cards3("Final Assessment",[
 (BLUE,"WA (Q&A) — 60 min",["Short-answer questions","Assesses knowledge K1–K7","Open book"]),
 (TEAL,"Practical Performance — 60 min",["Build a working IoT solution","Assesses abilities A1–A4","Open book, done individually"]),
 (VIOLET,"What you may use",["The course slides","Your Learner Guide","Approved materials only","An appeal process is available"])],
 kicker="ASSESSMENT · 120 MINUTES TOTAL · END OF DAY 2")
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit the WA (Q&A) — 60 min, open book",
 "Complete the Practical Performance — 60 min",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")

# ================================================================ DAY 1
section("DAY 1",C.DAY_THEMES[1],"1","Topic 1: Overview of IoT  ·  Topic 2: Collect and Post Environmental Data to Cloud")

# ---------------- TOPIC 1 — OVERVIEW OF IoT ----------------
T=C.TOPICS[0]
section(f"TOPIC {T['code']}",T["title"],T["code"],T["subtitle"])
big_statement("We are in the 4th Industrial Revolution.",
 "Steam, electricity, computers — and now cyber-physical systems where physical assets report their own state in real time.",
 "WHY NOW",color=BLUE)
tile_grid(f"Key Concepts — {T['title']}",T["concepts"],kicker=f"{T['weighting']}",cols=2,size=13)
picture_slide("The Fourth Industrial Revolution","industry40.png",
 caption="Industry 4.0 — cyber-physical systems, IoT, cloud computing and cognitive computing.",
 kicker="TOPIC 01 · CONTEXT")
flow_h("The Four Industrial Revolutions",[
 "1.0  STEAM\nMechanisation",
 "2.0  ELECTRICITY\nMass production",
 "3.0  COMPUTERS\nAutomation",
 "4.0  CYBER-PHYSICAL\nIoT, AI and the cloud"],kicker="FROM STEAM TO SENSORS",color=BLUE)
tile_grid("Technologies Driving Industry 4.0",[
 ("Industrial IoT (IIoT)","Connected machines and sensors on the factory or plant floor."),
 ("Big data & analytics","Turning high-volume machine data into operational decisions."),
 ("Cloud computing","Storage, compute and availability without running your own servers."),
 ("Cybersecurity","Protecting devices, data and the physical processes they control."),
 ("Autonomous robots","Machines that sense their environment and act without an operator."),
 ("Digital twin","A live simulation of a physical asset, fed by its own telemetry.")],
 kicker="THE TECHNOLOGY LANDSCAPE",cols=2,size=13,accent=VIOLET)
picture_slide("What Is the Internet of Things?","iot-definition.png",
 caption="IoT connects everyday objects to the internet so they can send and receive data.",
 kicker="TOPIC 01 · DEFINITION")
picture_slide("The Components of an IoT System","iot-components.png",
 caption="A 'thing' is any object with embedded electronics that transfers data over a network.",
 kicker="TOPIC 01 · COMPONENTS")
stat_band("The Scale of IoT",[
 ("$9T","Estimated IoT market value"),
 ("50B+","Connected devices worldwide"),
 ("4th","Industrial revolution underway"),
 ("5G","The accelerator to mass adoption")],kicker="THE OPPORTUNITY",color=BLUE)
picture_slide("Driving Forces of IoT","driving-forces.png",
 caption="Low-cost sensors and long-range wireless made IoT viable; 5G is driving mass adoption.",
 kicker="TOPIC 01 · DRIVING FORCES")
flow_h("How IoT Works — The Four Building Blocks",[
 "SENSORS & DEVICES capture data from the physical world",
 "CONNECTIVITY carries it over WiFi, cellular, LoRa or MQTT",
 "CLOUD stores, processes and analyses the data",
 "USER INTERFACE shows insight and sends commands back"],kicker="THE IoT ARCHITECTURE",color=TEAL)
picture_slide("How IoT Works","how-iot-works.png",
 caption="Sensors and devices talk to the cloud; software processes the data and acts, or shows it to a user.",
 kicker="TOPIC 01 · ARCHITECTURE")
tile_grid("What Is a Sensor?",[
 ("Definition","A device that detects an event or change in its environment and turns it into a signal."),
 ("Temperature","Thermocouples, thermistors, RTDs and semiconductor sensors — the most measured quantity."),
 ("Humidity & pressure","Environmental monitoring for comfort, process control and weather sensing."),
 ("Proximity & motion","Detect the presence, absence or movement of an object without contact."),
 ("Gas & chemical","Air quality, CO₂ and hazardous-gas detection in cities and industrial plants."),
 ("Light & IR","Ambient light sensing, obstacle detection and remote-control technology.")],
 kicker="TOPIC 01 · SENSING THE PHYSICAL WORLD",cols=2,size=13)
picture_slide("Sensors for IoT","sensors-overview.png",
 caption="Low-cost sensors are what made large-scale IoT deployment economically viable.",
 kicker="TOPIC 01 · SENSORS")
picture_slide("More Sensors for IoT","sensors-more.png",
 caption="Every physical quantity a business cares about has a low-cost sensor for it.",
 kicker="TOPIC 01 · SENSORS")
picture_slide("Actuators for IoT","iot-actuator.png",
 caption="Actuators turn a decision in the cloud back into a physical action.",
 kicker="TOPIC 01 · ACTUATORS")
cards3("Sensors, Actuators and Gateways",[
 (BLUE,"Sensors — sense",["Temperature & humidity","Motion, presence, vibration","Light, gas, air quality","GPS location, current"]),
 (TEAL,"Actuators — act",["Relays and switches","Motors and servos","Valves and pumps","Alarms and displays"]),
 (VIOLET,"Gateways — connect",["Aggregate nearby devices","Translate protocols","Buffer when offline","Add edge processing"])],
 kicker="THE PHYSICAL LAYER")
tile_grid("Wireless Technologies for IoT",[
 ("WiFi","High bandwidth, short range, mains power — best indoors where power is available."),
 ("Bluetooth / BLE","Very low power, very short range — wearables and personal devices."),
 ("Zigbee / Z-Wave","Low-power mesh — smart buildings and home automation."),
 ("Cellular (4G/5G)","Wide coverage with a subscription cost — vehicles, logistics and remote assets."),
 ("LoRaWAN / Sigfox","Long range, very low power, tiny payloads — agriculture, metering, city-scale sensing."),
 ("NB-IoT","Licensed low-power wide-area networking with carrier-grade reliability.")],
 kicker="CONNECTIVITY CHOICES",cols=2,size=13,accent=VIOLET)
picture_slide("Wireless Technologies for IoT","wireless-tech.png",
 caption="Range, power consumption, bandwidth and cost determine which technology fits a use case.",
 kicker="TOPIC 01 · CONNECTIVITY")
picture_slide("Comparing Wireless Technologies","wireless-comparison.png",
 caption="There is no single best option — every choice trades range against power, bandwidth and cost.",
 kicker="TOPIC 01 · CONNECTIVITY")
tile_grid("Types of IoT",[
 ("Consumer IoT","Everyday use — home appliances, voice assistants, smart lighting and wearables."),
 ("Commercial IoT","Healthcare and transport — smart pacemakers, monitoring systems, connected cars."),
 ("Industrial IoT (IIoT)","Manufacturing and energy — digital control systems and industrial big data."),
 ("Infrastructure IoT","Smart cities — infrastructure sensors and city management systems.")],
 kicker="FOUR CATEGORIES",cols=2,size=14,accent=TEAL)
picture_slide("IoT vs Industrial IoT (IIoT)","iot-vs-iiot.png",
 caption="IIoT extends IoT into industrial sectors, where reliability and safety requirements are higher.",
 kicker="TOPIC 01 · IIoT")
picture_slide("IoT Applications Across Industry","iot-applications.png",
 caption="IoT has found its way into every conceivable field, from agriculture to aerospace.",
 kicker="TOPIC 01 · APPLICATIONS")
picture_slide("Use Case — Healthcare","usecase-healthcare.png",
 caption="Asset tracking and patient monitoring: find the nearest wheelchair, watch vitals continuously.",
 kicker="TOPIC 01 · USE CASE")
picture_slide("Use Case — Agriculture","usecase-agriculture.png",
 caption="Soil, weather and crop sensing drive precision irrigation and fertiliser decisions.",
 kicker="TOPIC 01 · USE CASE")
picture_slide("Use Case — Smart Home","usecase-smart-home.png",
 caption="Smart outlets, thermostats, locks and leak detectors improve efficiency and safety.",
 kicker="TOPIC 01 · USE CASE")
picture_slide("Use Case — Smart City","usecase-smart-city.png",
 caption="Air quality, smart lighting, infrastructure monitoring and parking management.",
 kicker="TOPIC 01 · USE CASE")
picture_slide("Use Case — Smart Building","usecase-smart-building.png",
 caption="Occupancy, energy and equipment sensing cut utility cost and enable predictive maintenance.",
 kicker="TOPIC 01 · USE CASE")
picture_slide("Use Case — Logistics","usecase-logistics.png",
 caption="Track-and-trace with temperature control — critical for food, flowers and pharmaceuticals.",
 kicker="TOPIC 01 · USE CASE")
picture_slide("Use Case — Manufacturing","usecase-manufacturing.png",
 caption="Production-line monitoring enables proactive maintenance before equipment fails.",
 kicker="TOPIC 01 · USE CASE")
picture_slide("Use Case — Retail","usecase-retail.png",
 caption="Smart shelves and beacons manage inventory and personalise the customer experience.",
 kicker="TOPIC 01 · USE CASE")
discussion_slide(C.DISCUSSIONS[0],kicker=f"TOPIC {T['code']} · ACTIVITY")
content(f"Recap — {T['title']}",[
 "IoT connects physical objects to the internet so they can collect and exchange data.",
 "Every IoT system has four blocks: sensors/devices, connectivity, cloud processing and a user interface.",
 "Sensors turn a physical phenomenon into a signal; actuators turn a decision back into physical action.",
 "Wireless choice trades range against power, bandwidth and cost — there is no single best option."],
 kicker="TOPIC RECAP",size=17)

brk("Lunch Break","1 hour  ·  Digital attendance (PM) on your return")

# ---------------- TOPIC 2 — COLLECT AND POST DATA ----------------
T=C.TOPICS[1]
section(f"TOPIC {T['code']}",T["title"],T["code"],T["subtitle"])
tile_grid(f"Key Concepts — {T['title']}",T["concepts"],kicker=f"{T['weighting']}",cols=2,size=13)
tile_grid("Cloud Computing for IoT",[
 ("Why the cloud","Constrained devices lack the storage, compute and availability the data needs."),
 ("Always available","The platform keeps receiving data whether or not your laptop is switched on."),
 ("Scales with the fleet","One device or a thousand — the same endpoint and the same code."),
 ("Data persistence","History is retained so trends and performance can be analysed later."),
 ("Accessible anywhere","A browser or a phone shows the same live data from any location."),
 ("Integrations","Webhooks and APIs push events into the systems the business already uses.")],
 kicker="THE CLOUD LAYER",cols=2,size=13)
picture_slide("Cloud Computing for IoT","cloud-computing.png",
 caption="The cloud gives constrained devices the storage, compute and availability they lack.",
 kicker="TOPIC 02 · THE CLOUD LAYER")
picture_slide(f"{C.PLATFORM} — {C.PLATFORM_URL}","iotflow-home.png",
 caption="The platform you will use for every lab in this course.",
 kicker="TOPIC 02 · OUR PLATFORM",accent=TEAL)
tile_grid(f"{C.PLATFORM} — Our IoT Platform",[
 ("Projects","A self-contained workspace with its own devices, dashboard, alerts, map and automations."),
 ("Devices & tokens","Register a device in a guided wizard; a device token authenticates every message it sends."),
 ("HTTP & MQTT","POST JSON to a REST endpoint, or publish/subscribe over MQTT for real-time two-way traffic."),
 ("Dashboards","Number cards, gauges, charts, LED indicators and maps that refresh automatically."),
 ("Alerts & automations","Threshold and offline rules that fire a webhook into an n8n workflow."),
 ("Clients","Official Python client (pip install iotflow) and an Arduino library for ESP32/ESP8266.")],
 kicker=f"{C.PLATFORM_URL}",cols=2,size=13,accent=TEAL)
tile_grid("The Raspberry Pi as an IoT Gateway",[
 ("A full Linux computer","Low cost and credit-card sized, running Raspberry Pi OS with Python built in."),
 ("GPIO pins","Connect sensors and actuators directly to the board — no extra hardware needed."),
 ("Built-in WiFi","Reaches the cloud without a separate network module."),
 ("Python ecosystem","sense_hat, gpiozero, adafruit-dht and the iotflow client are a pip install away."),
 ("Runs unattended","systemd restarts your sensor script automatically after a power cut."),
 ("Remote access","SSH or VNC lets you work on the Pi headless, from your laptop.")],
 kicker="THE DEVICE LAYER",cols=2,size=13,accent=BLUE)
cards3("Reading Environmental Data",[
 (BLUE,"Sense HAT",["Temperature, humidity, pressure","Motion and orientation","8×8 LED matrix and joystick","One import: sense_hat"]),
 (TEAL,"DHT11 / DHT22",["Temperature and humidity","Connects to a single GPIO pin","Very low cost","adafruit_dht library"]),
 (VIOLET,"Simulated data",["No hardware required","Random or replayed values","Useful for testing the uplink","Identical platform behaviour"])],
 kicker="THREE WAYS TO GET A READING")
flow_h("The IoT Data Round Trip",[
 "DEVICE reads a sensor value",
 "UPLINK posts it over HTTP or MQTT",
 "CLOUD stores, charts and evaluates rules",
 "DECISION — a person or an automation acts",
 "DOWNLINK sends a command back to the device"],kicker="FROM SENSOR TO ACTION AND BACK",color=BLUE)
picture_slide("How MQTT Works","how-mqtt-works.png",
 caption="Publish/subscribe: devices publish to a topic and the broker delivers to every subscriber.",
 kicker="TOPIC 02 · PROTOCOLS")
two_col("HTTP REST vs MQTT",
 [("HTTP REST",0),("Request/response",1),("Simplest to start with",1),
  ("POST JSON to an endpoint",1),("Works from cURL or any language",1),("Higher overhead per message",1)],
 [("MQTT",0),("Publish/subscribe via a broker",1),("Lightweight and low bandwidth",1),
  ("Persistent connection",1),("Best for real-time two-way control",1),("Ideal for many devices",1)],
 kicker="CHOOSING YOUR UPLINK PROTOCOL",lhead="Simple",rhead="Real-time")
tile_grid("Device Tokens and Security",[
 ("What a token is","A secret string that authenticates every message the device sends."),
 ("Shown once","Copy it when the device is created — the platform will not display it again."),
 ("Anyone holding it can post","A leaked token means someone else can publish as your device."),
 ("Keep it out of code","Store it in an environment variable, never in a Git repository."),
 ("Use TLS endpoints","Encrypt the data in transit so the token cannot be read off the wire."),
 ("Rotate if exposed","Regenerate the token immediately if you suspect it has leaked.")],
 kicker="K2 · AUTHENTICATING THE DEVICE",cols=2,size=13,accent=AMBER)

# --- the hands-on practical block: overview + one visual slide per lab (NO steps) ---
big_statement("Hands-On Practical — Labs 1 and 2",
 f"Running on {C.PLATFORM} ({C.PLATFORM_URL}). Step-by-step instructions are in your Learner Guide — follow along there.",
 "TOPIC 02 · PRACTICAL",color=TEAL)
for a in DOMAIN2:
    lab_outcome(a,kicker=f"TOPIC {T['code']} · HANDS-ON")
    if a.get("image"):
        picture_slide(f"Lab {a['num']} — {a['title']}", a["image"],
                      caption=f"{C.PLATFORM} — {a['build']}",
                      kicker=f"TOPIC {T['code']} · WHAT YOU'LL SEE",accent=TEAL)
content(f"Recap — {T['title']}",[
 "The cloud gives a constrained device the storage, availability and reach it does not have on its own.",
 "The Raspberry Pi reads a sensor over GPIO and posts the reading to the cloud over HTTP or MQTT.",
 "A device token authenticates every message — treat it like a password.",
 "Once the uplink is reliable, the business finally has data it can act on."],
 kicker="TOPIC RECAP",size=17)
big_statement("End of Day 1",
 "Tomorrow: turn the data you are now collecting into a dashboard, an alert, and an automatic control action.",
 "SEE YOU AT 9:30AM",color=BLUE)

# ================================================================ DAY 2
section("DAY 2",C.DAY_THEMES[2],"2","Topic 3: IoT Data Analytics and Visualization  ·  Topic 4: Monitor Data to Trigger Control from Cloud")

# ---------------- TOPIC 3 — ANALYTICS AND VISUALIZATION ----------------
T=C.TOPICS[2]
section(f"TOPIC {T['code']}",T["title"],T["code"],T["subtitle"])
big_statement("Raw readings are not insight.",
 "A number in a database changes nothing. A dashboard that makes a problem obvious — and an alert that arrives in time — is what changes the outcome.",
 "WHY VISUALISE",color=TEAL)
tile_grid(f"Key Concepts — {T['title']}",T["concepts"],kicker=f"{T['weighting']}",cols=2,size=13)
tile_grid("Choosing the Right Widget",[
 ("Number card","One current value at a glance — the reading somebody asks for most often."),
 ("Gauge","A value inside its safe operating range — instantly shows 'how close to the limit'."),
 ("Line chart","History over time — the only way to see trends, drift and daily cycles."),
 ("Bar chart","Comparing totals across periods or across devices."),
 ("LED indicator","A binary state: on/off, open/closed, healthy/faulty."),
 ("Map","Where the device is — essential for vehicles, logistics and field assets.")],
 kicker="DISPLAY WIDGETS",cols=2,size=13,accent=TEAL)
flow_h("From Reading to Decision",[
 "COLLECT telemetry from the device",
 "VISUALISE it on a dashboard",
 "ANALYSE the history for trends and drift",
 "DETECT when a threshold is crossed",
 "DECIDE and record the action taken"],kicker="A3 · THE ANALYTICS PIPELINE",color=TEAL)
tile_grid("Analysing IoT Data",[
 ("Current vs normal","Compare the live reading against the established operating range."),
 ("Trends over time","A slow drift upward is often more important than a single high reading."),
 ("Peaks and troughs","The extremes reveal whether the process ever leaves its safe envelope."),
 ("Noise vs event","One odd sample is noise; a sustained change is a real event worth acting on."),
 ("Correlation","Temperature rising as humidity falls tells a story neither metric tells alone."),
 ("Recording performance","The telemetry history is the evidence that the solution actually works.")],
 kicker="K5 · ADVANCED PROCESS CONTROL",cols=2,size=13)
tile_grid("Alert Rules That Work",[
 ("Threshold rules","Fire when a metric crosses a limit: temperature > 30, humidity < 40."),
 ("Device-offline rules","Fire when a device stops reporting — silent failure is the biggest risk."),
 ("Set a meaningful limit","Choose the value at which a person would genuinely need to act."),
 ("Avoid alert fatigue","Too many alerts and the real one gets ignored — tune the threshold."),
 ("Active and resolved","Track the alert lifecycle so response time can be measured."),
 ("Trigger automation","An alert can call a webhook and start a workflow with no human involved.")],
 kicker="DETECTING WHAT MATTERS",cols=2,size=13,accent=AMBER)
big_statement("Hands-On Practical — Lab 3",
 f"Running on {C.PLATFORM} ({C.PLATFORM_URL}). Step-by-step instructions are in your Learner Guide — follow along there.",
 "TOPIC 03 · PRACTICAL",color=TEAL)
for a in DOMAIN3:
    lab_outcome(a,kicker=f"TOPIC {T['code']} · HANDS-ON")
    if a.get("image"):
        picture_slide(f"Lab {a['num']} — {a['title']}", a["image"],
                      caption=f"{C.PLATFORM} — {a['build']}",
                      kicker=f"TOPIC {T['code']} · WHAT YOU'LL SEE",accent=TEAL)
discussion_slide(C.DISCUSSIONS[1],kicker=f"TOPIC {T['code']} · ACTIVITY")
content(f"Recap — {T['title']}",[
 "A dashboard turns a stream of readings into an operational picture somebody can act on.",
 "Pick the widget that answers the question: number for now, gauge for range, chart for trend.",
 "Analyse history, not just the latest value — trends and drift matter more than one sample.",
 "An alert rule set at a business-meaningful threshold turns monitoring into timely action."],
 kicker="TOPIC RECAP",size=17)

brk("Lunch Break","1 hour  ·  Digital attendance (PM) on your return")

# ---------------- TOPIC 4 — MONITOR AND TRIGGER CONTROL ----------------
T=C.TOPICS[3]
section(f"TOPIC {T['code']}",T["title"],T["code"],T["subtitle"])
tile_grid(f"Key Concepts — {T['title']}",T["concepts"],kicker=f"{T['weighting']}",cols=2,size=13)
two_col("Uplink vs Downlink",
 [("Uplink — telemetry",0),("Device → cloud",1),("Sensor readings and status",1),
  ("HTTP POST /api/telemetry",1),("or MQTT publish",1),("This is your monitoring data",1)],
 [("Downlink — commands",0),("Cloud → device",1),("Switch a relay, set a value",1),
  ("MQTT topic devices/<id>/down",1),("or HTTP state polling",1),("This is your automation",1)],
 kicker="TWO DIRECTIONS, TWO PURPOSES",lhead="Monitoring",rhead="Control")
tile_grid("Control Widgets and Virtual Pins",[
 ("Virtual pin","A named channel (V1, relay, pump) carrying a command from dashboard to device."),
 ("Switch","A toggle for a persistent on/off state — a relay, a fan, a pump."),
 ("Button","A momentary action — reset, trigger, open for two seconds."),
 ("Slider","A value within a range — motor speed, brightness, a setpoint."),
 ("Terminal","Free-text commands for diagnostics and advanced control."),
 ("@on_command","The handler on the Pi that receives the value and drives the GPIO pin.")],
 kicker="K3 · EQUIPMENT AUTOMATION",cols=2,size=13,accent=VIOLET)
flow_h("Closing the Monitor-and-Control Loop",[
 "SENSE — the Pi reads the temperature",
 "REPORT — telemetry arrives in the cloud",
 "DETECT — the alert rule crosses its threshold",
 "AUTOMATE — n8n notifies, logs and decides",
 "ACT — a downlink command switches the fan on"],kicker="A4 · THE FULL LOOP",color=TEAL)
tile_grid("Automation with n8n",[
 ("Webhook trigger","IoTFlow calls an n8n webhook when your chosen event fires."),
 ("Notify","Email, Telegram or WhatsApp so the right person hears about it immediately."),
 ("Record","Append the event to Google Sheets or a database to build the performance history."),
 ("Analyse with AI","An AI node summarises recent readings and recommends an action in plain language."),
 ("Control","An HTTP Request node sends a downlink command straight back to the device."),
 ("No code","The whole workflow is drag-and-drop — no server and no deployment.")],
 kicker="LOW-CODE WORKFLOWS",cols=2,size=13,accent=TEAL)
big_statement("Hands-On Practical — Lab 4",
 f"Running on {C.PLATFORM} ({C.PLATFORM_URL}). Step-by-step instructions are in your Learner Guide — follow along there.",
 "TOPIC 04 · PRACTICAL",color=TEAL)
for a in DOMAIN4:
    lab_outcome(a,kicker=f"TOPIC {T['code']} · HANDS-ON")
    if a.get("image"):
        picture_slide(f"Lab {a['num']} — {a['title']}", a["image"],
                      caption=f"{C.PLATFORM} — {a['build']}",
                      kicker=f"TOPIC {T['code']} · WHAT YOU'LL SEE",accent=TEAL)
tile_grid("Monitoring the Effectiveness of an IoT Solution",[
 ("Device uptime","What percentage of the time is the device actually reporting?"),
 ("Data completeness","Are readings arriving at the expected interval, with no silent gaps?"),
 ("Alert response time","How long from the threshold being crossed to the action being taken?"),
 ("False-positive rate","How many alerts turned out not to need any action at all?"),
 ("The business metric","Did downtime, energy, spoilage or labour actually improve?"),
 ("Tune and repeat","Adjust thresholds and sampling rates based on what the record shows.")],
 kicker="A4 · IS IT WORKING?",cols=2,size=13,accent=BLUE)
cards3("IoT Security — Why It Is Different",[
 (AMBER,"Constrained devices",["Microcontrollers, not servers","Often battery powered","May not support TLS/SSL"]),
 (VIOLET,"Unattended & long-lived",["Run for years without supervision","Patching is inconvenient","Rogue devices go unnoticed"]),
 (BLUE,"Physical consequences",["IT breach leaks data","IoT breach can cause harm","Safety-critical systems at risk"])],
 kicker="K6 · RISK FACTORS")
picture_slide("IoT Security Is a Top Concern","iot-security-concern.png",
 caption="Security and data privacy are consistently the biggest barriers to IoT adoption.",
 kicker="TOPIC 04 · SECURITY",accent=AMBER)
big_statement("The Mirai botnet, 12 October 2016.",
 "Default credentials on cameras and routers were harvested into a botnet whose DDoS attack took much of the US east coast offline — an unsecured device is everyone's problem.",
 "CASE STUDY · WHY DEVICE SECURITY MATTERS",color=AMBER)
tile_grid("Securing Your IoT Solution",[
 ("Change default credentials","The single most common cause of IoT compromise — Mirai proved it."),
 ("Protect the device token","Environment variables, never source control; rotate it if exposed."),
 ("Encrypt in transit","Use TLS endpoints so readings and tokens cannot be read off the wire."),
 ("Keep firmware updated","Unpatched, unattended devices are the easiest target on any network."),
 ("Segment the network","Keep IoT devices off the network carrying business-critical systems."),
 ("Least privilege","A device should be able to do its job and nothing more.")],
 kicker="K6 · SECURITY AND PRIVACY APPLICATIONS",cols=2,size=13,accent=AMBER)
tile_grid("IoT Guidelines and Communication Standards",[
 ("MQTT","OASIS-standard lightweight publish/subscribe messaging — the IoT default."),
 ("HTTP / REST","Universally supported request-response, easiest to integrate and debug."),
 ("CoAP","A compact request-response protocol designed for very constrained devices."),
 ("IEEE 802.15.4","The physical/MAC layer beneath Zigbee and other low-rate wireless networks."),
 ("LoRaWAN","LoRa Alliance specification for long-range, low-power wide-area networking."),
 ("IMDA & PDPA","Singapore's IoT cyber-security guide and personal-data obligations.")],
 kicker="K7 · STANDARDS THAT MATTER",cols=2,size=13,accent=VIOLET)
discussion_slide(C.DISCUSSIONS[2],kicker=f"TOPIC {T['code']} · ACTIVITY")
content(f"Recap — {T['title']}",[
 "Reading data back and sending commands forward turns monitoring into automation.",
 "Virtual pins carry the command from the dashboard to a handler that drives the GPIO pin.",
 "Alerts plus n8n notify, record, analyse with AI and can act with no human in the loop.",
 "Measure effectiveness — uptime, response time and the business metric — and secure every layer."],
 kicker="TOPIC RECAP",size=17)

# ---------------- CLOSE ----------------
section("WRAP-UP","Course Summary & Next Steps","")
tile_grid("What You Achieved",[
 ("LO1 · Analysed IoT technologies","Sensors, actuators, wireless technologies and use cases across nine industries."),
 ("LO2 · Collected and posted data","Registered a Raspberry Pi and streamed live sensor readings over HTTP and MQTT."),
 ("LO3 · Analysed and visualised","Built a live dashboard, analysed telemetry history and set a working alert rule."),
 ("LO4 · Monitored and controlled","Drove hardware from the cloud and automated the response end to end.")],
 kicker="LEARNING OUTCOMES",cols=1,size=15)
tile_grid("Your Next Steps",[
 ("Keep your IoTFlow project","Your devices, dashboard and automations stay available after the course."),
 ("Deploy your Pi for real","Pick one thing worth measuring and let it run unattended for a week."),
 ("Revisit the Learner Guide","Every lab's step-by-step instructions are there for you to repeat."),
 ("Explore the tutorials",f"More platform walkthroughs at {C.PLATFORM_DOCS}")],
 kicker="AFTER TODAY",cols=2,size=14,accent=TEAL)
content("Recommended Courses",[
 "WSQ - Internet of Things (IoT) Fundamental for Beginners",
 "WSQ - Business Innovation with Internet of Things (IoT)",
 "WSQ - Practical Electronics Design with Arduino Microcontroller",
 "WSQ - Hands-On Guide to IoT Development with Microcontrollers",
 "Browse the full catalogue at www.tertiarycourses.com.sg"],kicker="CONTINUE YOUR LEARNING")
content("Summary & Q&A",[
 "IoT connects physical assets so an organisation can measure what used to be invisible.",
 "The Raspberry Pi reads the physical world; the cloud stores, analyses and acts on it.",
 "Dashboards make performance visible, alerts make problems timely, automation closes the loop.",
 "Any questions before the assessment?"],kicker="SUMMARY")
cards3("Final Assessment",[
 (BLUE,"WA (Q&A) — 60 min",["Short-answer questions","Assesses knowledge K1–K7","Open book"]),
 (TEAL,"Practical Performance — 60 min",["Build a working IoT solution","Assesses abilities A1–A4","Open book, done individually"]),
 (VIOLET,"Before you begin",["Take the Assessment digital attendance","Complete the TRAQOM survey","Slides + Learner Guide allowed","Submit as directed by your assessor"])],
 kicker="ASSESSMENT · 120 MINUTES TOTAL")
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit the WA (Q&A) — 60 min, open book",
 "Complete the Practical Performance — 60 min",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")
tile_grid("Digital Attendance & TRAQOM Survey (Mandatory)",[
 ("Assessment attendance","Take the Assessment digital attendance before you begin — scan the SSG QR code."),
 ("Cert & TRAQOM survey","Complete the mandatory survey at https://lms-tms.tertiaryinfotech.com/"),
 ("Your certificate","Your certificate is issued through the LMS once you are assessed Competent."),
 ("75% minimum","At least 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=14,accent=VIOLET)
tile_grid("Support",[
 ("Email","enquiry@tertiaryinfotech.com"),
 ("Telephone","+65 6100 0613"),
 ("Website","www.tertiarycourses.com.sg"),
 ("LMS / TMS portal","https://lms-tms.tertiaryinfotech.com")],
 kicker="WE'RE HERE TO HELP — DURING AND AFTER THE CLASS",cols=2,size=15)
big_statement("Thank You!",
 "You can now build, analyse and control a complete IoT solution with a Raspberry Pi and the cloud.",
 "SEE YOU AT THE NEXT COURSE",color=TEAL)

# Guard: a picture slide that silently loses its image looks fine to the build
# but ships a blank slide, so fail loudly instead.
if MISSING_IMAGES:
    raise SystemExit(f"ERROR: {len(MISSING_IMAGES)} image(s) not found in {IMG}: "
                     + ", ".join(sorted(set(MISSING_IMAGES))))

OUT=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
print(f"Saved {OUT}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)  images from {IMG}")
