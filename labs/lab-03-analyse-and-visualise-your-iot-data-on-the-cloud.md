# Lab 3 — Analyse and Visualise Your IoT Data on the Cloud

**Course:** IoT with Raspberry Pi (TGS-2020505433)  
**Topic 03:** IoT Data Analytics and Visualization  
**Objective:** Use the platform's tools to analyse IoT data and record performance (A3, K4, K5).  
**Platform:** IoTFlow — https://iot.tertiaryinfotech.com

## Goal

Build a live dashboard from the readings your Raspberry Pi is streaming — number cards, gauges, line charts, LED indicators and a map — then interrogate the history to spot trends and set a threshold alert at the point where somebody would actually need to act.

## What you'll build

A live monitoring dashboard for your Raspberry Pi, plus a working threshold alert rule

*Uses: Display widgets · Number cards · Gauges · Line charts · Maps · Alert rules · Telemetry history.*

![IoTFlow — Lab 3](../courseware/assets/lab-05-dashboard.png)

## Why the business cares

This is the screen the supervisor actually looks at. A dashboard makes performance visible, and an alert makes a problem timely instead of discovered too late.

## Prerequisites

- A free account on IoTFlow (https://iot.tertiaryinfotech.com).
- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be completed with cURL or Python from any terminal.
- Your device token from Lab 1 (`dev_...`).
- Optional, for the scripted steps: Python 3 with `pip install "iotflow[mqtt]"`.

## Step-by-step

### Step 1 — On the Dashboard click Add widget. Widgets are grouped into Display (show data) and Control (send commands). Add a Number card bound to the temperature metric and give it a clear title.

### Step 2 — Add a Gauge for humidity with sensible min/max bounds (0–100 %). A gauge communicates 'where in the safe range are we' far better than a bare number.

### Step 3 — Add a Line chart for temperature to plot the history over time. This is where trends, drift and daily cycles become visible.

### Step 4 — Add an LED indicator for an on/off state, and a Map widget if your device reports a location. Arrange the layout — widgets snap to a responsive grid and refresh automatically every 5 seconds.

### Step 5 — Analyse the history rather than the instant: open the telemetry view and compare the last hour against the last day. Identify the normal operating range, and note the highest and lowest readings.

### Step 6 — Warm the sensor with your hand (or breathe on it) and watch the chart respond. Confirm the reading returns to baseline — this tells you the difference between a genuine event and sensor noise.

### Step 7 — Create an alert rule on a business-meaningful threshold — the value at which a person would need to act, not simply an unusual number.

```bash
Alert rule:  temperature > 30  →  raise alert
```

### Step 8 — Add a device-offline rule so a Pi that stops reporting raises an alert instead of failing silently. Silent failure is the most common way an IoT deployment quietly stops delivering value.

```bash
Alert rule:  device offline for 120 s  →  raise alert
```

### Step 9 — Trigger the alert deliberately: warm the sensor past your threshold and confirm the alert appears as Active on the dashboard, then resolve it.

### Step 10 — Record performance: note the readings, the alert that fired and the time it took to resolve. This log is the evidence base for judging whether the solution is effective (Topic 4).

## Test it

Your dashboard shows live temperature, humidity and history from the Raspberry Pi, and crossing your threshold raises a visible Active alert that you can resolve.

---
*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · www.tertiarycourses.com.sg*
