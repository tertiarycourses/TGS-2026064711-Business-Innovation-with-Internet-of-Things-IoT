"""
Topic 2 — Collect and Post Environmental Data to Cloud (LO2 / A2, K2, K3).

Labs 1 and 2 of the IoTFlow lab set, adapted for Raspberry Pi. These replace the
legacy ThingSpeak / MATLAB labs from v14 of this course.

All labs run on IoTFlow — https://iot.tertiaryinfotech.com
Platform source: https://github.com/alfredang/iotplatform

The `steps` here drive the LEARNER GUIDE and the labs/*.md files only.
The slide deck shows the lab OVERVIEW + OUTCOME visually — never the steps.
"""

DOMAIN2 = [
    dict(
        num=1,
        topic=2,
        title="Register Your Raspberry Pi on IoTFlow",
        image="lab-01-add-device.png",
        objective="Identify an area for an IoT solution and connect the asset to the cloud (A2, K2).",
        desc=("Turn your Raspberry Pi into a managed IoT device. You sign in to IoTFlow, create a project "
              "workspace for your monitoring scenario, register the Pi through the Add Device wizard, choose how "
              "it will talk to the cloud (HTTP or MQTT), and capture the device token that authenticates every "
              "message it sends."),
        build="A registered Raspberry Pi device in your own IoTFlow project, with its device token saved",
        services="IoTFlow projects · Add Device wizard · Device tokens · HTTP & MQTT",
        business=("This is the first step of any IoT deployment: an asset that was previously invisible now has an "
                  "identity, an owner and a data stream that can be measured, monitored and managed."),
        steps=[
            ("Open the IoTFlow platform at https://iot.tertiaryinfotech.com and sign up for a free account, or log in if you already have one.", ""),
            ("Create a project — a self-contained workspace with its own dashboard, alerts, map and automations. Name it after your monitoring scenario, e.g. 'Environment Monitoring' or 'Smart Classroom'.", ""),
            ("Click Add Device in the sidebar and give the device a descriptive name that identifies the physical unit.", "Device name:  Raspberry Pi Sensor 01"),
            ("Work through the guided wizard and choose a protocol. HTTP is the simplest — POST JSON to a REST endpoint. MQTT is a lightweight publish/subscribe protocol, better for real-time control and many devices. Both stay available afterwards.", ""),
            ("Copy the device token shown when the device is created. It is displayed only once — save it somewhere safe on your Pi.", "dev_XXXXXXXXXXXX"),
            ("Note how the token authenticates every message the device sends. Anyone holding the token can post as that device, which is exactly why device credential management is an IoT security concern (Topic 4).", "Authorization: Bearer dev_XXXXXXXXXXXX"),
            ("Prepare the Raspberry Pi: boot Raspberry Pi OS, connect it to WiFi, and confirm you can reach the internet. If you are working headless, enable SSH or VNC from Preferences → Raspberry Pi Configuration → Interfaces.", "ping -c 3 iot.tertiaryinfotech.com"),
        ],
        test=("Your Raspberry Pi appears in the project's device list, and its Integrate page shows code snippets "
              "pre-filled with your endpoint and device token."),
    ),
    dict(
        num=2,
        topic=2,
        title="Collect Environmental Data and Post It to the Cloud",
        image="lab-02-send-reading.png",
        objective="Collect environment data with the Raspberry Pi and post it to cloud computing (A2, K2, K3).",
        desc=("Read temperature and humidity on the Raspberry Pi and stream the readings to IoTFlow — first with a "
              "single cURL call, then with the official Python client over HTTP, then continuously over MQTT. This "
              "is the uplink every IoT solution depends on: without a reliable data stream there is nothing to "
              "analyse."),
        build="Live temperature and humidity telemetry streaming from the Raspberry Pi into IoTFlow",
        services="Sense HAT / DHT22 · Telemetry REST API · Python client (pip install iotflow) · MQTT broker",
        business=("Each reading is an operational fact with a timestamp. Once the stream exists, the organisation "
                  "can answer questions it previously could not — how often, how long, how bad, and at what cost."),
        steps=[
            ("Open the Integrate page for your device. Every snippet on it is pre-filled with your endpoint and device token.", ""),
            ("Send your first reading from the Raspberry Pi terminal with cURL over HTTP POST, to prove connectivity before adding any sensor code.",
             'curl -X POST https://iot.tertiaryinfotech.com/api/telemetry \\\n  -H "Authorization: Bearer dev_XXXXXXXXXXXX" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"temperature": 28.5, "humidity": 65}\''),
            ("Open the Dashboard. The reading appears under Latest Telemetry within seconds — widgets auto-refresh every 5 seconds.", ""),
            ("Install the official IoTFlow Python client on the Pi from PyPI.",
             'pip install "iotflow[mqtt]"      # with real-time MQTT (paho-mqtt)\npip install iotflow               # HTTP only — zero dependencies'),
            ("Read the real sensor. With a Sense HAT, use the sense_hat library — it gives temperature, humidity and pressure from one board.",
             'from sense_hat import SenseHat\n\nsense = SenseHat()\ntemperature = round(sense.get_temperature(), 1)\nhumidity    = round(sense.get_humidity(), 1)\npressure    = round(sense.get_pressure(), 1)\nprint(temperature, humidity, pressure)'),
            ("No Sense HAT? Use a DHT11/DHT22 on a GPIO pin instead — the rest of the lab is identical.",
             'import adafruit_dht, board\n\ndht = adafruit_dht.DHT22(board.D4)     # data pin on GPIO4\ntemperature = dht.temperature\nhumidity    = dht.humidity'),
            ("Post the sensor readings to IoTFlow over HTTP — several metrics at once with send(), or one at a time with virtual_write().",
             'from iotflow import IoTFlow\n\niot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "raspberry-pi-sensor-01")\niot.send(temperature=temperature, humidity=humidity, pressure=pressure)\niot.virtual_write("temperature", temperature)   # or one at a time'),
            ("Stream continuously over MQTT. connect() runs MQTT in the background and mqtt_publish() sends a reading every few seconds — this is the shape of a real production sensor.",
             'iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="raspberry-pi-sensor-01",\n              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)\niot.connect()                    # MQTT runs in the background\nwhile True:\n    iot.mqtt_publish(temperature=sense.get_temperature(),\n                     humidity=sense.get_humidity())\n    time.sleep(10)'),
            ("Keep it running unattended: start the script at boot with systemd so the Pi resumes reporting after a power cut.",
             'sudo systemctl enable --now iotflow-sensor.service'),
        ],
        test=("Every value the Raspberry Pi sends appears in the Dashboard's Latest Telemetry within seconds, and "
              "the device's telemetry history grows with each reading."),
    ),
]
