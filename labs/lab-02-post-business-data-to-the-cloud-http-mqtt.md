# Lab 2 — Post Business Data to the Cloud (HTTP & MQTT)

**Course:** Business Innovation with Internet-of-Things (IoT) (TGS-2026064711)  
**Topic 03:** IoT Technology  
**Objective:** Apply digitisation by streaming operational data from the asset to the cloud (A3, K2).  
**Platform:** IoTFlow — https://iot.tertiaryinfotech.com

## Goal

Send readings to IoTFlow three different ways — cURL from any terminal, the Python client, and (optionally) an ESP32/ESP8266 over MQTT — and watch them arrive live. This is the uplink that every IoT business case depends on: without a reliable data stream there is nothing to analyse.

## What you'll build

Live temperature and humidity telemetry streaming into IoTFlow from terminal and Python

*Uses: Telemetry REST API · Python client (pip install iotflow) · MQTT broker · ESP32/ESP8266.*

![IoTFlow — Lab 2](../courseware/assets/lab-02-send-reading.png)

## Why the business cares

Each reading is an operational fact with a timestamp. Once the stream exists, the business can ask questions it previously could not answer — how often, how long, how bad, and at what cost.

## Prerequisites

- A free account on IoTFlow (https://iot.tertiaryinfotech.com).
- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be completed with cURL or Python from any terminal.
- Your device token from Lab 1 (`dev_...`).
- Optional, for the scripted steps: Python 3 with `pip install "iotflow[mqtt]"`.

## Step-by-step

### Step 1 — Open the Integrate page for your device. Every snippet on it is pre-filled with your endpoint and device token.

### Step 2 — Send your first reading from any terminal with cURL over HTTP POST.

```bash
curl -X POST https://iot.tertiaryinfotech.com/api/telemetry \
  -H "Authorization: Bearer dev_XXXXXXXXXXXX" \
  -H "Content-Type: application/json" \
  -d '{"temperature": 22.5, "humidity": 60}'
```

### Step 3 — Open the Dashboard. The reading appears under Latest Telemetry within seconds — widgets auto-refresh every 5 seconds.

### Step 4 — Install the official IoTFlow Python client from PyPI.

```bash
pip install "iotflow[mqtt]"      # with real-time MQTT (paho-mqtt)
pip install iotflow               # HTTP only — zero dependencies
```

### Step 5 — Send readings from Python over HTTP — several metrics at once with send(), or one at a time with virtual_write().

```bash
from iotflow import IoTFlow

iot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "cold-room-sensor-01")
iot.send(temperature=22.5, humidity=60)      # several metrics at once
iot.virtual_write("temperature", 22.5)       # or one at a time
```

### Step 6 — Stream continuously over MQTT with the telemetry_upload.py example — download it, fill in your broker host, device id and device token, then run it.

```bash
curl -O https://raw.githubusercontent.com/alfredang/iotplatform/main/clients/python/examples/telemetry_upload.py
# edit: MQTT_BROKER = "iot.tertiaryinfotech.com", DEVICE_ID, DEVICE_TOKEN
python telemetry_upload.py
```

### Step 7 — Study the loop inside telemetry_upload.py — connect() runs MQTT in the background and mqtt_publish() sends a reading every 10 seconds. This is the shape of a real production sensor.

```bash
iot = IoTFlow(token=DEVICE_TOKEN, device_id=DEVICE_ID,
              mqtt_host=MQTT_BROKER, mqtt_port=MQTT_PORT)
iot.connect()                    # MQTT runs in the background
while True:
    iot.mqtt_publish(temperature=temperature, humidity=humidity, voltage=3.7)
    time.sleep(PUBLISH_INTERVAL_S)
```

### Step 8 — Hardware alternative (optional): flash the ESP8266_Telemetry_Upload Arduino sketch. The Arduino library speaks the same protocol as the Python client, so the dashboard cannot tell the difference.

```bash
IoTFlow.virtualWrite("temperature", t);   // metric name binds to dashboard widgets
```

## Test it

Every value you send appears in the Dashboard's Latest Telemetry within seconds, and the device's telemetry history grows with each reading.

---
*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · www.tertiarycourses.com.sg*
