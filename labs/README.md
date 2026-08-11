# Hands-On Labs — Business Innovation with Internet-of-Things (IoT)

**WSQ Course Code:** TGS-2026064711 · Conducted by Tertiary Infotech Academy Pte Ltd (UEN 201200696W)

All labs run on our IoT platform **IoTFlow** — https://iot.tertiaryinfotech.com — and are completed during the 90-minute practical block in Topic 3. Work through them in order; each lab builds on the one before.

Full step-by-step instructions are also in the Learner Guide. The slide deck shows each lab's purpose and outcome only.

Each lab is a folder: `README.md` has the instructions, and the `.py` files next to it are runnable IoTFlow scripts built on the official `iotflow` Python package.

## Setup (once, before Lab 1)

```bash
pip install -r requirements.txt   # installs iotflow[mqtt]
cp config.example.py config.py    # paste your device token from Lab 1
```

`config.py` is git-ignored — your device token never leaves your machine. HTTP-mode scripts need no third-party package at all; only the MQTT scripts need the `[mqtt]` extra.

## Topic 03 — IoT Technology  (LO3 · A3, K2 · 60 min + 90 min practical)

- [Lab 1: Register Your First IoT Device on IoTFlow](lab-01/README.md) — A registered IoT device in your own IoTFlow project, with its device token saved  
  Scripts: `verify_device.py`
- [Lab 2: Post Business Data to the Cloud (HTTP & MQTT)](lab-02/README.md) — Live temperature and humidity telemetry streaming into IoTFlow from terminal and Python  
  Scripts: `send_telemetry_http.py`, `send_telemetry_mqtt.py`
- [Lab 3: Read Data Back and Remotely Control the Asset](lab-03/README.md) — A dashboard switch and slider that control a relay/LED on the device in real time  
  Scripts: `control_http.py`, `control_mqtt.py`, `read_state.py`
- [Lab 4: Turn IoT Data into Business Insight](lab-04/README.md) — A monitoring dashboard plus an alert-driven n8n workflow with an AI summary and a downlink command  
  Scripts: `closed_loop.py`, `simulate_breach.py`

---
*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · www.tertiarycourses.com.sg*
