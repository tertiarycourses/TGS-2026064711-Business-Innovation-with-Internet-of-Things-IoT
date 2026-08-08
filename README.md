# IoT with Raspberry Pi — WSQ Courseware

**WSQ Course Code:** TGS-2020505433
**TSC:** EVS-TEM-4002-1.1 — Internet of Things Management (Level 4)
**Duration:** 2 days · 16 training hours (+ 2 hours assessment)
**Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)

Courseware for the WSQ course *IoT with Raspberry Pi* — previously delivered as
*Mastering Raspberry Pi: Hands-On Practical Applications for Beginners*. Every
hands-on lab now runs on **IoTFlow**, our open-source IoT platform
([iot.tertiaryinfotech.com](https://iot.tertiaryinfotech.com) ·
[source](https://github.com/alfredang/iotplatform)), replacing the legacy
ThingSpeak / MATLAB / Node-RED / Adafruit IO / IFTTT lab set.

---

## Learning outcomes

| | Outcome | TSC |
|---|---|---|
| **LO1** | Analyse the uses and functions of IoT technologies | A1, K1 |
| **LO2** | Collect environment data with Raspberry Pi and post it to cloud computing | A2, K2, K3 |
| **LO3** | Use cloud computing to analyse and visualise IoT data | A3, K4, K5 |
| **LO4** | Monitor data and trigger control on devices | A4, K6, K7 |

## Topics

| Topic | Title | Day |
|---|---|---|
| 1 | Overview of Internet of Things (IoT) | 1 |
| 2 | Collect and Post Environmental Data to Cloud | 1 |
| 3 | IoT Data Analytics and Visualization | 2 |
| 4 | Monitor Data to Trigger Control from Cloud | 2 |

## Hands-on labs

All four labs run on [IoTFlow](https://iot.tertiaryinfotech.com) with a Raspberry Pi
and a Sense HAT or DHT11/DHT22 sensor (simulated readings work too).

| Lab | Title | Topic |
|---|---|---|
| 1 | [Register Your Raspberry Pi on IoTFlow](labs/lab-01-register-your-raspberry-pi-on-iotflow.md) | 2 |
| 2 | [Collect Environmental Data and Post It to the Cloud](labs/lab-02-collect-environmental-data-and-post-it-to-the-cloud.md) | 2 |
| 3 | [Analyse and Visualise Your IoT Data on the Cloud](labs/lab-03-analyse-and-visualise-your-iot-data-on-the-cloud.md) | 3 |
| 4 | [Monitor Data and Trigger Control on the Raspberry Pi](labs/lab-04-monitor-data-and-trigger-control-on-the-raspberry-pi.md) | 4 |

---

## Repository layout

```
courseware/          the built artifacts
  IoT with Raspberry Pi-v15.0.pptx / .pdf   trainer slide deck (116 slides)
  LP-IoT with Raspberry Pi.docx / .pdf      Lesson Plan
  LG-IoT with Raspberry Pi.docx / .pdf      Learner Guide
LG-IoT with Raspberry Pi.md                 Markdown mirror of the Learner Guide
labs/                the four hands-on labs, one Markdown file each
assets/              diagrams and platform screenshots used by the deck and LG
build/               the single-source build pipeline
archive/             superseded versions
```

## Building

Everything is generated from **one source of truth** —
`build/course_data.py` plus `build/data_domain1..5.py` — so the deck, Lesson Plan,
Learner Guide and labs can never drift apart.

```bash
cd build
./build_courseware.sh
```

The script builds the deck, LP, LG (DOCX + Markdown), the labs and the assessment,
renders the PDFs, injects page-numbered tables of contents, and re-renders.
Requires Python 3 with `python-pptx`, `python-docx`, `pypdf` and `Pillow`, plus
LibreOffice (`soffice`) for the PDF conversion.

### Design rules enforced by the build

- **No step-by-step instructions in the slide deck.** Lab slides show only the
  purpose, what the learner builds and why it matters; the numbered steps and
  commands live solely in the Learner Guide and `labs/*.md`.
- **Highly visual slides** — tile grids, flow diagrams, cards, stat bands and
  screenshots instead of bullet walls.
- The build **fails loudly** on a missing image or an unassessed K/A code rather
  than silently shipping a blank slide or an incomplete paper.

## Assessment

The assessment set (Written Assessment + Practical Performance, question papers
and answer keys) is **confidential** and is deliberately **not** in this
repository — it is distributed through Google Drive and the LMS only. The
assessment builder is git-ignored for the same reason.

---

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. ·
[www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)
