# Lab 1 — Register Your Raspberry Pi on IoTFlow

**Course:** IoT with Raspberry Pi (TGS-2020505433)  
**Topic 02:** Collect and Post Environmental Data to Cloud  
**Objective:** Identify an area for an IoT solution and connect the asset to the cloud (A2, K2).  
**Platform:** IoTFlow — https://iot.tertiaryinfotech.com

## Goal

Turn your Raspberry Pi into a managed IoT device. You sign in to IoTFlow, create a project workspace for your monitoring scenario, register the Pi through the Add Device wizard, choose how it will talk to the cloud (HTTP or MQTT), and capture the device token that authenticates every message it sends.

## What you'll build

A registered Raspberry Pi device in your own IoTFlow project, with its device token saved

*Uses: IoTFlow projects · Add Device wizard · Device tokens · HTTP & MQTT.*

![IoTFlow — Lab 1](../courseware/assets/lab-01-add-device.png)

## Why the business cares

This is the first step of any IoT deployment: an asset that was previously invisible now has an identity, an owner and a data stream that can be measured, monitored and managed.

## Prerequisites

- A free account on IoTFlow (https://iot.tertiaryinfotech.com).
- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be completed with cURL or Python from any terminal.
- Optional, for the scripted steps: Python 3 with `pip install "iotflow[mqtt]"`.

## Step-by-step

### Step 1 — Open the IoTFlow platform at https://iot.tertiaryinfotech.com and sign up for a free account, or log in if you already have one.

### Step 2 — Create a project — a self-contained workspace with its own dashboard, alerts, map and automations. Name it after your monitoring scenario, e.g. 'Environment Monitoring' or 'Smart Classroom'.

### Step 3 — Click Add Device in the sidebar and give the device a descriptive name that identifies the physical unit.

```bash
Device name:  Raspberry Pi Sensor 01
```

### Step 4 — Work through the guided wizard and choose a protocol. HTTP is the simplest — POST JSON to a REST endpoint. MQTT is a lightweight publish/subscribe protocol, better for real-time control and many devices. Both stay available afterwards.

### Step 5 — Copy the device token shown when the device is created. It is displayed only once — save it somewhere safe on your Pi.

```bash
dev_XXXXXXXXXXXX
```

### Step 6 — Note how the token authenticates every message the device sends. Anyone holding the token can post as that device, which is exactly why device credential management is an IoT security concern (Topic 4).

```bash
Authorization: Bearer dev_XXXXXXXXXXXX
```

### Step 7 — Prepare the Raspberry Pi: boot Raspberry Pi OS, connect it to WiFi, and confirm you can reach the internet. If you are working headless, enable SSH or VNC from Preferences → Raspberry Pi Configuration → Interfaces.

```bash
ping -c 3 iot.tertiaryinfotech.com
```

## Test it

Your Raspberry Pi appears in the project's device list, and its Integrate page shows code snippets pre-filled with your endpoint and device token.

---
*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · www.tertiarycourses.com.sg*
