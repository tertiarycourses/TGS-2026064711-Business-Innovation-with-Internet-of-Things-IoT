# Business Innovation with Internet-of-Things (IoT) — Learner Guide

**WSQ Course Code:** TGS-2026064711  |  **Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)  |  **Version v10.0 · 8 August 2026**

## Contents

- [Introduction](#introduction)
- [Course Learning Outcomes](#course-learning-outcomes)
- [How This Course Is Assessed](#how-this-course-is-assessed)
- [Skills Framework Mapping](#skills-framework-mapping)
- [Before You Start — Setting Up for the Hands-On Labs](#before-you-start--setting-up-for-the-hands-on-labs)
- [Topic 01 — Overview of Internet of Things (IoT)  (LO1 · A1, K1 · 60 min)](#topic-01--overview-of-internet-of-things-iot--lo1--a1-k1--60-min)
  - [Activity — Discussion — Compare Business Models  (15 minutes)](#activity--discussion--compare-business-models--15-minutes)
- [Topic 02 — Potential Opportunities of IoT Innovation  (LO2 · A2, K1 · 60 min)](#topic-02--potential-opportunities-of-iot-innovation--lo2--a2-k1--60-min)
  - [Activity — Discussion — Spot an IoT Opportunity  (15 minutes)](#activity--discussion--spot-an-iot-opportunity--15-minutes)
- [Topic 03 — IoT Technology  (LO3 · A3, K2 · 60 min + 90 min practical)](#topic-03--iot-technology--lo3--a3-k2--60-min--90-min-practical)
  - [Lab 1 — Register Your First IoT Device on IoTFlow](#lab-1--register-your-first-iot-device-on-iotflow)
  - [Lab 2 — Post Business Data to the Cloud (HTTP & MQTT)](#lab-2--post-business-data-to-the-cloud-http--mqtt)
  - [Lab 3 — Read Data Back and Remotely Control the Asset](#lab-3--read-data-back-and-remotely-control-the-asset)
  - [Lab 4 — Turn IoT Data into Business Insight](#lab-4--turn-iot-data-into-business-insight)
- [Topic 04 — IoT Adoption  (LO4 · A4, K3 · 60 min)](#topic-04--iot-adoption--lo4--a4-k3--60-min)
  - [Activity — Discussion — Cost-Benefit Analysis  (20 minutes)](#activity--discussion--cost-benefit-analysis--20-minutes)
- [Topic 05 — IoT Implementation  (LO5 · A5, K4 · 60 min)](#topic-05--iot-implementation--lo5--a5-k4--60-min)
  - [Activity — Discussion — Your Implementation Action Plan  (20 minutes)](#activity--discussion--your-implementation-action-plan--20-minutes)
- [Putting It Together — From Opportunity to Action Plan](#putting-it-together--from-opportunity-to-action-plan)
- [Troubleshooting the Labs](#troubleshooting-the-labs)
- [Glossary](#glossary)


## Introduction

This Learner Guide accompanies the WSQ course Business Innovation with Internet-of-Things (IoT) (TGS-2026064711), conducted by Tertiary Infotech Academy Pte Ltd. It is a one-day (8-hour) course mapped to the Skills Framework for Infocomm Technology TSC Business Innovation (ICT-SNA-4003-1.1, Level 4).

The course answers a business question, not only a technical one: where can the Internet of Things create value in your organisation, and how would you justify and implement it? Topics 1, 2, 4 and 5 build the business case through facilitated discussion. Topic 3 is hands-on — you will connect a device to the cloud yourself on IoTFlow (https://iot.tertiaryinfotech.com) so that the technology is concrete rather than abstract.

This guide contains the full step-by-step instructions for every lab. The slide deck deliberately shows only each lab's purpose and outcome, so follow the numbered steps here while the trainer demonstrates. Keep this guide with you during the assessment — it is open book.


## Course Learning Outcomes

On completion of this course, you will be able to:

- LO1: Compare the organisation's current business model with emerging IoT-enabled business models in the industry. (A1, K1)
- LO2: Explore potential opportunities for business innovation using IoT across industry use cases. (A2, K1)
- LO3: Identify how IoT works and the ways digitisation can be applied to the business. (A3, K2)
- LO4: Conduct a feasibility analysis and weigh the costs and benefits of adopting IoT. (A4, K3)
- LO5: Implement business innovation processes with IoT in line with a defined action plan. (A5, K4)


## How This Course Is Assessed

The assessment has two instruments, both open book, conducted at the end of the training day:

- Written Assessment (WA) — Short-Answer Questions (Q&A), 75 minutes, open book. Covers A1–A5.
- Oral Questioning (OQ) — 15 minutes, 1:1 with the assessor, open book. Covers K1–K4.
- Open book means you may refer to the course slides, this Learner Guide and any approved materials.
- A minimum of 75% attendance is required to be eligible for assessment and funding.
- An appeal process is available if you disagree with the assessment outcome.

The Written Assessment covers the five abilities (A1–A5) and the Oral Questioning covers the four knowledge statements (K1–K4). Each topic in this guide is labelled with the ability and knowledge it develops, so you can see exactly what each session is preparing you for.


## Skills Framework Mapping

**Abilities — assessed by the Written Assessment**

- A1 — Compare current business model for the organisation with the other business models in the industry
- A2 — Explore potential opportunities for business innovation to be introduced within the organisation
- A3 — Identify ways in which digitisation can be applied to the business
- A4 — Conduct feasibility analysis and weigh the costs-benefits of potential business innovation opportunities
- A5 — Implement business innovation processes in line with a defined action plan

**Knowledge — assessed by Oral Questioning**

- K1 — New and emerging innovative business processes / models deployed in the industry
- K2 — Concept and principles of digitisation
- K3 — Factors to consider to assess the viability of business innovation for a given organisation context
- K4 — Success factors for implementation of business innovation


## Before You Start — Setting Up for the Hands-On Labs

**What you need**

- A free learner account on IoTFlow — https://iot.tertiaryinfotech.com. Sign up with your email; no credit card is required.
- A laptop with a modern web browser. Every lab can be completed from the browser and a terminal.
- A terminal with cURL available (built into macOS, Linux and Windows 10+).
- Optional — Python 3 with the official client: pip install "iotflow[mqtt]" for the scripted labs.
- Optional — IoT hardware (ESP32 or ESP8266) if you want to send readings from a real sensor. The Arduino library speaks the same protocol as the Python client, so the platform cannot tell the difference.

**Create your account and project**

Open https://iot.tertiaryinfotech.com, sign up, then create a project. A project is a self-contained workspace with its own devices, dashboard, alerts, map and automations. Name it after a business scenario you care about — for example Cold Chain Monitoring, Smart Office or Workshop Machine Health. Using a real scenario makes the discussions in Topics 4 and 5 much more productive.

```bash
Open https://iot.tertiaryinfotech.com  ->  Sign up  ->  Log in  ->  New project
```

**Conventions used in every lab**

- Placeholders in CAPITALS or angle brackets are replaced with your own values — dev_XXXXXXXXXXXX is your device token and <id> is your device id.
- Your device token is shown only once when the device is created. Save it somewhere safe before closing the dialog.
- Commands prefixed with a $ are run in your terminal; Python snippets are run in a .py file or an interactive session.
- Dashboard widgets refresh automatically about every 5 seconds, so allow a moment for a new reading to appear.
- If a step fails, check the token first — an expired or mistyped token is by far the most common cause.

> **Note:** Treat your device token like a password. Anyone who holds it can post data as your device. This is exactly the credential-management problem discussed in Topic 4 on IoT security.


## Topic 01 — Overview of Internet of Things (IoT)  (LO1 · A1, K1 · 60 min)

Industry 4.0 · IoT business models · Sensors & actuators · Wireless technologies

**Key concepts**

- Industry 4.0 — IoT, AI, 5G, cloud and robotics converge so physical assets report their own state in real time.
- What IoT is — Connecting everyday objects to the internet to cut cost, lift productivity and open new revenue.
- The four building blocks — Sensors/devices capture data, connectivity moves it, cloud processes it, a UI acts on it.
- Why now — Cheap sensors, long-range low-power wireless and 5G removed the cost barrier to mass adoption.
- Product to service — IoT shifts firms from one-off product sales to subscription, outcome and pay-per-use models.
- Data as the asset — The recurring value is the telemetry stream, not the device — it compounds over time.


### Activity — Discussion — Compare Business Models  (15 minutes)

In pairs, describe how your organisation earns revenue today. Then pick one IoT-enabled competitor or industry example and compare the two.

**Discussion prompts**

- How does your organisation make money today — product sale, project fee, subscription?
- Which IoT-enabled model could apply: outcome-based, pay-per-use, subscription, or predictive service?
- What data would you need to collect before that model becomes possible?
- What would customers gain, and what would they be willing to pay for?

**What to produce**

A short written comparison of your current model against one IoT-enabled model.

> **Note:** Write your answer down as you go. The same reasoning is what the Written Assessment asks you to demonstrate for A1.


## Topic 02 — Potential Opportunities of IoT Innovation  (LO2 · A2, K1 · 60 min)

Agriculture · Autonomous vehicles · Logistics · Smart buildings · Healthcare · Drones

**Key concepts**

- Agriculture — Soil, weather and crop sensing drive precision irrigation and fertiliser decisions — e.g. IBM AgroPad.
- Autonomous vehicles — Vehicle telemetry and sensor fusion enable driver assistance and highly automated driving.
- Logistics & fleet — Location, temperature and fuel telemetry give end-to-end shipment visibility and route optimisation.
- Smart buildings — Occupancy, energy and equipment sensing cut utility cost and enable predictive maintenance.
- Healthcare & wearables — Continuous patient monitoring feeds records securely, supporting earlier clinical intervention.
- Drones — Aerial inspection, survey and delivery reach places people cannot, safely and at lower cost.


### Activity — Discussion — Spot an IoT Opportunity  (15 minutes)

Working from the six industry use cases, identify one process in your own organisation that is currently invisible, manual or reactive, and could be sensed instead.

**Discussion prompts**

- Which process today relies on someone physically checking something?
- What would you measure, how often, and who would act on the reading?
- What is the cost of the current blind spot — downtime, spoilage, overtime, penalties?
- Which of the six use cases is closest to your scenario, and what can you borrow from it?

**What to produce**

One clearly stated IoT opportunity: the asset, the measurement, and the decision it improves.

> **Note:** Write your answer down as you go. The same reasoning is what the Written Assessment asks you to demonstrate for A2.


## Topic 03 — IoT Technology  (LO3 · A3, K2 · 60 min + 90 min practical)

Cloud platforms · Post data · Read & control · Analytics & visualisation · Automation

**Key concepts**

- Cloud for IoT — A platform ingests telemetry, stores history, visualises it and triggers actions — no servers to run.
- IoTFlow — Our platform: projects, devices, tokens, dashboards, alerts and automations in one place.
- Uplink: posting data — Devices POST readings over HTTP REST or publish over MQTT, authenticated by a device token.
- Downlink: control — Virtual pins carry commands from the dashboard back to the device to switch a relay or set a value.
- Analytics & visualisation — Number cards, gauges, charts and maps turn raw readings into an operational picture.
- Automation & AI — Rules and n8n workflows notify, log and let AI summarise readings and recommend an action.


### Lab 1 — Register Your First IoT Device on IoTFlow

Objective: Identify how digitisation is applied to a business asset by connecting it to the cloud (A3, K2).

Goal: Turn a physical asset into a digital one. You sign in to IoTFlow, create a project workspace for your business scenario, register a device through the Add Device wizard, choose how it will talk to the cloud (HTTP or MQTT), and capture the device token that authenticates every message it sends.

**What you'll build**

A registered IoT device in your own IoTFlow project, with its device token saved   (Tools: IoTFlow projects · Add Device wizard · Device tokens · HTTP & MQTT.)

![IoTFlow — Lab 1: Register Your First IoT Device on IoTFlow](courseware/assets/lab-01-add-device.png)

*IoTFlow — Lab 1: Register Your First IoT Device on IoTFlow*

**Why the business cares**

This is the first step of digitisation: an asset that was previously invisible to the business now has an identity, an owner and a data stream that can be measured and managed.

**Step-by-step**

1. Open the IoTFlow platform at https://iot.tertiaryinfotech.com and sign up for a free account, or log in if you already have one.
2. Create a project — a self-contained workspace with its own dashboard, alerts, map and automations. Name it after your business scenario, e.g. 'Cold Chain Monitoring' or 'Smart Office'.
3. Click Add Device in the sidebar and give the device a descriptive, business-meaningful name.

   ```bash
   Device name:  Cold Room Sensor 01
   ```

4. Work through the guided wizard and choose a protocol. HTTP is the simplest — POST JSON to a REST endpoint. MQTT is a lightweight publish/subscribe protocol, better for many devices and real-time control. Both stay available afterwards.
5. Copy the device token shown when the device is created. It is displayed only once — save it somewhere safe.

   ```bash
   dev_XXXXXXXXXXXX
   ```

6. Note how the token authenticates every message the device sends. Anyone holding the token can post as that device, which is exactly why device credential management is an IoT security concern (Topic 4).

   ```bash
   Authorization: Bearer dev_XXXXXXXXXXXX
   ```


**Test it**

Your new device appears in the project's device list, and its Integrate page shows code snippets pre-filled with your endpoint and device token.

> **Note:** A standalone copy of this lab is in labs/lab-01-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


### Lab 2 — Post Business Data to the Cloud (HTTP & MQTT)

Objective: Apply digitisation by streaming operational data from the asset to the cloud (A3, K2).

Goal: Send readings to IoTFlow three different ways — cURL from any terminal, the Python client, and (optionally) an ESP32/ESP8266 over MQTT — and watch them arrive live. This is the uplink that every IoT business case depends on: without a reliable data stream there is nothing to analyse.

**What you'll build**

Live temperature and humidity telemetry streaming into IoTFlow from terminal and Python   (Tools: Telemetry REST API · Python client (pip install iotflow) · MQTT broker · ESP32/ESP8266.)

![IoTFlow — Lab 2: Post Business Data to the Cloud (HTTP & MQTT)](courseware/assets/lab-02-send-reading.png)

*IoTFlow — Lab 2: Post Business Data to the Cloud (HTTP & MQTT)*

**Why the business cares**

Each reading is an operational fact with a timestamp. Once the stream exists, the business can ask questions it previously could not answer — how often, how long, how bad, and at what cost.

**Step-by-step**

1. Open the Integrate page for your device. Every snippet on it is pre-filled with your endpoint and device token.
2. Send your first reading from any terminal with cURL over HTTP POST.

   ```bash
   curl -X POST https://iot.tertiaryinfotech.com/api/telemetry \
  -H "Authorization: Bearer dev_XXXXXXXXXXXX" \
  -H "Content-Type: application/json" \
  -d '{"temperature": 22.5, "humidity": 60}'
   ```

3. Open the Dashboard. The reading appears under Latest Telemetry within seconds — widgets auto-refresh every 5 seconds.
4. Install the official IoTFlow Python client from PyPI.

   ```bash
   pip install "iotflow[mqtt]"      # with real-time MQTT (paho-mqtt)
pip install iotflow               # HTTP only — zero dependencies
   ```

5. Send readings from Python over HTTP — several metrics at once with send(), or one at a time with virtual_write().

   ```bash
   from iotflow import IoTFlow

iot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "cold-room-sensor-01")
iot.send(temperature=22.5, humidity=60)      # several metrics at once
iot.virtual_write("temperature", 22.5)       # or one at a time
   ```

6. Stream continuously over MQTT with the telemetry_upload.py example — download it, fill in your broker host, device id and device token, then run it.

   ```bash
   curl -O https://raw.githubusercontent.com/alfredang/iotplatform/main/clients/python/examples/telemetry_upload.py
# edit: MQTT_BROKER = "iot.tertiaryinfotech.com", DEVICE_ID, DEVICE_TOKEN
python telemetry_upload.py
   ```

7. Study the loop inside telemetry_upload.py — connect() runs MQTT in the background and mqtt_publish() sends a reading every 10 seconds. This is the shape of a real production sensor.

   ```bash
   iot = IoTFlow(token=DEVICE_TOKEN, device_id=DEVICE_ID,
              mqtt_host=MQTT_BROKER, mqtt_port=MQTT_PORT)
iot.connect()                    # MQTT runs in the background
while True:
    iot.mqtt_publish(temperature=temperature, humidity=humidity, voltage=3.7)
    time.sleep(PUBLISH_INTERVAL_S)
   ```

8. Hardware alternative (optional): flash the ESP8266_Telemetry_Upload Arduino sketch. The Arduino library speaks the same protocol as the Python client, so the dashboard cannot tell the difference.

   ```bash
   IoTFlow.virtualWrite("temperature", t);   // metric name binds to dashboard widgets
   ```


**Test it**

Every value you send appears in the Dashboard's Latest Telemetry within seconds, and the device's telemetry history grows with each reading.

> **Note:** A standalone copy of this lab is in labs/lab-02-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


### Lab 3 — Read Data Back and Remotely Control the Asset

Objective: Close the loop between cloud data and physical action — the basis of an IoT business process (A3, K2).

Goal: Read device state back out of the cloud over the REST API and MQTT, then add Control widgets (switch, slider) bound to virtual pins and drive the device from the dashboard. Reading data is monitoring; sending commands back is automation — and that is where the labour savings appear.

**What you'll build**

A dashboard switch and slider that control a relay/LED on the device in real time   (Tools: REST API (GET /api/device/state) · MQTT subscribe · Control widgets · Virtual pins · @on_command.)

![IoTFlow — Lab 3: Read Data Back and Remotely Control the Asset](courseware/assets/lab-04-control-device.png)

*IoTFlow — Lab 3: Read Data Back and Remotely Control the Asset*

**Why the business cares**

Monitoring tells you what happened. Control lets the system act without a person driving out to the site — this is usually the single largest line in an IoT cost-benefit case.

**Step-by-step**

1. Read your device's latest state from any terminal over the REST API, and inspect the JSON reply — the platform returns the current value of every metric and virtual pin.

   ```bash
   curl https://iot.tertiaryinfotech.com/api/device/state \
  -H "Authorization: Bearer dev_XXXXXXXXXXXX"
   ```

2. Subscribe to your device's MQTT downlink topic to watch commands and data arrive in real time. Note the direction: uplink is telemetry, downlink is commands.

   ```bash
   mosquitto_sub -h iot.tertiaryinfotech.com -p 1883 \
  -u device -P dev_XXXXXXXXXXXX -t "devices/<id>/down" -v
   ```

3. On the Dashboard click Add widget and choose a Control type: Button (momentary), Switch (toggle), Slider (value) or Terminal (text).
4. Assign the virtual pin the widget writes to — for example V1, relay or pump. For a slider also set the min/max range.

   ```bash
   Virtual pin:  V1
   ```

5. React to commands in Python with the iotflow client. Decorate a handler with @iot.on_command and poll over HTTP — no extra dependencies needed.

   ```bash
   from iotflow import IoTFlow

iot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "cold-room-sensor-01")

@iot.on_command
def handle(pin, value, text):
    if pin == "V1":
        print("relay ->", value)      # drive a GPIO here

iot.run(interval=3)                   # blocks, polls every 3 s
   ```

6. For real-time control use the same handler over MQTT — loop_forever() keeps the connection open so commands arrive instantly instead of on the next poll.

   ```bash
   iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="cold-room-sensor-01",
              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)

@iot.on_command
def handle(pin, value, text): ...

iot.loop_forever()
   ```

7. Flip the switch and drag the slider on the dashboard. Commands are delivered to the device immediately and the relay/LED responds. The same events can also trigger automations (Lab 4).

**Test it**

Toggling the dashboard switch changes the relay/LED state within a second, and the slider value arrives in your @on_command handler as you drag it.

> **Note:** A standalone copy of this lab is in labs/lab-03-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


### Lab 4 — Turn IoT Data into Business Insight

Objective: Use analytics, visualisation and automation to turn raw telemetry into a business decision (A3, K2).

Goal: Build a live dashboard from your readings — number cards, gauges, charts, LED indicators and maps — then set a threshold alert and hand it to an n8n workflow that notifies the team, logs the event and asks an AI node to summarise the readings and recommend an action.

**What you'll build**

A monitoring dashboard plus an alert-driven n8n workflow with an AI summary and a downlink command   (Tools: Display widgets · Alert rules · IoTFlow Automations · n8n Webhook · Email/Telegram · Google Sheets · AI nodes.)

![IoTFlow — Lab 4: Turn IoT Data into Business Insight](courseware/assets/lab-05-dashboard.png)

*IoTFlow — Lab 4: Turn IoT Data into Business Insight*

**Why the business cares**

This is the slide the board actually sees. A dashboard makes performance visible, an alert makes it timely, and the AI summary turns a stream of numbers into a recommended action.

**Step-by-step**

1. On the Dashboard click Add widget. Widgets are grouped into Display (show data) and Control (send commands). Add a Number card for temperature and give it a clear title.
2. Add a Gauge for humidity with sensible min/max bounds (0–100 %), then a Line chart to plot the temperature history over time.
3. Add an LED indicator for on/off state, and a Map widget if your device reports a location. Arrange the layout — widgets snap to a responsive grid and refresh automatically.
4. Create an alert rule on a business-meaningful threshold — the point at which someone would need to act.

   ```bash
   Alert rule:  temperature > 30  →  fire automation
   ```

5. In n8n, add a Webhook node to a new workflow, activate the workflow and copy the Production URL.
6. Back in IoTFlow, create an Automation, choose the trigger type (telemetry received, alert fired, device online/offline, or command sent), optionally narrow it by device and metric, then paste the n8n webhook URL and save.
7. Use Test to send a sample payload to n8n and inspect the JSON the webhook receives, then enable live triggering.
8. In n8n, branch the flow: send an Email/Telegram notification and append the reading to Google Sheets so the event is both escalated and recorded.
9. Add an AI node that summarises the recent readings and recommends an action — analytics with no code, and the output a manager can read.
10. Close the loop: add an HTTP Request node that sends a downlink command back to the device, for example switching a fan or compressor on.

   ```bash
   POST https://iot.tertiaryinfotech.com/api/device/command
{ "pin": "V1", "value": 1 }
   ```


**Test it**

Pushing a reading above the threshold fires the n8n workflow: the notification arrives, a row is appended to the sheet, the AI summary is generated, and the device reacts to the command sent back.

> **Note:** A standalone copy of this lab is in labs/lab-04-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


## Topic 04 — IoT Adoption  (LO4 · A4, K3 · 60 min)

Adoption challenges · IoT security · Edge computing · Cost-benefit analysis

**Key concepts**

- Barriers to adoption — Data privacy, security, cost, skills gaps, weak standards and interoperability with legacy systems.
- Why IoT security differs — Constrained devices, long unattended lifetimes and physical consequences to a breach.
- Mirai botnet — Default credentials on cameras and routers built a botnet that took down much of the US east coast.
- Edge computing — Processing near the source cuts latency, bandwidth and cost, and keeps sensitive data local.
- Falling hardware cost — Sensor, gateway and connectivity prices keep dropping, improving the business case each year.
- Cost-benefit analysis — Weigh hardware, connectivity, platform and integration against savings, uptime and new revenue.


### Activity — Discussion — Cost-Benefit Analysis  (20 minutes)

Take the opportunity you identified in Topic 2 and build a first-pass feasibility and cost-benefit case for it, including the security and privacy risks.

**Discussion prompts**

- Costs: devices, connectivity, platform subscription, integration, installation, maintenance.
- Benefits: labour saved, downtime avoided, energy or wastage reduced, new revenue enabled.
- Risks: data privacy, device security, interoperability with legacy systems, skills gaps.
- Roughly how long before the benefits exceed the costs — and what would break that estimate?

**What to produce**

A cost-benefit summary with an estimated payback period and the top three risks.

> **Note:** Write your answer down as you go. The same reasoning is what the Written Assessment asks you to demonstrate for A4.


## Topic 05 — IoT Implementation  (LO5 · A5, K4 · 60 min)

Success factors · Design thinking · A 7-step action plan

**Key concepts**

- Lead with business value — Start from the business outcome IoT delivers, not from the technology itself.
- Strategic alignment — The initiative must serve the business strategy and respect technology constraints.
- Business process focus — Integrate IoT into existing workflows so the new way is clearly better than today.
- Operating model & capability — Value networks and new skills are needed; give people a common IoT language.
- Security by design — Build end-to-end security in from the start — it is a selection criterion, not an add-on.
- Design thinking — Empathise, Define, Ideate, Prototype, Test — start small, prove value, then scale.


### Activity — Discussion — Your Implementation Action Plan  (20 minutes)

Apply design thinking and the success factors to turn your opportunity into a staged action plan you could actually pitch to management.

**Discussion prompts**

- Empathise & Define: whose problem is this, and how would you state it in one sentence?
- Ideate & Prototype: what is the smallest pilot that proves the value — one device, one site?
- Test & scale: what measurable result would justify rolling it out further?
- Which success factor is weakest in your organisation today, and how will you address it?

**What to produce**

A staged action plan: pilot scope, success measure, owner, and the case for scaling.

> **Note:** Write your answer down as you go. The same reasoning is what the Written Assessment asks you to demonstrate for A5.


## Putting It Together — From Opportunity to Action Plan

By the end of the day you should be able to carry one idea through the whole arc of the course. This is the reasoning the assessment is built around:

1. Compare your current business model with an IoT-enabled model in your industry, and state what would have to change for you to adopt it. (A1, K1)
2. Identify a specific process that is invisible, manual or reactive today, and define what you would measure, how often, and who or what would act on the reading. (A2, K1)
3. Explain how the data would actually flow — device, uplink, cloud, dashboard or alert, and the downlink command that closes the loop. You did this end to end in Labs 1 to 4. (A3, K2)
4. Build the cost-benefit case: hardware, connectivity, platform, integration and running cost against labour saved, downtime avoided and new revenue. State the security and privacy risks honestly. (A4, K3)
5. Turn it into a staged action plan using design thinking — a pilot on one asset, a measurable success criterion, a named owner, and the evidence you would need before scaling. (A5, K4)

> **Note:** If you can answer these five in order for your own organisation, you are ready for both the Written Assessment and the Oral Questioning.


## Troubleshooting the Labs

- No data on the dashboard — confirm the device token is correct and that you are posting to the right project. Re-copy the snippet from the device's Integrate page, which is pre-filled with your values.
- 401 or 403 from the API — the Authorization header is missing, malformed, or the token is wrong. The header must read: Authorization: Bearer dev_XXXXXXXXXXXX
- Reading posted but no widget updates — check that the widget's metric name matches the key you sent exactly (temperature is not the same as Temperature).
- MQTT will not connect — confirm the broker host and port 1883, and that you installed the MQTT extra: pip install "iotflow[mqtt]". Without it the client falls back to HTTP only.
- Commands not reaching the device — the handler must be running. iot.run() polls over HTTP; iot.loop_forever() keeps an MQTT connection open for instant delivery.
- n8n workflow does not fire — make sure the workflow is ACTIVE and that you pasted the Production URL, not the Test URL, into the IoTFlow automation.


## Glossary

- **Actuator** — A device that acts on the physical world — a relay, motor, valve, pump or alarm — usually driven by a command from the cloud.
- **API key / Device token** — The secret credential that authenticates a device to the platform. Sent as an Authorization: Bearer header.
- **Cloud platform** — A managed service that ingests, stores, visualises and acts on telemetry so you do not run servers yourself.
- **Cost-benefit analysis** — Weighing the total cost of an IoT deployment (hardware, connectivity, platform, integration, running cost) against its measurable benefits.
- **Dashboard** — A screen of widgets — number cards, gauges, charts, LEDs, maps — that shows current and historical device data.
- **Design thinking** — A five-stage innovation method — Empathise, Define, Ideate, Prototype, Test — from the Stanford d.school.
- **Digitisation** — Applying digital technology to a business process so that it produces data that can be measured, analysed and acted on.
- **Downlink** — Traffic from the cloud to the device — commands that change device state, such as switching a relay.
- **Edge computing** — Processing data at or near the device instead of in the cloud, to cut latency, bandwidth and privacy exposure.
- **Gateway** — A device that aggregates nearby sensors, translates protocols and forwards data to the cloud.
- **HTTP REST API** — A request/response web interface. Devices POST readings as JSON to an endpoint such as /api/telemetry.
- **Industry 4.0** — The fourth industrial revolution — the convergence of IoT, AI, 5G, cloud computing and robotics in industry.
- **IoT (Internet of Things)** — Connecting physical objects to the internet so they can report their state and be acted upon remotely.
- **IoTFlow** — The IoT cloud platform used for the hands-on labs in this course — https://iot.tertiaryinfotech.com
- **LoRaWAN** — A long-range, low-power wireless protocol for small payloads — used in agriculture, metering and city-scale sensing.
- **Mirai** — The 2016 botnet that harvested IoT devices with default credentials and launched a major DDoS attack.
- **MQTT** — A lightweight publish/subscribe messaging protocol designed for constrained devices and real-time two-way traffic.
- **n8n** — A no-code workflow automation tool. An IoTFlow automation calls an n8n webhook to notify, log and analyse events.
- **Payback period** — How long it takes for the accumulated benefits of an IoT deployment to exceed its total cost.
- **Predictive maintenance** — Using sensor data to service equipment before it fails, converting unplanned downtime into scheduled work.
- **Sensor** — A device that measures a physical quantity — temperature, humidity, motion, light, location — and reports it as data.
- **Telemetry** — The stream of measurements a device sends to the cloud, each with a value and a timestamp.
- **Uplink** — Traffic from the device to the cloud — sensor readings and status messages.
- **Virtual pin** — A named channel (V1, relay, pump) that binds a dashboard control widget to a value the device acts on.
- **Webhook** — An HTTP callback. The platform POSTs event data to a URL you supply, triggering an external workflow.
