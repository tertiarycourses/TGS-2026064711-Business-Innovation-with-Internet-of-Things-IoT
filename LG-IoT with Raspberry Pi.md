# IoT with Raspberry Pi — Learner Guide

**WSQ Course Code:** TGS-2020505433  |  **Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)  |  **Version v15.0 · 8 August 2026**

## Contents

- [Introduction](#introduction)
- [Course Learning Outcomes](#course-learning-outcomes)
- [How This Course Is Assessed](#how-this-course-is-assessed)
- [Skills Framework Mapping](#skills-framework-mapping)
- [Before You Start — Setting Up for the Hands-On Labs](#before-you-start--setting-up-for-the-hands-on-labs)
- [Topic 01 — Overview of Internet of Things (IoT)  (LO1 · A1, K1 · Day 1 AM)](#topic-01--overview-of-internet-of-things-iot--lo1--a1-k1--day-1-am)
  - [Activity — Discussion — Analyse an IoT Use Case  (20 minutes)](#activity--discussion--analyse-an-iot-use-case--20-minutes)
- [Topic 02 — Collect and Post Environmental Data to Cloud  (LO2 · A2, K2, K3 · Day 1 PM)](#topic-02--collect-and-post-environmental-data-to-cloud--lo2--a2-k2-k3--day-1-pm)
  - [Lab 1 — Register Your Raspberry Pi on IoTFlow](#lab-1--register-your-raspberry-pi-on-iotflow)
  - [Lab 2 — Collect Environmental Data and Post It to the Cloud](#lab-2--collect-environmental-data-and-post-it-to-the-cloud)
- [Topic 03 — IoT Data Analytics and Visualization  (LO3 · A3, K4, K5 · Day 2 AM)](#topic-03--iot-data-analytics-and-visualization--lo3--a3-k4-k5--day-2-am)
  - [Activity — Discussion — Design Your Monitoring Dashboard  (20 minutes)](#activity--discussion--design-your-monitoring-dashboard--20-minutes)
  - [Lab 3 — Analyse and Visualise Your IoT Data on the Cloud](#lab-3--analyse-and-visualise-your-iot-data-on-the-cloud)
- [Topic 04 — Monitor Data to Trigger Control from Cloud  (LO4 · A4, K6, K7 · Day 2 PM)](#topic-04--monitor-data-to-trigger-control-from-cloud--lo4--a4-k6-k7--day-2-pm)
  - [Activity — Discussion — Monitor Effectiveness and Manage Risk  (20 minutes)](#activity--discussion--monitor-effectiveness-and-manage-risk--20-minutes)
  - [Lab 4 — Monitor Data and Trigger Control on the Raspberry Pi](#lab-4--monitor-data-and-trigger-control-on-the-raspberry-pi)
- [Putting It Together — The Complete IoT Loop](#putting-it-together--the-complete-iot-loop)
- [Troubleshooting the Labs](#troubleshooting-the-labs)
- [Glossary](#glossary)


## Introduction

This Learner Guide accompanies the WSQ course IoT with Raspberry Pi (TGS-2020505433), conducted by Tertiary Infotech Academy Pte Ltd. It is a two-day (16-hour) course mapped to the Skills Framework TSC Internet of Things Management (EVS-TEM-4002-1.1, Level 4).

The course is deliberately practical. Topic 1 builds the concepts — what IoT is, how it works, and where it is used. Topics 2, 3 and 4 are hands-on: you will connect a Raspberry Pi to the cloud, stream real sensor readings, visualise and analyse them, and finally control the hardware back from the dashboard. Every lab runs on IoTFlow (https://iot.tertiaryinfotech.com), an open-source IoT platform (https://github.com/alfredang/iotplatform).

This guide contains the full step-by-step instructions for every lab. The slide deck deliberately shows only each lab's purpose and outcome, so follow the numbered steps here while the trainer demonstrates. Keep this guide with you during the assessment — it is open book.


## Course Learning Outcomes

On completion of this course, you will be able to:

- LO1: Analyse the uses and functions of IoT technologies. (A1, K1)
- LO2: Collect environment data with Raspberry Pi and post the data to cloud computing. (A2, K2, K3)
- LO3: Use cloud computing to analyse and visualise IoT data. (A3, K4, K5)
- LO4: Monitor data and trigger control on devices. (A4, K6, K7)


## How This Course Is Assessed

The assessment has two instruments, both open book, conducted at the end of Day 2:

- Written Assessment (WA) — Short-Answer Questions (Q&A), 60 minutes, open book. Covers K1–K7.
- Practical Performance (PP) — 60 minutes, open book, individually completed. Covers A1–A4.
- Open book means you may refer to the course slides, this Learner Guide and any approved materials.
- A minimum of 75% attendance is required to be eligible for assessment and funding.
- An appeal process is available if you disagree with the assessment outcome.

The Written Assessment covers the seven knowledge statements (K1–K7) and the Practical Performance covers the four abilities (A1–A4). Each topic in this guide is labelled with the ability and knowledge it develops, so you can see exactly what each session is preparing you for.


## Skills Framework Mapping

**Abilities — assessed by the Practical Performance**

- A1 — Analyse relevant data to recommend control actions
- A2 — Identify areas for implementing IoT solutions for process improvement
- A3 — Use relevant tool to analyse and record performance
- A4 — Monitor the effectiveness of IoT solutions

**Knowledge — assessed by the Written Assessment**

- K1 — IoT concept and technical knowledge of IoT implementation
- K2 — Connectivity in devices using sensors, smart devices and other technologies for data collection and communication
- K3 — Equipment automation
- K4 — Building and/or Environment automation
- K5 — Advanced process control
- K6 — Security and privacy applications for IoT
- K7 — IoT guidelines and communication standards


## Before You Start — Setting Up for the Hands-On Labs

**What you need**

- A free learner account on IoTFlow — https://iot.tertiaryinfotech.com. Sign up with your email; no credit card is required.
- A Raspberry Pi (any model with WiFi — Pi 3, Pi 4, Pi 5 or Pi Zero W) running Raspberry Pi OS, connected to the internet. The classroom units are already imaged and ready.
- An environmental sensor — a Sense HAT (temperature, humidity, pressure) or a DHT11/DHT22 on a GPIO pin. If you have no sensor, every lab still works with simulated readings.
- An LED with a 330 Ω resistor (or a relay module) for the remote-control lab in Topic 4.
- A laptop with a modern web browser, used to reach the Pi over SSH or VNC and to open the dashboard.
- A terminal with cURL available (built into Raspberry Pi OS, macOS, Linux and Windows 10+).
- Python 3 with the official client: pip install "iotflow[mqtt]" — already installed on the classroom units.

**Create your account and project**

Open https://iot.tertiaryinfotech.com, sign up, then create a project. A project is a self-contained workspace with its own devices, dashboard, alerts, map and automations. Name it after a monitoring scenario you care about — for example Environment Monitoring, Smart Classroom or Cold Room Monitoring. Using a real scenario makes the discussions in Topics 3 and 4 much more productive.

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


## Topic 01 — Overview of Internet of Things (IoT)  (LO1 · A1, K1 · Day 1 AM)

Industry 4.0 · What IoT is · Sensors & actuators · Wireless technologies · Use cases

**Key concepts**

- Industry 4.0 — Steam, electricity, computers and now cyber-physical systems — assets report their own state in real time.
- What IoT is — A network of physical objects embedded with sensors and connectivity that collect and exchange data.
- The four building blocks — Sensors/devices capture data, connectivity moves it, cloud processes it, a UI acts on it.
- Sensors and actuators — Sensors turn a physical phenomenon into a signal; actuators turn a decision back into physical action.
- Wireless technologies — WiFi, BLE, Zigbee, LoRaWAN, NB-IoT and 5G trade range against power, bandwidth and cost.
- Types of IoT — Consumer, commercial, industrial (IIoT) and infrastructure IoT each serve a different context.


### Activity — Discussion — Analyse an IoT Use Case  (20 minutes)

In pairs, pick one of the IoT use cases covered (healthcare, agriculture, connected vehicles, smart home, smart city, smart building, logistics, manufacturing or retail) and analyse how the data collected leads to a recommended control action.

**Discussion prompts**

- What is physically being sensed, how often, and by what kind of sensor?
- Which wireless technology suits that deployment — and why does range or power decide it?
- What control action does the data recommend, and who or what carries it out?
- What would the organisation lose if that measurement did not exist?

**What to produce**

A short analysis linking the sensed data to a specific recommended control action.

> **Note:** Write your answer down as you go. The same reasoning is what the Written Assessment asks you to demonstrate for A1.


## Topic 02 — Collect and Post Environmental Data to Cloud  (LO2 · A2, K2, K3 · Day 1 PM)

Cloud platforms · Raspberry Pi · Sensors · Device tokens · HTTP REST & MQTT uplink

**Key concepts**

- Cloud computing for IoT — The cloud gives constrained devices the storage, compute and availability they lack.
- IoTFlow — Our platform: projects, devices, tokens, dashboards, alerts and automations in one place.
- Raspberry Pi as gateway — A low-cost Linux computer with GPIO, WiFi and Python — it reads sensors and speaks to the cloud.
- Reading environmental data — Temperature, humidity and pressure from a Sense HAT, DHT11/DHT22 or a simulated source.
- Device tokens — A token authenticates every message a device sends — and is why credential management matters.
- HTTP REST & MQTT uplink — POST JSON to a REST endpoint, or publish over MQTT for lightweight real-time streaming.


### Lab 1 — Register Your Raspberry Pi on IoTFlow

Objective: Identify an area for an IoT solution and connect the asset to the cloud (A2, K2).

Goal: Turn your Raspberry Pi into a managed IoT device. You sign in to IoTFlow, create a project workspace for your monitoring scenario, register the Pi through the Add Device wizard, choose how it will talk to the cloud (HTTP or MQTT), and capture the device token that authenticates every message it sends.

**What you'll build**

A registered Raspberry Pi device in your own IoTFlow project, with its device token saved   (Tools: IoTFlow projects · Add Device wizard · Device tokens · HTTP & MQTT.)

![IoTFlow — Lab 1: Register Your Raspberry Pi on IoTFlow](courseware/assets/lab-01-add-device.png)

*IoTFlow — Lab 1: Register Your Raspberry Pi on IoTFlow*

**Why the business cares**

This is the first step of any IoT deployment: an asset that was previously invisible now has an identity, an owner and a data stream that can be measured, monitored and managed.

**Step-by-step**

1. Open the IoTFlow platform at https://iot.tertiaryinfotech.com and sign up for a free account, or log in if you already have one.
2. Create a project — a self-contained workspace with its own dashboard, alerts, map and automations. Name it after your monitoring scenario, e.g. 'Environment Monitoring' or 'Smart Classroom'.
3. Click Add Device in the sidebar and give the device a descriptive name that identifies the physical unit.

   ```bash
   Device name:  Raspberry Pi Sensor 01
   ```

4. Work through the guided wizard and choose a protocol. HTTP is the simplest — POST JSON to a REST endpoint. MQTT is a lightweight publish/subscribe protocol, better for real-time control and many devices. Both stay available afterwards.
5. Copy the device token shown when the device is created. It is displayed only once — save it somewhere safe on your Pi.

   ```bash
   dev_XXXXXXXXXXXX
   ```

6. Note how the token authenticates every message the device sends. Anyone holding the token can post as that device, which is exactly why device credential management is an IoT security concern (Topic 4).

   ```bash
   Authorization: Bearer dev_XXXXXXXXXXXX
   ```

7. Prepare the Raspberry Pi: boot Raspberry Pi OS, connect it to WiFi, and confirm you can reach the internet. If you are working headless, enable SSH or VNC from Preferences → Raspberry Pi Configuration → Interfaces.

   ```bash
   ping -c 3 iot.tertiaryinfotech.com
   ```


**Test it**

Your Raspberry Pi appears in the project's device list, and its Integrate page shows code snippets pre-filled with your endpoint and device token.

> **Note:** A standalone copy of this lab is in labs/lab-01-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


### Lab 2 — Collect Environmental Data and Post It to the Cloud

Objective: Collect environment data with the Raspberry Pi and post it to cloud computing (A2, K2, K3).

Goal: Read temperature and humidity on the Raspberry Pi and stream the readings to IoTFlow — first with a single cURL call, then with the official Python client over HTTP, then continuously over MQTT. This is the uplink every IoT solution depends on: without a reliable data stream there is nothing to analyse.

**What you'll build**

Live temperature and humidity telemetry streaming from the Raspberry Pi into IoTFlow   (Tools: Sense HAT / DHT22 · Telemetry REST API · Python client (pip install iotflow) · MQTT broker.)

![IoTFlow — Lab 2: Collect Environmental Data and Post It to the Cloud](courseware/assets/lab-02-send-reading.png)

*IoTFlow — Lab 2: Collect Environmental Data and Post It to the Cloud*

**Why the business cares**

Each reading is an operational fact with a timestamp. Once the stream exists, the organisation can answer questions it previously could not — how often, how long, how bad, and at what cost.

**Step-by-step**

1. Open the Integrate page for your device. Every snippet on it is pre-filled with your endpoint and device token.
2. Send your first reading from the Raspberry Pi terminal with cURL over HTTP POST, to prove connectivity before adding any sensor code.

   ```bash
   curl -X POST https://iot.tertiaryinfotech.com/api/telemetry \
  -H "Authorization: Bearer dev_XXXXXXXXXXXX" \
  -H "Content-Type: application/json" \
  -d '{"temperature": 28.5, "humidity": 65}'
   ```

3. Open the Dashboard. The reading appears under Latest Telemetry within seconds — widgets auto-refresh every 5 seconds.
4. Install the official IoTFlow Python client on the Pi from PyPI.

   ```bash
   pip install "iotflow[mqtt]"      # with real-time MQTT (paho-mqtt)
pip install iotflow               # HTTP only — zero dependencies
   ```

5. Read the real sensor. With a Sense HAT, use the sense_hat library — it gives temperature, humidity and pressure from one board.

   ```bash
   from sense_hat import SenseHat

sense = SenseHat()
temperature = round(sense.get_temperature(), 1)
humidity    = round(sense.get_humidity(), 1)
pressure    = round(sense.get_pressure(), 1)
print(temperature, humidity, pressure)
   ```

6. No Sense HAT? Use a DHT11/DHT22 on a GPIO pin instead — the rest of the lab is identical.

   ```bash
   import adafruit_dht, board

dht = adafruit_dht.DHT22(board.D4)     # data pin on GPIO4
temperature = dht.temperature
humidity    = dht.humidity
   ```

7. Post the sensor readings to IoTFlow over HTTP — several metrics at once with send(), or one at a time with virtual_write().

   ```bash
   from iotflow import IoTFlow

iot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "raspberry-pi-sensor-01")
iot.send(temperature=temperature, humidity=humidity, pressure=pressure)
iot.virtual_write("temperature", temperature)   # or one at a time
   ```

8. Stream continuously over MQTT. connect() runs MQTT in the background and mqtt_publish() sends a reading every few seconds — this is the shape of a real production sensor.

   ```bash
   iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="raspberry-pi-sensor-01",
              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)
iot.connect()                    # MQTT runs in the background
while True:
    iot.mqtt_publish(temperature=sense.get_temperature(),
                     humidity=sense.get_humidity())
    time.sleep(10)
   ```

9. Keep it running unattended: start the script at boot with systemd so the Pi resumes reporting after a power cut.

   ```bash
   sudo systemctl enable --now iotflow-sensor.service
   ```


**Test it**

Every value the Raspberry Pi sends appears in the Dashboard's Latest Telemetry within seconds, and the device's telemetry history grows with each reading.

> **Note:** A standalone copy of this lab is in labs/lab-02-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


## Topic 03 — IoT Data Analytics and Visualization  (LO3 · A3, K4, K5 · Day 2 AM)

Dashboards · Number cards, gauges & charts · Maps · Alert rules · Analysing trends

**Key concepts**

- Why visualise — A dashboard turns a stream of raw readings into an operational picture a manager can act on.
- Display widgets — Number cards, gauges, line and bar charts, LED indicators and maps, refreshed automatically.
- Analysing the data — Compare current readings against history to spot trends, drift and abnormal behaviour.
- Alert rules — Threshold and device-offline rules fire the moment a reading crosses a business-meaningful limit.
- Recording performance — Telemetry history is the evidence base for measuring whether the solution actually works.
- From data to decision — Analytics only pays off when a reading changes what somebody — or something — does next.


### Activity — Discussion — Design Your Monitoring Dashboard  (20 minutes)

Working from the data your Raspberry Pi is now streaming, decide what a supervisor actually needs to see on one screen, and which threshold would justify interrupting somebody.

**Discussion prompts**

- Which three widgets earn their place on the screen, and what does each one answer?
- What is the normal operating range, and at what value does it become a problem?
- How would you tell a genuine fault apart from a single noisy reading?
- What performance record would you need to prove the solution is working?

**What to produce**

A dashboard layout plus one justified alert threshold with its rationale.

> **Note:** Write your answer down as you go. The same reasoning is what the Written Assessment asks you to demonstrate for A3.


### Lab 3 — Analyse and Visualise Your IoT Data on the Cloud

Objective: Use the platform's tools to analyse IoT data and record performance (A3, K4, K5).

Goal: Build a live dashboard from the readings your Raspberry Pi is streaming — number cards, gauges, line charts, LED indicators and a map — then interrogate the history to spot trends and set a threshold alert at the point where somebody would actually need to act.

**What you'll build**

A live monitoring dashboard for your Raspberry Pi, plus a working threshold alert rule   (Tools: Display widgets · Number cards · Gauges · Line charts · Maps · Alert rules · Telemetry history.)

![IoTFlow — Lab 3: Analyse and Visualise Your IoT Data on the Cloud](courseware/assets/lab-05-dashboard.png)

*IoTFlow — Lab 3: Analyse and Visualise Your IoT Data on the Cloud*

**Why the business cares**

This is the screen the supervisor actually looks at. A dashboard makes performance visible, and an alert makes a problem timely instead of discovered too late.

**Step-by-step**

1. On the Dashboard click Add widget. Widgets are grouped into Display (show data) and Control (send commands). Add a Number card bound to the temperature metric and give it a clear title.
2. Add a Gauge for humidity with sensible min/max bounds (0–100 %). A gauge communicates 'where in the safe range are we' far better than a bare number.
3. Add a Line chart for temperature to plot the history over time. This is where trends, drift and daily cycles become visible.
4. Add an LED indicator for an on/off state, and a Map widget if your device reports a location. Arrange the layout — widgets snap to a responsive grid and refresh automatically every 5 seconds.
5. Analyse the history rather than the instant: open the telemetry view and compare the last hour against the last day. Identify the normal operating range, and note the highest and lowest readings.
6. Warm the sensor with your hand (or breathe on it) and watch the chart respond. Confirm the reading returns to baseline — this tells you the difference between a genuine event and sensor noise.
7. Create an alert rule on a business-meaningful threshold — the value at which a person would need to act, not simply an unusual number.

   ```bash
   Alert rule:  temperature > 30  →  raise alert
   ```

8. Add a device-offline rule so a Pi that stops reporting raises an alert instead of failing silently. Silent failure is the most common way an IoT deployment quietly stops delivering value.

   ```bash
   Alert rule:  device offline for 120 s  →  raise alert
   ```

9. Trigger the alert deliberately: warm the sensor past your threshold and confirm the alert appears as Active on the dashboard, then resolve it.
10. Record performance: note the readings, the alert that fired and the time it took to resolve. This log is the evidence base for judging whether the solution is effective (Topic 4).

**Test it**

Your dashboard shows live temperature, humidity and history from the Raspberry Pi, and crossing your threshold raises a visible Active alert that you can resolve.

> **Note:** A standalone copy of this lab is in labs/lab-03-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


## Topic 04 — Monitor Data to Trigger Control from Cloud  (LO4 · A4, K6, K7 · Day 2 PM)

Downlink control · Virtual pins · Automations & n8n · Monitoring effectiveness · IoT security

**Key concepts**

- Reading data back — Query the current state of every metric and virtual pin over the REST API or MQTT.
- Downlink control — Virtual pins carry commands from the dashboard back to the device to switch a relay or set a value.
- Closing the loop — Monitoring tells you what happened; control lets the system act without anyone driving to site.
- Automation with n8n — Alerts fire a webhook into a low-code workflow that notifies, logs, and can ask AI to recommend.
- Monitoring effectiveness — Track uptime, alert response and the metric you set out to improve — then tune the rules.
- IoT security — Constrained, unattended devices with physical consequences — protect tokens, transport and firmware.


### Activity — Discussion — Monitor Effectiveness and Manage Risk  (20 minutes)

Take the IoT solution you have built across the labs and plan how you would monitor its effectiveness in production — and how you would secure it.

**Discussion prompts**

- Which metrics tell you the solution is working — uptime, response time, or the business outcome?
- How would you know a device had silently stopped reporting?
- Where are the credentials in your solution, and what happens if one leaks?
- Which standard or guideline would you cite when asked how the data is protected?

**What to produce**

A monitoring and security plan: the effectiveness metrics, the offline strategy, and the top three risks.

> **Note:** Write your answer down as you go. The same reasoning is what the Written Assessment asks you to demonstrate for A4.


### Lab 4 — Monitor Data and Trigger Control on the Raspberry Pi

Objective: Monitor IoT data and trigger a control action on the device from the cloud (A4, K6, K7).

Goal: Read device state back out of the cloud over the REST API and MQTT, then add Control widgets (switch, slider) bound to virtual pins and drive an LED or relay on the Raspberry Pi from the dashboard. Reading data is monitoring; sending a command back is automation — and that is where the labour saving appears.

**What you'll build**

A dashboard switch and slider that control an LED/relay on the Raspberry Pi in real time   (Tools: REST API (GET /api/device/state) · MQTT subscribe · Control widgets · Virtual pins · @on_command · GPIO.)

![IoTFlow — Lab 4: Monitor Data and Trigger Control on the Raspberry Pi](courseware/assets/lab-04-control-device.png)

*IoTFlow — Lab 4: Monitor Data and Trigger Control on the Raspberry Pi*

**Why the business cares**

Monitoring tells you what happened. Control lets the system act without a person driving out to site — usually the single largest line in an IoT cost-benefit case.

**Step-by-step**

1. Read your device's latest state from the terminal over the REST API and inspect the JSON reply — the platform returns the current value of every metric and virtual pin.

   ```bash
   curl https://iot.tertiaryinfotech.com/api/device/state \
  -H "Authorization: Bearer dev_XXXXXXXXXXXX"
   ```

2. Subscribe to your device's MQTT downlink topic to watch commands arrive in real time. Note the direction: uplink is telemetry, downlink is commands.

   ```bash
   mosquitto_sub -h iot.tertiaryinfotech.com -p 1883 \
  -u device -P dev_XXXXXXXXXXXX -t "devices/<id>/down" -v
   ```

3. Wire an LED to the Raspberry Pi: long leg to GPIO17 through a 330 Ω resistor, short leg to GND. A relay module in place of the LED switches a real appliance.
4. On the Dashboard click Add widget and choose a Control type: Button (momentary), Switch (toggle), Slider (value) or Terminal (text).
5. Assign the virtual pin the widget writes to — for example V1. For a slider also set the min/max range.

   ```bash
   Virtual pin:  V1
   ```

6. React to commands on the Pi with the iotflow client. Decorate a handler with @iot.on_command and drive the GPIO pin from inside it.

   ```bash
   from iotflow import IoTFlow
from gpiozero import LED

led = LED(17)
iot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "raspberry-pi-sensor-01")

@iot.on_command
def handle(pin, value, text):
    if pin == "V1":
        led.on() if int(value) else led.off()

iot.run(interval=3)                   # blocks, polls every 3 s
   ```

7. For real-time control use the same handler over MQTT — loop_forever() keeps the connection open so commands arrive instantly instead of on the next poll.

   ```bash
   iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="raspberry-pi-sensor-01",
              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)

@iot.on_command
def handle(pin, value, text): ...

iot.loop_forever()
   ```

8. Flip the switch and drag the slider on the dashboard. The LED responds within a second — you are now controlling hardware from the cloud.
9. Automate the response. In n8n, add a Webhook node to a new workflow, activate it and copy the Production URL.
10. Back in IoTFlow, create an Automation: choose the trigger (telemetry received, alert fired, device online/offline, or command sent), narrow it by device and metric, then paste the n8n webhook URL and save.
11. Use Test to send a sample payload to n8n and inspect the JSON the webhook receives, then enable live triggering.
12. In n8n, branch the flow: send an Email or Telegram notification and append the reading to Google Sheets, so the event is both escalated and recorded for later analysis.
13. Close the loop: add an HTTP Request node that sends a downlink command back to the Pi — for example switching a fan on when the temperature alert fires.

   ```bash
   POST https://iot.tertiaryinfotech.com/api/device/command
{ "pin": "V1", "value": 1 }
   ```

14. Secure what you have built: never commit the device token to source control, keep it in an environment variable, use TLS endpoints, and regenerate the token if it is ever exposed.

   ```bash
   export IOTFLOW_TOKEN="dev_XXXXXXXXXXXX"   # not hard-coded in the script
   ```

15. Monitor effectiveness: check that the alert fired, the notification arrived, the row was logged and the fan switched on. Record how long the whole loop took — that is your response time metric.

**Test it**

Pushing a reading above the threshold fires the automation end to end: the notification arrives, a row is appended to the sheet, and the command sent back switches the LED/relay on the Raspberry Pi.

> **Note:** A standalone copy of this lab is in labs/lab-04-*.md so you can repeat it after the course. Your IoTFlow project stays available to you.

---


## Putting It Together — The Complete IoT Loop

By the end of Day 2 you should be able to carry one scenario through the whole arc of the course. This is the reasoning the assessment is built around:

1. Analyse the use case: state what is being sensed, which sensor and wireless technology suit it, and what control action the data should recommend. (A1, K1)
2. Connect the asset: register the Raspberry Pi on the platform, capture the device token, and choose HTTP or MQTT for the uplink. You did this in Lab 1. (A2, K2)
3. Collect and post the data: read temperature and humidity on the Pi and stream the readings to the cloud reliably, including unattended operation. You did this in Lab 2. (A2, K2, K3)
4. Analyse and visualise: build the dashboard, interpret the telemetry history for trends and drift, and set an alert rule at a threshold that justifies acting. You did this in Lab 3. (A3, K4, K5)
5. Monitor and control: drive the LED or relay from the dashboard over a virtual pin, automate the response with n8n, then judge whether the solution is effective and secure. Lab 4. (A4, K6, K7)

> **Note:** If you can work through these five steps for your own scenario, you are ready for both the Written Assessment and the Practical Performance.


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
- **GPIO** — General-Purpose Input/Output — the Raspberry Pi header pins used to wire sensors and actuators.
- **Sense HAT** — A Raspberry Pi add-on board with temperature, humidity, pressure and motion sensors plus an LED matrix.
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
