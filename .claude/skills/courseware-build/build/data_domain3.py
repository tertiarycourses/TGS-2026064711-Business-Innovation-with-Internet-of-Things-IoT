"""
Topic 3 — IoT Technology: the hands-on practical block (90 minutes, LO3 / A3, K2).

This is the ONLY practical block in this one-day course, per the approved Course
Proposal (5 h classroom + 1.5 h practical + 1.5 h assessment). The four labs are
adapted from TGS-2020504020 "Internet of Things (IoT) Fundamental for Beginners"
and all run on IoTFlow — https://iot.tertiaryinfotech.com

Each lab is deliberately business-framed: the learner does not just wire a
sensor, they see how the data becomes a decision — which is what A3 ("identify
ways in which digitisation can be applied to the business") is assessed on.

The `steps` here drive the LEARNER GUIDE and the labs/*.md files only.
The slide deck shows the lab OVERVIEW + OUTCOME visually — never the steps.
"""

DOMAIN3 = [
    dict(
        num=1,
        topic=3,
        title="Register Your First IoT Device on IoTFlow",
        image="lab-01-add-device.png",
        objective="Identify how digitisation is applied to a business asset by connecting it to the cloud (A3, K2).",
        desc=("Turn a physical asset into a digital one. You sign in to IoTFlow, create a project workspace for "
              "your business scenario, register a device through the Add Device wizard, choose how it will talk to "
              "the cloud (HTTP or MQTT), and capture the device token that authenticates every message it sends."),
        build="A registered IoT device in your own IoTFlow project, with its device token saved",
        services="IoTFlow projects · Add Device wizard · Device tokens · HTTP & MQTT",
        business=("This is the first step of digitisation: an asset that was previously invisible to the business "
                  "now has an identity, an owner and a data stream that can be measured and managed."),
        steps=[
            ("Open the IoTFlow platform at https://iot.tertiaryinfotech.com and sign up for a free account, or log in if you already have one.", ""),
            ("Create a project — a self-contained workspace with its own dashboard, alerts, map and automations. Name it after your business scenario, e.g. 'Cold Chain Monitoring' or 'Smart Office'.", ""),
            ("Click Add Device in the sidebar and give the device a descriptive, business-meaningful name.", "Device name:  Cold Room Sensor 01"),
            ("Work through the guided wizard and choose a protocol. HTTP is the simplest — POST JSON to a REST endpoint. MQTT is a lightweight publish/subscribe protocol, better for many devices and real-time control. Both stay available afterwards.", ""),
            ("Copy the device token shown when the device is created. It is displayed only once — save it somewhere safe.", "dev_XXXXXXXXXXXX"),
            ("Note how the token authenticates every message the device sends. Anyone holding the token can post as that device, which is exactly why device credential management is an IoT security concern (Topic 4).", "Authorization: Bearer dev_XXXXXXXXXXXX"),
        ],
        test=("Your new device appears in the project's device list, and its Integrate page shows code snippets "
              "pre-filled with your endpoint and device token."),
    ),
    dict(
        num=2,
        topic=3,
        title="Post Business Data to the Cloud (HTTP & MQTT)",
        image="lab-02-send-reading.png",
        objective="Apply digitisation by streaming operational data from the asset to the cloud (A3, K2).",
        desc=("Send readings to IoTFlow three different ways — cURL from any terminal, the Python client, and "
              "(optionally) an ESP32/ESP8266 over MQTT — and watch them arrive live. This is the uplink that "
              "every IoT business case depends on: without a reliable data stream there is nothing to analyse."),
        build="Live temperature and humidity telemetry streaming into IoTFlow from terminal and Python",
        services="Telemetry REST API · Python client (pip install iotflow) · MQTT broker · ESP32/ESP8266",
        business=("Each reading is an operational fact with a timestamp. Once the stream exists, the business can "
                  "ask questions it previously could not answer — how often, how long, how bad, and at what cost."),
        steps=[
            ("Open the Integrate page for your device. Every snippet on it is pre-filled with your endpoint and device token.", ""),
            ("Send your first reading from any terminal with cURL over HTTP POST.",
             'curl -X POST https://iot.tertiaryinfotech.com/api/telemetry \\\n  -H "Authorization: Bearer dev_XXXXXXXXXXXX" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"temperature": 22.5, "humidity": 60}\''),
            ("Open the Dashboard. The reading appears under Latest Telemetry within seconds — widgets auto-refresh every 5 seconds.", ""),
            ("Install the official IoTFlow Python client from PyPI.",
             'pip install "iotflow[mqtt]"      # with real-time MQTT (paho-mqtt)\npip install iotflow               # HTTP only — zero dependencies'),
            ("Send readings from Python over HTTP — several metrics at once with send(), or one at a time with virtual_write().",
             'from iotflow import IoTFlow\n\niot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "cold-room-sensor-01")\niot.send(temperature=22.5, humidity=60)      # several metrics at once\niot.virtual_write("temperature", 22.5)       # or one at a time'),
            ("Stream continuously over MQTT with the telemetry_upload.py example — download it, fill in your broker host, device id and device token, then run it.",
             'curl -O https://raw.githubusercontent.com/alfredang/iotplatform/main/clients/python/examples/telemetry_upload.py\n# edit: MQTT_BROKER = "iot.tertiaryinfotech.com", DEVICE_ID, DEVICE_TOKEN\npython telemetry_upload.py'),
            ("Study the loop inside telemetry_upload.py — connect() runs MQTT in the background and mqtt_publish() sends a reading every 10 seconds. This is the shape of a real production sensor.",
             'iot = IoTFlow(token=DEVICE_TOKEN, device_id=DEVICE_ID,\n              mqtt_host=MQTT_BROKER, mqtt_port=MQTT_PORT)\niot.connect()                    # MQTT runs in the background\nwhile True:\n    iot.mqtt_publish(temperature=temperature, humidity=humidity, voltage=3.7)\n    time.sleep(PUBLISH_INTERVAL_S)'),
            ("Hardware alternative (optional): flash the ESP8266_Telemetry_Upload Arduino sketch. The Arduino library speaks the same protocol as the Python client, so the dashboard cannot tell the difference.",
             'IoTFlow.virtualWrite("temperature", t);   // metric name binds to dashboard widgets'),
        ],
        test=("Every value you send appears in the Dashboard's Latest Telemetry within seconds, and the device's "
              "telemetry history grows with each reading."),
    ),
    dict(
        num=3,
        topic=3,
        title="Read Data Back and Remotely Control the Asset",
        image="lab-04-control-device.png",
        objective="Close the loop between cloud data and physical action — the basis of an IoT business process (A3, K2).",
        desc=("Read device state back out of the cloud over the REST API and MQTT, then add Control widgets "
              "(switch, slider) bound to virtual pins and drive the device from the dashboard. Reading data is "
              "monitoring; sending commands back is automation — and that is where the labour savings appear."),
        build="A dashboard switch and slider that control a relay/LED on the device in real time",
        services="REST API (GET /api/device/state) · MQTT subscribe · Control widgets · Virtual pins · @on_command",
        business=("Monitoring tells you what happened. Control lets the system act without a person driving out to "
                  "the site — this is usually the single largest line in an IoT cost-benefit case."),
        steps=[
            ("Read your device's latest state from any terminal over the REST API, and inspect the JSON reply — the platform returns the current value of every metric and virtual pin.",
             'curl https://iot.tertiaryinfotech.com/api/device/state \\\n  -H "Authorization: Bearer dev_XXXXXXXXXXXX"'),
            ("Subscribe to your device's MQTT downlink topic to watch commands and data arrive in real time. Note the direction: uplink is telemetry, downlink is commands.",
             'mosquitto_sub -h iot.tertiaryinfotech.com -p 1883 \\\n  -u device -P dev_XXXXXXXXXXXX -t "devices/<id>/down" -v'),
            ("On the Dashboard click Add widget and choose a Control type: Button (momentary), Switch (toggle), Slider (value) or Terminal (text).", ""),
            ("Assign the virtual pin the widget writes to — for example V1, relay or pump. For a slider also set the min/max range.", "Virtual pin:  V1"),
            ("React to commands in Python with the iotflow client. Decorate a handler with @iot.on_command and poll over HTTP — no extra dependencies needed.",
             'from iotflow import IoTFlow\n\niot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "cold-room-sensor-01")\n\n@iot.on_command\ndef handle(pin, value, text):\n    if pin == "V1":\n        print("relay ->", value)      # drive a GPIO here\n\niot.run(interval=3)                   # blocks, polls every 3 s'),
            ("For real-time control use the same handler over MQTT — loop_forever() keeps the connection open so commands arrive instantly instead of on the next poll.",
             'iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="cold-room-sensor-01",\n              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)\n\n@iot.on_command\ndef handle(pin, value, text): ...\n\niot.loop_forever()'),
            ("Flip the switch and drag the slider on the dashboard. Commands are delivered to the device immediately and the relay/LED responds. The same events can also trigger automations (Lab 4).", ""),
        ],
        test=("Toggling the dashboard switch changes the relay/LED state within a second, and the slider value "
              "arrives in your @on_command handler as you drag it."),
    ),
    dict(
        num=4,
        topic=3,
        title="Turn IoT Data into Business Insight",
        image="lab-05-dashboard.png",
        objective="Use analytics, visualisation and automation to turn raw telemetry into a business decision (A3, K2).",
        desc=("Build a live dashboard from your readings — number cards, gauges, charts, LED indicators and maps — "
              "then set a threshold alert and hand it to an n8n workflow that notifies the team, logs the event and "
              "asks an AI node to summarise the readings and recommend an action."),
        build="A monitoring dashboard plus an alert-driven n8n workflow with an AI summary and a downlink command",
        services="Display widgets · Alert rules · IoTFlow Automations · n8n Webhook · Email/Telegram · Google Sheets · AI nodes",
        business=("This is the slide the board actually sees. A dashboard makes performance visible, an alert makes "
                  "it timely, and the AI summary turns a stream of numbers into a recommended action."),
        steps=[
            ("On the Dashboard click Add widget. Widgets are grouped into Display (show data) and Control (send commands). Add a Number card for temperature and give it a clear title.", ""),
            ("Add a Gauge for humidity with sensible min/max bounds (0–100 %), then a Line chart to plot the temperature history over time.", ""),
            ("Add an LED indicator for on/off state, and a Map widget if your device reports a location. Arrange the layout — widgets snap to a responsive grid and refresh automatically.", ""),
            ("Create an alert rule on a business-meaningful threshold — the point at which someone would need to act.", "Alert rule:  temperature > 30  →  fire automation"),
            ("In n8n, add a Webhook node to a new workflow, activate the workflow and copy the Production URL.", ""),
            ("Back in IoTFlow, create an Automation, choose the trigger type (telemetry received, alert fired, device online/offline, or command sent), optionally narrow it by device and metric, then paste the n8n webhook URL and save.", ""),
            ("Use Test to send a sample payload to n8n and inspect the JSON the webhook receives, then enable live triggering.", ""),
            ("In n8n, branch the flow: send an Email/Telegram notification and append the reading to Google Sheets so the event is both escalated and recorded.", ""),
            ("Add an AI node that summarises the recent readings and recommends an action — analytics with no code, and the output a manager can read.", ""),
            ("Close the loop: add an HTTP Request node that sends a downlink command back to the device, for example switching a fan or compressor on.",
             'POST https://iot.tertiaryinfotech.com/api/device/command\n{ "pin": "V1", "value": 1 }'),
        ],
        test=("Pushing a reading above the threshold fires the n8n workflow: the notification arrives, a row is "
              "appended to the sheet, the AI summary is generated, and the device reacts to the command sent back."),
    ),
]
