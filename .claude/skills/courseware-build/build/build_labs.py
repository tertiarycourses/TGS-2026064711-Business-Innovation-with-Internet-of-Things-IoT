#!/usr/bin/env python3
"""Generate the standalone labs/ folders + labs/README.md index from the same
single source (course_data.py + data_domainN.py) that drives the deck, LP and
LG, so a lab can never drift from the guide.

One FOLDER per activity: labs/lab-NN/README.md, alongside the hand-written
Python scripts for that lab (labs/lab-NN/*.py). The scripts are NOT generated —
they are maintained by hand and verified against the real `iotflow` package —
so this generator only ever rewrites README.md and lists whatever scripts it
finds next to it.
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

def scripts_in(folder):
    """The hand-written Python scripts for a lab, in a stable order."""
    if not os.path.isdir(folder): return []
    return sorted(f for f in os.listdir(folder)
                  if f.endswith(".py") and f != "config.py")

def docstring_summary(path):
    """First SENTENCE of a script's 'WHAT THIS SCRIPT DOES' block, for the table.

    The block is wrapped over several indented lines, so join it back into one
    paragraph before cutting at the first full stop — otherwise the table cell
    ends mid-sentence.
    """
    try:
        with open(path) as f: src=f.read(4000)
    except OSError: return ""
    m=re.search(r"WHAT THIS SCRIPT DOES\s*\n((?:[ \t]+.*\n)+)", src)
    if not m: return ""
    para=" ".join(l.strip() for l in m.group(1).splitlines() if l.strip())
    # Cut at the first sentence end that is not a decimal point or abbreviation.
    s=re.split(r"(?<=[.!?])\s+(?=[A-Z])", para)[0].strip()
    return s.replace("|","\\|")

written=[]
for a in ACT:
    t=TOPICS[a["topic"]]
    folder=os.path.join(LABS,f"lab-{a['num']:02d}")
    os.makedirs(folder,exist_ok=True)
    name=f"lab-{a['num']:02d}/README.md"
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
        # Screenshots live in <repo>/assets/; each lab README is two folders
        # deep (labs/lab-NN/README.md), so climb two levels to reach them.
        L.append(f"![{C.PLATFORM} — Lab {a['num']}](../../assets/{a['image']})\n")
    if a.get("business"):
        L.append("## Why the business cares\n")
        L.append(a["business"]+"\n")
    L.append("## Prerequisites\n")
    L.append(f"- A free account on {C.PLATFORM} ({C.PLATFORM_URL}).")
    L.append("- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be "
             "completed with cURL or Python from any terminal.")
    if a["num"]>1:
        L.append("- Your device token from Lab 1 (`dev_...`).")
    L.append("- Python 3 for the scripted steps — see Setup below.\n")

    # ---- setup + the hand-written scripts that ship with this lab ----
    sc=scripts_in(folder)
    if sc:
        L.append("## Setup (once for all labs)\n")
        L.append("```bash")
        L.append('pip install -r ../requirements.txt   # installs iotflow[mqtt]')
        L.append("cp ../config.example.py ../config.py  # then paste your device token")
        L.append("```\n")
        L.append(f"`config.py` holds your device token, so you paste it once and every "
                 f"lab script picks it up. It is git-ignored and never committed.\n")
        L.append("## Scripts in this folder\n")
        L.append("| Script | What it does |")
        L.append("|---|---|")
        for s in sc:
            L.append(f"| [`{s}`]({s}) | {docstring_summary(os.path.join(folder,s))} |")
        L.append("")
        L.append("Run them from inside this folder, e.g.:\n")
        L.append("```bash")
        L.append(f"cd lab-{a['num']:02d}")
        L.append(f"python {sc[0]}")
        L.append("```\n")

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
idx.append(f"All labs run on our IoT platform **{C.PLATFORM}** — {C.PLATFORM_URL} — and are completed "
           f"during the 90-minute practical block in Topic 3. Work through them in order; each lab "
           f"builds on the one before.\n")
idx.append("Full step-by-step instructions are also in the Learner Guide. The slide deck shows each "
           "lab's purpose and outcome only.\n")
idx.append("Each lab is a folder: `README.md` has the instructions, and the `.py` files next to it "
           f"are runnable {C.PLATFORM} scripts built on the official `iotflow` Python package.\n")
idx.append("## Setup (once, before Lab 1)\n")
idx.append("```bash")
idx.append("pip install -r requirements.txt   # installs iotflow[mqtt]")
idx.append("cp config.example.py config.py    # paste your device token from Lab 1")
idx.append("```\n")
idx.append("`config.py` is git-ignored — your device token never leaves your machine. "
           "HTTP-mode scripts need no third-party package at all; only the MQTT scripts "
           "need the `[mqtt]` extra.\n")
by_topic={}
for a,name in written: by_topic.setdefault(a["topic"],[]).append((a,name))
for tn in sorted(by_topic):
    t=TOPICS[tn]
    idx.append(f"## Topic {t['code']} — {t['title']}  ({t['weighting']})\n")
    for a,name in by_topic[tn]:
        sc=scripts_in(os.path.join(LABS,f"lab-{a['num']:02d}"))
        extra=f"  \n  Scripts: {', '.join(f'`{s}`' for s in sc)}" if sc else ""
        idx.append(f"- [Lab {a['num']}: {a['title']}]({name}) — {a['build']}{extra}")
    idx.append("")
idx.append(FOOTER)
with open(os.path.join(LABS,"README.md"),"w") as f: f.write("\n".join(idx))
print("Saved",os.path.join(LABS,"README.md"))
print(f"{len(written)} lab file(s) generated.")
