#!/usr/bin/env python3
"""Generate the Business Innovation with IoT (TGS-2026064711) Learner Guide as
BOTH a Markdown mirror (LG-*.md at repo root) and a DOCX (courseware/LG-*.docx)
from one source, so the two can never diverge.

House format: cover page, Document Version Control Record, page-numbered TOC,
Arial 11pt body, one section per topic (key concepts + the facilitated
discussion) and per lab (Objective, Goal, What you'll build, platform
screenshot, Why the business cares, Step-by-step with commands, Test it), plus
setup, troubleshooting and an IoT glossary.

This is where the STEP-BY-STEP lab instructions live. The slide deck shows each
lab's purpose and outcome only — by design.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

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
IMG=os.path.join(REPO,"assets")   # course diagrams & screenshots

# ---------------- block DSL (single content stream → MD + DOCX) ----------------
B=[]
def h1(t): B.append(("h1",t))
def h2(t): B.append(("h2",t))
def h3(t): B.append(("h3",t))
def p(t):  B.append(("p",t))
def bullets(xs): B.append(("bullets",xs))
def steps(xs): B.append(("steps",xs))
def code(t): B.append(("code",t))
def note(t): B.append(("note",t))
def rule(): B.append(("rule",))
def image(path,caption=""): B.append(("image",path,caption))

# ---------------- content ----------------
h1("Introduction")
p(f"This Learner Guide accompanies the WSQ course {C.TITLE} ({C.COURSE_CODE}), conducted by {C.ORG}. "
  f"It is a one-day (8-hour) course mapped to the Skills Framework for Infocomm Technology TSC "
  f"{C.TSC_TITLE} ({C.TSC_CODE}, Level 4).")
p("The course answers a business question, not only a technical one: where can the Internet of Things "
  "create value in your organisation, and how would you justify and implement it? Topics 1, 2, 4 and 5 "
  "build the business case through facilitated discussion. Topic 3 is hands-on — you will connect a "
  f"device to the cloud yourself on {C.PLATFORM} ({C.PLATFORM_URL}) so that the technology is concrete "
  "rather than abstract.")
p("This guide contains the full step-by-step instructions for every lab. The slide deck deliberately "
  "shows only each lab's purpose and outcome, so follow the numbered steps here while the trainer "
  "demonstrates. Keep this guide with you during the assessment — it is open book.")

h1("Course Learning Outcomes")
p("On completion of this course, you will be able to:")
bullets(C.LEARNING_OUTCOMES)

h1("How This Course Is Assessed")
p("The assessment has two instruments, both open book, conducted at the end of the training day:")
bullets([
 C.ASSESSMENT["written"],
 C.ASSESSMENT["practical"],
 "Open book means you may refer to the course slides, this Learner Guide and any approved materials.",
 C.ASSESSMENT["note"],
 "An appeal process is available if you disagree with the assessment outcome.",
])
p("The Written Assessment covers the five abilities (A1–A5) and the Oral Questioning covers the four "
  "knowledge statements (K1–K4). Each topic in this guide is labelled with the ability and knowledge "
  "it develops, so you can see exactly what each session is preparing you for.")

h1("Skills Framework Mapping")
h3("Abilities — assessed by the Written Assessment")
bullets([f"{code} — {txt}" for code,txt in C.ABILITIES])
h3("Knowledge — assessed by Oral Questioning")
bullets([f"{code} — {txt}" for code,txt in C.KNOWLEDGE])

h1("Before You Start — Setting Up for the Hands-On Labs")
h3("What you need")
bullets([
 f"A free learner account on {C.PLATFORM} — {C.PLATFORM_URL}. Sign up with your email; no credit card is required.",
 "A laptop with a modern web browser. Every lab can be completed from the browser and a terminal.",
 "A terminal with cURL available (built into macOS, Linux and Windows 10+).",
 "Optional — Python 3 with the official client: pip install \"iotflow[mqtt]\" for the scripted labs.",
 "Optional — IoT hardware (ESP32 or ESP8266) if you want to send readings from a real sensor. "
 "The Arduino library speaks the same protocol as the Python client, so the platform cannot tell the difference.",
])
h3("Create your account and project")
p(f"Open {C.PLATFORM_URL}, sign up, then create a project. A project is a self-contained workspace with "
  "its own devices, dashboard, alerts, map and automations. Name it after a business scenario you care "
  "about — for example Cold Chain Monitoring, Smart Office or Workshop Machine Health. Using a real "
  "scenario makes the discussions in Topics 4 and 5 much more productive.")
code("Open https://iot.tertiaryinfotech.com  ->  Sign up  ->  Log in  ->  New project")
h3("Conventions used in every lab")
bullets([
 "Placeholders in CAPITALS or angle brackets are replaced with your own values — dev_XXXXXXXXXXXX is your device token and <id> is your device id.",
 "Your device token is shown only once when the device is created. Save it somewhere safe before closing the dialog.",
 "Commands prefixed with a $ are run in your terminal; Python snippets are run in a .py file or an interactive session.",
 "Dashboard widgets refresh automatically about every 5 seconds, so allow a moment for a new reading to appear.",
 "If a step fails, check the token first — an expired or mistyped token is by far the most common cause.",
])
note("Treat your device token like a password. Anyone who holds it can post data as your device. This is "
     "exactly the credential-management problem discussed in Topic 4 on IoT security.")

# ---------------- per-topic, per-lab ----------------
DISC_BY_TOPIC={d["topic"]:d for d in C.DISCUSSIONS}
for t in C.TOPICS:
    h1(f"Topic {t['code']} — {t['title']}  ({t['weighting']})")
    p(t["subtitle"])
    h3("Key concepts")
    bullets([f"{name} — {desc}" for name,desc in t["concepts"]])

    # Facilitated discussion for the lecture-only topics
    d=DISC_BY_TOPIC.get(t["num"])
    if d:
        h2(f"Activity — {d['title']}  ({d['mins']} minutes)")
        p(d["brief"])
        h3("Discussion prompts")
        bullets(d["prompts"])
        h3("What to produce")
        p(d["output"])
        note("Write your answer down as you go. The same reasoning is what the Written Assessment asks "
             f"you to demonstrate for {d['code']}.")

    # Hands-on labs (Topic 3 only)
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        h2(f"Lab {a['num']} — {a['title']}")
        p(f"Objective: {a['objective']}")
        p(f"Goal: {a['desc']}")
        h3("What you'll build")
        p(a["build"]+f"   (Tools: {a['services']}.)")
        if a.get("image"):
            image(a["image"],f"{C.PLATFORM} — Lab {a['num']}: {a['title']}")
        if a.get("business"):
            h3("Why the business cares")
            p(a["business"])
        h3("Step-by-step")
        steps([(instr,cmd) for instr,cmd in a["steps"]])
        h3("Test it")
        p(a["test"])
        note(f"A standalone copy of this lab is in labs/lab-{a['num']:02d}/README.md, with runnable "
             f"Python scripts beside it, so you can repeat it after the course. "
             f"Your {C.PLATFORM} project stays available to you.")
        rule()

h1("Putting It Together — From Opportunity to Action Plan")
p("By the end of the day you should be able to carry one idea through the whole arc of the course. "
  "This is the reasoning the assessment is built around:")
steps([
 ("Compare your current business model with an IoT-enabled model in your industry, and state what "
  "would have to change for you to adopt it. (A1, K1)",""),
 ("Identify a specific process that is invisible, manual or reactive today, and define what you would "
  "measure, how often, and who or what would act on the reading. (A2, K1)",""),
 ("Explain how the data would actually flow — device, uplink, cloud, dashboard or alert, and the "
  "downlink command that closes the loop. You did this end to end in Labs 1 to 4. (A3, K2)",""),
 ("Build the cost-benefit case: hardware, connectivity, platform, integration and running cost against "
  "labour saved, downtime avoided and new revenue. State the security and privacy risks honestly. (A4, K3)",""),
 ("Turn it into a staged action plan using design thinking — a pilot on one asset, a measurable success "
  "criterion, a named owner, and the evidence you would need before scaling. (A5, K4)",""),
])
note("If you can answer these five in order for your own organisation, you are ready for both the "
     "Written Assessment and the Oral Questioning.")

h1("Troubleshooting the Labs")
bullets([
 "No data on the dashboard — confirm the device token is correct and that you are posting to the right "
 "project. Re-copy the snippet from the device's Integrate page, which is pre-filled with your values.",
 "401 or 403 from the API — the Authorization header is missing, malformed, or the token is wrong. "
 "The header must read: Authorization: Bearer dev_XXXXXXXXXXXX",
 "Reading posted but no widget updates — check that the widget's metric name matches the key you sent "
 "exactly (temperature is not the same as Temperature).",
 "MQTT will not connect — confirm the broker host and port 1883, and that you installed the MQTT extra: "
 "pip install \"iotflow[mqtt]\". Without it the client falls back to HTTP only.",
 "Commands not reaching the device — the handler must be running. iot.run() polls over HTTP; "
 "iot.loop_forever() keeps an MQTT connection open for instant delivery.",
 "n8n workflow does not fire — make sure the workflow is ACTIVE and that you pasted the Production URL, "
 "not the Test URL, into the IoTFlow automation.",
])

h1("Glossary")
B.append(("dl",[
 ("Actuator","A device that acts on the physical world — a relay, motor, valve, pump or alarm — usually driven by a command from the cloud."),
 ("API key / Device token","The secret credential that authenticates a device to the platform. Sent as an Authorization: Bearer header."),
 ("Cloud platform","A managed service that ingests, stores, visualises and acts on telemetry so you do not run servers yourself."),
 ("Cost-benefit analysis","Weighing the total cost of an IoT deployment (hardware, connectivity, platform, integration, running cost) against its measurable benefits."),
 ("Dashboard","A screen of widgets — number cards, gauges, charts, LEDs, maps — that shows current and historical device data."),
 ("Design thinking","A five-stage innovation method — Empathise, Define, Ideate, Prototype, Test — from the Stanford d.school."),
 ("Digitisation","Applying digital technology to a business process so that it produces data that can be measured, analysed and acted on."),
 ("Downlink","Traffic from the cloud to the device — commands that change device state, such as switching a relay."),
 ("Edge computing","Processing data at or near the device instead of in the cloud, to cut latency, bandwidth and privacy exposure."),
 ("Gateway","A device that aggregates nearby sensors, translates protocols and forwards data to the cloud."),
 ("HTTP REST API","A request/response web interface. Devices POST readings as JSON to an endpoint such as /api/telemetry."),
 ("Industry 4.0","The fourth industrial revolution — the convergence of IoT, AI, 5G, cloud computing and robotics in industry."),
 ("IoT (Internet of Things)","Connecting physical objects to the internet so they can report their state and be acted upon remotely."),
 ("IoTFlow","The IoT cloud platform used for the hands-on labs in this course — https://iot.tertiaryinfotech.com"),
 ("LoRaWAN","A long-range, low-power wireless protocol for small payloads — used in agriculture, metering and city-scale sensing."),
 ("Mirai","The 2016 botnet that harvested IoT devices with default credentials and launched a major DDoS attack."),
 ("MQTT","A lightweight publish/subscribe messaging protocol designed for constrained devices and real-time two-way traffic."),
 ("n8n","A no-code workflow automation tool. An IoTFlow automation calls an n8n webhook to notify, log and analyse events."),
 ("Payback period","How long it takes for the accumulated benefits of an IoT deployment to exceed its total cost."),
 ("Predictive maintenance","Using sensor data to service equipment before it fails, converting unplanned downtime into scheduled work."),
 ("Sensor","A device that measures a physical quantity — temperature, humidity, motion, light, location — and reports it as data."),
 ("Telemetry","The stream of measurements a device sends to the cloud, each with a value and a timestamp."),
 ("Uplink","Traffic from the device to the cloud — sensor readings and status messages."),
 ("Virtual pin","A named channel (V1, relay, pump) that binds a dashboard control widget to a value the device acts on."),
 ("Webhook","An HTTP callback. The platform POSTs event data to a URL you supply, triggering an external workflow."),
]))

# ---------------- render Markdown ----------------
def _anchor(txt):
    return "".join(ch.lower() if ch.isalnum() else ("-" if ch in " -" else "") for ch in txt)

def render_md():
    out=[f"# {C.TITLE} — Learner Guide",""]
    out.append(f"**WSQ Course Code:** {C.COURSE_CODE}  |  **Conducted by:** {C.ORG} ({C.UEN.replace('UEN: ','UEN ')})  |  **Version {C.VERSION} · {C.VERSION_DATE}**")
    out.append("")
    # TOC (h1 + h2)
    out.append("## Contents"); out.append("")
    for kind,*rest in B:
        if kind=="h1": out.append(f"- [{rest[0]}](#{_anchor(rest[0])})")
        elif kind=="h2": out.append(f"  - [{rest[0]}](#{_anchor(rest[0])})")
    out.append("")
    for kind,*rest in B:
        if kind=="h1": out+=["",f"## {rest[0]}",""]
        elif kind=="h2": out+=["",f"### {rest[0]}",""]
        elif kind=="h3": out+=[f"**{rest[0]}**",""]
        elif kind=="p": out+=[rest[0],""]
        elif kind=="bullets": out+=[f"- {x}" for x in rest[0]]+[""]
        elif kind=="steps":
            for i,(instr,cmd) in enumerate(rest[0],1):
                out.append(f"{i}. {instr}")
                if cmd: out+=["",f"   ```bash",f"   {cmd}","   ```",""]
            out.append("")
        elif kind=="code": out+=["```bash",rest[0],"```",""]
        elif kind=="note": out+=[f"> **Note:** {rest[0]}",""]
        elif kind=="rule": out+=["---",""]
        elif kind=="image":
            # Assets live at the repo root; this Markdown is written into
            # courseware/, so climb one level to reach them.
            out+=[f"![{rest[1]}](../assets/{rest[0]})","",f"*{rest[1]}*",""]
        elif kind=="dl":
            for term,defn in rest[0]: out.append(f"- **{term}** — {defn}")
            out.append("")
    return "\n".join(out)

# The Markdown mirror sits beside the DOCX in courseware/ — that is the copy the
# repo tracks and publishes, so both must land in the same folder.
MD_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.md")
with open(MD_OUT,"w") as f: f.write(render_md())
print("Saved",MD_OUT)

# ---------------- render DOCX ----------------
BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
INKCODE=RGBColor(0x0B,0x30,0x60)
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)
prodoc.add_cover_page(doc,"LEARNER GUIDE",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=None, course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("9.0","1 January 2026","Previous release — 2-day structure with ThingSpeak, MATLAB and IFTTT practical activities.",C.TRAINER),
 ("10.0","8 August 2026",
  "Major revision. Restructured to the accredited one-day (8-hour) format per Course Proposal "
  "CA-WSQ-2020-007388. All practical activities replaced with four hands-on labs on the IoTFlow "
  "platform (https://iot.tertiaryinfotech.com); ThingSpeak, MATLAB and IFTTT content retired. "
  "Added facilitated-discussion activities for Topics 1, 2, 4 and 5, a Skills Framework mapping "
  "section, a lab troubleshooting section and an IoT glossary.",C.TRAINER),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Each lab is now a self-contained folder (labs/lab-NN/) holding its instructions plus runnable "
  "Python scripts built on the official iotflow client, so learners can repeat every lab after "
  "the course. Updated the standalone-copy references in each lab section to the new paths.",
  C.TRAINER),
])
prodoc.add_toc(doc)

def code_para(text):
    for line in text.split("\n"):
        para=doc.add_paragraph(); prodoc._shade_para(para) if hasattr(prodoc,"_shade_para") else None
        r=para.add_run(line); r.font.name="Consolas"; r.font.size=Pt(9.5); r.font.color.rgb=INKCODE

for kind,*rest in B:
    if kind=="h1": doc.add_heading(rest[0],level=1)
    elif kind=="h2": doc.add_heading(rest[0],level=2)
    elif kind=="h3":
        para=doc.add_paragraph(); r=para.add_run(rest[0]); r.bold=True; r.font.size=Pt(11); r.font.color.rgb=BRAND
    elif kind=="p": doc.add_paragraph(rest[0])
    elif kind=="bullets":
        for x in rest[0]: doc.add_paragraph(x,style="List Bullet")
    elif kind=="steps":
        for i,(instr,cmd) in enumerate(rest[0],1):
            para=doc.add_paragraph(style="List Number"); para.add_run(instr)
            if cmd: code_para(cmd)
    elif kind=="code": code_para(rest[0])
    elif kind=="note":
        para=doc.add_paragraph(); r=para.add_run("Note: "); r.bold=True; r.font.color.rgb=BRAND
        para.add_run(rest[0]).font.size=Pt(10)
    elif kind=="rule": doc.add_paragraph("")
    elif kind=="image":
        ipath=os.path.join(IMG,rest[0])
        if os.path.exists(ipath):
            from docx.shared import Inches as _In
            doc.add_picture(ipath,width=_In(6.0))
            doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
            cap=doc.add_paragraph(); cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
            cr=cap.add_run(rest[1]); cr.italic=True; cr.font.size=Pt(9); cr.font.color.rgb=GREY
    elif kind=="dl":
        for term,defn in rest[0]:
            para=doc.add_paragraph(style="List Bullet")
            r=para.add_run(term+" — "); r.bold=True; para.add_run(defn)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
DOCX_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.docx")
doc.save(DOCX_OUT)
print("Saved",DOCX_OUT)
