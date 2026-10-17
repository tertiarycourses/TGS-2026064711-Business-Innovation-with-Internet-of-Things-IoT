# WSQ — Business Innovation with Internet-of-Things (IoT)

**WSQ Course Reference:** `TGS-2026064711`
**TSC:** Business Innovation — `ICT-SNA-4003-1.1` (Level 4), Skills Framework for Infocomm Technology
**Duration:** 1 day · 8 training hours
**Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)

[**Register for this course →**](https://www.tertiarycourses.com.sg/casl-business-innovation-with-internet-of-things-iot.html)

**Funding:** up to 70% course-fee funding for eligible learners and SMEs. Eligibility and terms apply — see the registration page.

Courseware for a one-day WSQ course on identifying, evaluating and implementing business
innovation opportunities using the Internet of Things. The course is deliberately
business-led rather than device-led: learners spend the day building a case they could
actually pitch, and prove the technology to themselves in a 90-minute hands-on block on
the [IoTFlow](https://iot.tertiaryinfotech.com) cloud platform.

---

## Learning outcomes

| # | Outcome | TSC |
|---|---|---|
| LO1 | Compare the organisation's current business model with emerging IoT-enabled business models in the industry | A1, K1 |
| LO2 | Explore potential opportunities for business innovation using IoT across industry use cases | A2, K1 |
| LO3 | Identify how IoT works and the ways digitisation can be applied to the business | A3, K2 |
| LO4 | Conduct a feasibility analysis and weigh the costs and benefits of adopting IoT | A4, K3 |
| LO5 | Implement business innovation processes with IoT in line with a defined action plan | A5, K4 |

## Course outline

| Topic | Content | Delivery |
|---|---|---|
| 1 — Overview of IoT | Industry 4.0, the four building blocks, sensors and actuators, wireless technologies, IoT business models | Lecture + discussion |
| 2 — Potential Opportunities | Use cases across agriculture, autonomous vehicles, logistics, smart buildings, healthcare and drones | Lecture + discussion |
| 3 — IoT Technology | Cloud platforms, uplink/downlink, dashboards, analytics and automation | Lecture + **4 hands-on labs** |
| 4 — IoT Adoption | Adoption barriers, IoT security, the Mirai botnet, edge vs cloud, cost-benefit analysis | Lecture + discussion |
| 5 — IoT Implementation | Six success factors, design thinking, a 7-step action plan | Lecture + discussion |

The training day runs 9:30am–6:30pm and is split as **5.0 h classroom facilitation +
1.5 h practical + 1.5 h assessment** (480 training minutes excluding a one-hour lunch),
per the approved course proposal. The Lesson Plan builder asserts this split, so the
schedule cannot silently drift out of alignment.

## Hands-on labs

All four labs run on **IoTFlow** — <https://iot.tertiaryinfotech.com>. Hardware is
optional: every lab can be completed from a browser and a terminal with cURL or Python.

Each lab is its own folder — `README.md` holds the instructions and the `.py` files
beside it are runnable scripts built on the official
[`iotflow`](https://pypi.org/project/iotflow/) Python client.

| Lab | Title | What the learner builds | Scripts |
|---|---|---|---|
| 1 | [Register Your First IoT Device on IoTFlow](labs/lab-01/README.md) | A registered device in your own project, with its device token saved | `verify_device.py` |
| 2 | [Post Business Data to the Cloud (HTTP & MQTT)](labs/lab-02/README.md) | Live telemetry streaming in from terminal and Python | `send_telemetry_http.py`, `send_telemetry_mqtt.py` |
| 3 | [Read Data Back and Remotely Control the Asset](labs/lab-03/README.md) | A dashboard switch and slider driving a relay/LED in real time | `read_state.py`, `control_http.py`, `control_mqtt.py` |
| 4 | [Turn IoT Data into Business Insight](labs/lab-04/README.md) | A dashboard plus an alert-driven n8n workflow with an AI summary | `simulate_breach.py`, `closed_loop.py` |

Learners set up once, then every script picks up their credentials:

```bash
cd labs
pip install -r requirements.txt   # installs iotflow[mqtt]
cp config.example.py config.py    # paste the device token from Lab 1
```

`labs/config.py` holds a live device token and is git-ignored, so it is never committed.
HTTP-mode scripts run on the Python standard library alone; only the MQTT scripts need
the `[mqtt]` extra.

Each lab is framed around the business decision it enables, not just the wiring — which
is what ability **A3** ("identify ways in which digitisation can be applied to the
business") is assessed on. See the [labs index](labs/README.md).

## Repository layout

```
courseware/                    Built deliverables (one live version only)
  Business Innovation with IoT-v10.1.pptx / .pdf    Slide deck — 100 slides
  LG-Business Innovation with IoT.docx / .pdf / .md Learner Guide (+ Markdown mirror)
  LP-Business Innovation with IoT.docx / .pdf       Lesson Plan
labs/                          4 IoTFlow labs — one folder each, + index
  README.md                    Labs index and one-time setup
  requirements.txt             iotflow[mqtt] — the only dependency
  config.example.py            Copy to config.py and paste your device token (git-ignored)
  lab-01/  README.md + verify_device.py
  lab-02/  README.md + send_telemetry_http.py, send_telemetry_mqtt.py
  lab-03/  README.md + read_state.py, control_http.py, control_mqtt.py
  lab-04/  README.md + simulate_breach.py, closed_loop.py
assets/                        Diagrams and platform screenshots used by the deck and guide
.claude/skills/courseware-build/build/
  course_data.py               SINGLE SOURCE OF TRUTH — metadata, outcomes, topics, discussions
  data_domain1.py … 5.py       Slide content, one module per topic (labs live in domain 3)
  build_slides.py              → the deck
  build_lesson_plan.py         → the Lesson Plan
  build_learner_guide.py       → the Learner Guide (DOCX + Markdown)
  build_labs.py                → labs/lab-NN/README.md and the labs index
  build_courseware.sh          Orchestrator: generate → PDF → inject TOC → re-render
  inject_toc.py, prodoc.py     Word TOC field injection and shared DOCX helpers
  *.example.py                 Course-agnostic templates for starting a new course
```

The lab **instructions** are generated from `data_domain3.py`; the lab **Python scripts**
are hand-written and verified against the real `iotflow` package, so `build_labs.py`
rewrites each `README.md` and lists whatever scripts it finds beside it without
overwriting them.

## Rebuilding the courseware

Every artifact is generated from one content module, so the deck, Lesson Plan, Learner
Guide and labs can never drift apart. Edit `course_data.py` (and `data_domain3.py` for
the labs), then:

```bash
bash .claude/skills/courseware-build/build/build_courseware.sh   # deck + LP + LG + PDFs
python3 .claude/skills/courseware-build/build/build_labs.py      # labs/*.md + index
```

Requires Python 3 with `python-pptx`, `python-docx` and `Pillow`, plus LibreOffice
(`soffice`) on the PATH for PDF rendering.

### Publishing to Drive and the LMS

Built artifacts are published to the course's Google Drive folder and then linked from the
course record on `lms-tms.tertiaryinfotech.com`:

```bash
python3 .claude/skills/gdrive-push/gdrive_push.py --repo . --dry-run   # preview, then drop --dry-run
python3 .claude/skills/lms-push/lms_push.py --repo .                   # write the Drive links onto the course
```

Neither step needs the folder link typed out. The destination resolves in order from an
explicitly passed link, then the course's **Courseware Link** on LMS-TMS, then
`COURSEWARE_LINK` in the course `.env` — which every real push writes back, so a later run
still works when the LMS API is unreachable. The lookup is keyed on the `TGS-` code read
out of the courseware itself, and a passed link that disagrees with the reference link is
**refused** unless `--force-folder`, so one course's material cannot land in another
course's folder. Superseded Drive files are moved to `archive/`; nothing is ever deleted.

The LMS API authenticates machine callers with a service key in the `x-api-key` header,
read from `LMS_TMS_API_KEY` in the environment, `./.claude/lms_tms_api_key`, or
`~/.claude/lms_tms_api_key`. That key and the `.env` are credentials — both are git-ignored
and neither is ever committed.

### Slide deck conventions

- **No step-by-step slides.** The deck shows each lab's purpose, what the learner builds
  and why the business cares; every numbered command lives only in the Learner Guide.
- **Visual over textual.** Tile grids, chevron flow diagrams, profile cards, stat bands
  and real platform screenshots instead of bullet walls.

## Assessment

Assessment materials are **confidential and are not published in this repository.** The
question papers and answer keys are held on Google Drive and released through the LMS to
authorised trainers and assessors only.

Per the approved Assessment Plan, this course uses two instruments — note that the
written paper covers the **abilities** and the oral covers the **knowledge**, which is
the inverse of the more common arrangement:

| Instrument | Duration | Ratio | Covers |
|---|---|---|---|
| Written Assessment (Q&A) | 75 min | 1:10 | Abilities **A1–A5** |
| Oral Questioning (OQ) | 15 min | 1:1 | Knowledge **K1–K4** |

Both are open book. A minimum 75% attendance is required to be eligible for assessment
and funding.

---

## Licence and attribution

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.
Course materials are provided for enrolled learners and authorised trainers.

**Powered by [Tertiary Infotech Academy Pte Ltd](https://www.tertiaryinfotech.com/)** ·
[www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)
