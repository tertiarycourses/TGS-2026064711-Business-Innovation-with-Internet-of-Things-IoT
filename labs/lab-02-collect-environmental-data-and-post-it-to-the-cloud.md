# Lab 2 — Collect Environmental Data and Post It to the Cloud

**Course:** IoT with Raspberry Pi (TGS-2020505433)  
**Topic 02:** Collect and Post Environmental Data to Cloud  
**Objective:** Collect environment data with the Raspberry Pi and post it to cloud computing (A2, K2, K3).  
**Platform:** IoTFlow — https://iot.tertiaryinfotech.com

## Goal

Read temperature and humidity on the Raspberry Pi and stream the readings to IoTFlow — first with a single cURL call, then with the official Python client over HTTP, then continuously over MQTT. This is the uplink every IoT solution depends on: without a reliable data stream there is nothing to analyse.

## What you'll build

Live temperature and humidity telemetry streaming from the Raspberry Pi into IoTFlow

*Uses: Sense HAT / DHT22 · Telemetry REST API · Python client (pip install iotflow) · MQTT broker.*

![IoTFlow — Lab 2](../courseware/assets/lab-02-send-reading.png)

## Why the business cares

Each reading is an operational fact with a timestamp. Once the stream exists, the organisation can answer questions it previously could not — how often, how long, how bad, and at what cost.

## Prerequisites

- A free account on IoTFlow (https://iot.tertiaryinfotech.com).
- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be completed with cURL or Python from any terminal.
- Your device token from Lab 1 (`dev_...`).
- Optional, for the scripted steps: Python 3 with `pip install "iotflow[mqtt]"`.

## Step-by-step

### Step 1 — Open the Integrate page for your device. Every snippet on it is pre-filled with your endpoint and device token.

### Step 2 — Send your first reading from the Raspberry Pi terminal with cURL over HTTP POST, to prove connectivity before adding any sensor code.

```bash
curl -X POST https://iot.tertiaryinfotech.com/api/telemetry \
  -H "Authorization: Bearer dev_XXXXXXXXXXXX" \
  -H "Content-Type: application/json" \
  -d '{"temperature": 28.5, "humidity": 65}'
```

### Step 3 — Open the Dashboard. The reading appears under Latest Telemetry within seconds — widgets auto-refresh every 5 seconds.

### Step 4 — Install the official IoTFlow Python client on the Pi from PyPI.

```bash
pip install "iotflow[mqtt]"      # with real-time MQTT (paho-mqtt)
pip install iotflow               # HTTP only — zero dependencies
```

### Step 5 — Read the real sensor. With a Sense HAT, use the sense_hat library — it gives temperature, humidity and pressure from one board.

```bash
from sense_hat import SenseHat

sense = SenseHat()
temperature = round(sense.get_temperature(), 1)
humidity    = round(sense.get_humidity(), 1)
pressure    = round(sense.get_pressure(), 1)
print(temperature, humidity, pressure)
```

### Step 6 — No Sense HAT? Use a DHT11/DHT22 on a GPIO pin instead — the rest of the lab is identical.

```bash
import adafruit_dht, board

dht = adafruit_dht.DHT22(board.D4)     # data pin on GPIO4
temperature = dht.temperature
humidity    = dht.humidity
```

### Step 7 — Post the sensor readings to IoTFlow over HTTP — several metrics at once with send(), or one at a time with virtual_write().

```bash
from iotflow import IoTFlow

iot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "raspberry-pi-sensor-01")
iot.send(temperature=temperature, humidity=humidity, pressure=pressure)
iot.virtual_write("temperature", temperature)   # or one at a time
```

### Step 8 — Stream continuously over MQTT. connect() runs MQTT in the background and mqtt_publish() sends a reading every few seconds — this is the shape of a real production sensor.

```bash
iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="raspberry-pi-sensor-01",
              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)
iot.connect()                    # MQTT runs in the background
while True:
    iot.mqtt_publish(temperature=sense.get_temperature(),
                     humidity=sense.get_humidity())
    time.sleep(10)
```

### Step 9 — Keep it running unattended: start the script at boot with systemd so the Pi resumes reporting after a power cut.

```bash
sudo systemctl enable --now iotflow-sensor.service
```

## Test it

Every value the Raspberry Pi sends appears in the Dashboard's Latest Telemetry within seconds, and the device's telemetry history grows with each reading.

---
*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · www.tertiarycourses.com.sg*
