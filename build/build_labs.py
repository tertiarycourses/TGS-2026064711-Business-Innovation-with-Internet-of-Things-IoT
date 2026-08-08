#!/usr/bin/env python3
"""Generate the standalone labs/ markdown files + labs/README.md index from the
same single source (course_data.py + data_domainN.py) that drives the deck, LP
and LG, so a lab can never drift from the guide.

One file per activity: labs/lab-NN-<slug>.md
"""
import os, re, sys

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)
LABS=os.path.join(REPO,"labs")
os.makedirs(LABS,exist_ok=True)

TOPICS={t["num"]:t for t in C.TOPICS}
FOOTER=f"---\n*© 2026 {C.ORG}. All rights reserved. · www.tertiarycourses.com.sg*\n"

def slug(s):
    s=s.lower()
    s=re.sub(r"[^a-z0-9]+","-",s)
    return re.sub(r"-+","-",s).strip("-")

written=[]
for a in ACT:
    t=TOPICS[a["topic"]]
    name=f"lab-{a['num']:02d}-{slug(a['title'])}.md"
    L=[]
    L.append(f"# Lab {a['num']} — {a['title']}\n")
    L.append(f"**Course:** {C.TITLE} ({C.COURSE_CODE})  ")
    L.append(f"**Topic {t['code']}:** {t['title']}  ")
    L.append(f"**Objective:** {a['objective']}  ")
    L.append(f"**Platform:** {C.PLATFORM} — {C.PLATFORM_URL}\n")
    L.append("## Goal\n")
    L.append(a["desc"]+"\n")
    L.append("## What you'll build\n")
    L.append(a["build"]+"\n")
    L.append(f"*Uses: {a['services']}.*\n")
    if a.get("image"):
        L.append(f"![{C.PLATFORM} — Lab {a['num']}](../courseware/assets/{a['image']})\n")
    if a.get("business"):
        L.append("## Why the business cares\n")
        L.append(a["business"]+"\n")
    L.append("## Prerequisites\n")
    L.append(f"- A free account on {C.PLATFORM} ({C.PLATFORM_URL}).")
    L.append("- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be "
             "completed with cURL or Python from any terminal.")
    if a["num"]>1:
        L.append("- Your device token from Lab 1 (`dev_...`).")
    L.append("- Optional, for the scripted steps: Python 3 with `pip install \"iotflow[mqtt]\"`.\n")
    L.append("## Step-by-step\n")
    for i,(instr,cmd) in enumerate(a["steps"],1):
        L.append(f"### Step {i} — {instr}\n")
        if cmd:
            L.append("```bash")
            L.append(cmd)
            L.append("```\n")
    L.append("## Test it\n")
    L.append(a["test"]+"\n")
    L.append(FOOTER)
    path=os.path.join(LABS,name)
    with open(path,"w") as f: f.write("\n".join(L))
    written.append((a,name))
    print("Saved",path)

# ---- index ----
idx=[f"# Hands-On Labs — {C.TITLE}\n"]
idx.append(f"**WSQ Course Code:** {C.COURSE_CODE} · Conducted by {C.ORG} ({C.UEN.replace('UEN: ','UEN ')})\n")
_lab_topics=sorted({a["topic"] for a in ACT})
_span=(f"Topics {_lab_topics[0]}–{_lab_topics[-1]}" if len(_lab_topics)>1 else f"Topic {_lab_topics[0]}")
idx.append(f"All labs run on our IoT platform **{C.PLATFORM}** — {C.PLATFORM_URL} — and are completed "
           f"across {_span} (300 minutes of practical time over {C.DAYS} days). Work through them in "
           f"order; each lab builds on the one before.\n")
idx.append("Full step-by-step instructions are also in the Learner Guide. The slide deck shows each "
           "lab's purpose and outcome only.\n")
by_topic={}
for a,name in written: by_topic.setdefault(a["topic"],[]).append((a,name))
for tn in sorted(by_topic):
    t=TOPICS[tn]
    idx.append(f"## Topic {t['code']} — {t['title']}  ({t['weighting']})\n")
    for a,name in by_topic[tn]:
        idx.append(f"- [Lab {a['num']}: {a['title']}]({name}) — {a['build']}")
    idx.append("")
idx.append(FOOTER)
with open(os.path.join(LABS,"README.md"),"w") as f: f.write("\n".join(idx))
print("Saved",os.path.join(LABS,"README.md"))
print(f"{len(written)} lab file(s) generated.")
