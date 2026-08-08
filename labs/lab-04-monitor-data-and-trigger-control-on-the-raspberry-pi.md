# Lab 4 — Monitor Data and Trigger Control on the Raspberry Pi

**Course:** IoT with Raspberry Pi (TGS-2020505433)  
**Topic 04:** Monitor Data to Trigger Control from Cloud  
**Objective:** Monitor IoT data and trigger a control action on the device from the cloud (A4, K6, K7).  
**Platform:** IoTFlow — https://iot.tertiaryinfotech.com

## Goal

Read device state back out of the cloud over the REST API and MQTT, then add Control widgets (switch, slider) bound to virtual pins and drive an LED or relay on the Raspberry Pi from the dashboard. Reading data is monitoring; sending a command back is automation — and that is where the labour saving appears.

## What you'll build

A dashboard switch and slider that control an LED/relay on the Raspberry Pi in real time

*Uses: REST API (GET /api/device/state) · MQTT subscribe · Control widgets · Virtual pins · @on_command · GPIO.*

![IoTFlow — Lab 4](../courseware/assets/lab-04-control-device.png)

## Why the business cares

Monitoring tells you what happened. Control lets the system act without a person driving out to site — usually the single largest line in an IoT cost-benefit case.

## Prerequisites

- A free account on IoTFlow (https://iot.tertiaryinfotech.com).
- A modern browser. IoT hardware (ESP32/ESP8266) is optional — every lab can be completed with cURL or Python from any terminal.
- Your device token from Lab 1 (`dev_...`).
- Optional, for the scripted steps: Python 3 with `pip install "iotflow[mqtt]"`.

## Step-by-step

### Step 1 — Read your device's latest state from the terminal over the REST API and inspect the JSON reply — the platform returns the current value of every metric and virtual pin.

```bash
curl https://iot.tertiaryinfotech.com/api/device/state \
  -H "Authorization: Bearer dev_XXXXXXXXXXXX"
```

### Step 2 — Subscribe to your device's MQTT downlink topic to watch commands arrive in real time. Note the direction: uplink is telemetry, downlink is commands.

```bash
mosquitto_sub -h iot.tertiaryinfotech.com -p 1883 \
  -u device -P dev_XXXXXXXXXXXX -t "devices/<id>/down" -v
```

### Step 3 — Wire an LED to the Raspberry Pi: long leg to GPIO17 through a 330 Ω resistor, short leg to GND. A relay module in place of the LED switches a real appliance.

### Step 4 — On the Dashboard click Add widget and choose a Control type: Button (momentary), Switch (toggle), Slider (value) or Terminal (text).

### Step 5 — Assign the virtual pin the widget writes to — for example V1. For a slider also set the min/max range.

```bash
Virtual pin:  V1
```

### Step 6 — React to commands on the Pi with the iotflow client. Decorate a handler with @iot.on_command and drive the GPIO pin from inside it.

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

### Step 7 — For real-time control use the same handler over MQTT — loop_forever() keeps the connection open so commands arrive instantly instead of on the next poll.

```bash
iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="raspberry-pi-sensor-01",
              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)

@iot.on_command
def handle(pin, value, text): ...

iot.loop_forever()
```

### Step 8 — Flip the switch and drag the slider on the dashboard. The LED responds within a second — you are now controlling hardware from the cloud.

### Step 9 — Automate the response. In n8n, add a Webhook node to a new workflow, activate it and copy the Production URL.

### Step 10 — Back in IoTFlow, create an Automation: choose the trigger (telemetry received, alert fired, device online/offline, or command sent), narrow it by device and metric, then paste the n8n webhook URL and save.

### Step 11 — Use Test to send a sample payload to n8n and inspect the JSON the webhook receives, then enable live triggering.

### Step 12 — In n8n, branch the flow: send an Email or Telegram notification and append the reading to Google Sheets, so the event is both escalated and recorded for later analysis.

### Step 13 — Close the loop: add an HTTP Request node that sends a downlink command back to the Pi — for example switching a fan on when the temperature alert fires.

```bash
POST https://iot.tertiaryinfotech.com/api/device/command
{ "pin": "V1", "value": 1 }
```

### Step 14 — Secure what you have built: never commit the device token to source control, keep it in an environment variable, use TLS endpoints, and regenerate the token if it is ever exposed.

```bash
export IOTFLOW_TOKEN="dev_XXXXXXXXXXXX"   # not hard-coded in the script
```

### Step 15 — Monitor effectiveness: check that the alert fired, the notification arrived, the row was logged and the fan switched on. Record how long the whole loop took — that is your response time metric.

## Test it

Pushing a reading above the threshold fires the automation end to end: the notification arrives, a row is appended to the sheet, and the command sent back switches the LED/relay on the Raspberry Pi.

---
*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · www.tertiarycourses.com.sg*
