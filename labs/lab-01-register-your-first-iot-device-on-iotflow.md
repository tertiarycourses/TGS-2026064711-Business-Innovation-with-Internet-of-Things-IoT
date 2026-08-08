# Lab 1 — Register Your First IoT Device on IoTFlow

**Course:** Business Innovation with Internet-of-Things (IoT) (TGS-2026064711)  
**Topic 03:** IoT Technology  
**Objective:** Identify how digitisation is applied to a business asset by connecting it to the cloud (A3, K2).  
**Platform:** IoTFlow — https://iot.tertiaryinfotech.com

## Goal

Turn a physical asset into a digital one. You sign in to IoTFlow, create a project workspace for your business scenario, register a device through the Add Device wizard, choose how it will talk to the cloud (HTTP or MQTT), and capture the device token that authenticates every message it sends.

## What you'll build

A registered IoT device in your own IoTFlow project, with its device token saved

*Uses: IoTFlow projects · Add Device wizard · Device tokens · HTTP & MQTT.*

![IoTFlow — Lab 1](../courseware/assets/lab-01-add-device.png)

## Why the business cares

This is the first step of digitisation: an asset that was previously invisible to the business now has an identity, an owner and a data stream that can be measured and managed.

## Prerequisites

- A free account on IoTFlow (https://iot.tertiaryinfotech.com).
- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be completed with cURL or Python from any terminal.
- Optional, for the scripted steps: Python 3 with `pip install "iotflow[mqtt]"`.

## Step-by-step

### Step 1 — Open the IoTFlow platform at https://iot.tertiaryinfotech.com and sign up for a free account, or log in if you already have one.

### Step 2 — Create a project — a self-contained workspace with its own dashboard, alerts, map and automations. Name it after your business scenario, e.g. 'Cold Chain Monitoring' or 'Smart Office'.

### Step 3 — Click Add Device in the sidebar and give the device a descriptive, business-meaningful name.

```bash
Device name:  Cold Room Sensor 01
```

### Step 4 — Work through the guided wizard and choose a protocol. HTTP is the simplest — POST JSON to a REST endpoint. MQTT is a lightweight publish/subscribe protocol, better for many devices and real-time control. Both stay available afterwards.

### Step 5 — Copy the device token shown when the device is created. It is displayed only once — save it somewhere safe.

```bash
dev_XXXXXXXXXXXX
```

### Step 6 — Note how the token authenticates every message the device sends. Anyone holding the token can post as that device, which is exactly why device credential management is an IoT security concern (Topic 4).

```bash
Authorization: Bearer dev_XXXXXXXXXXXX
```

## Test it

Your new device appears in the project's device list, and its Integrate page shows code snippets pre-filled with your endpoint and device token.

---
*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · www.tertiarycourses.com.sg*
