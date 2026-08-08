"""
Topic 4 — Monitor Data to Trigger Control from Cloud (LO4 / A4, K6, K7).

Lab 4 of the IoTFlow lab set — reading data back, remote control over virtual
pins, and alert-driven n8n automation. Replaces the legacy Adafruit IO / IFTTT
labs from v14 of this course.

All labs run on IoTFlow — https://iot.tertiaryinfotech.com
Platform source: https://github.com/alfredang/iotplatform

The `steps` here drive the LEARNER GUIDE and the labs/*.md files only.
The slide deck shows the lab OVERVIEW + OUTCOME visually — never the steps.
"""

DOMAIN4 = [
    dict(
        num=4,
        topic=4,
        title="Monitor Data and Trigger Control on the Raspberry Pi",
        image="lab-04-control-device.png",
        objective="Monitor IoT data and trigger a control action on the device from the cloud (A4, K6, K7).",
        desc=("Read device state back out of the cloud over the REST API and MQTT, then add Control widgets "
              "(switch, slider) bound to virtual pins and drive an LED or relay on the Raspberry Pi from the "
              "dashboard. Reading data is monitoring; sending a command back is automation — and that is where "
              "the labour saving appears."),
        build="A dashboard switch and slider that control an LED/relay on the Raspberry Pi in real time",
        services="REST API (GET /api/device/state) · MQTT subscribe · Control widgets · Virtual pins · @on_command · GPIO",
        business=("Monitoring tells you what happened. Control lets the system act without a person driving out to "
                  "site — usually the single largest line in an IoT cost-benefit case."),
        steps=[
            ("Read your device's latest state from the terminal over the REST API and inspect the JSON reply — the platform returns the current value of every metric and virtual pin.",
             'curl https://iot.tertiaryinfotech.com/api/device/state \\\n  -H "Authorization: Bearer dev_XXXXXXXXXXXX"'),
            ("Subscribe to your device's MQTT downlink topic to watch commands arrive in real time. Note the direction: uplink is telemetry, downlink is commands.",
             'mosquitto_sub -h iot.tertiaryinfotech.com -p 1883 \\\n  -u device -P dev_XXXXXXXXXXXX -t "devices/<id>/down" -v'),
            ("Wire an LED to the Raspberry Pi: long leg to GPIO17 through a 330 Ω resistor, short leg to GND. A relay module in place of the LED switches a real appliance.", ""),
            ("On the Dashboard click Add widget and choose a Control type: Button (momentary), Switch (toggle), Slider (value) or Terminal (text).", ""),
            ("Assign the virtual pin the widget writes to — for example V1. For a slider also set the min/max range.", "Virtual pin:  V1"),
            ("React to commands on the Pi with the iotflow client. Decorate a handler with @iot.on_command and drive the GPIO pin from inside it.",
             'from iotflow import IoTFlow\nfrom gpiozero import LED\n\nled = LED(17)\niot = IoTFlow("https://iot.tertiaryinfotech.com", "dev_XXXXXXXXXXXX", "raspberry-pi-sensor-01")\n\n@iot.on_command\ndef handle(pin, value, text):\n    if pin == "V1":\n        led.on() if int(value) else led.off()\n\niot.run(interval=3)                   # blocks, polls every 3 s'),
            ("For real-time control use the same handler over MQTT — loop_forever() keeps the connection open so commands arrive instantly instead of on the next poll.",
             'iot = IoTFlow(token="dev_XXXXXXXXXXXX", device_id="raspberry-pi-sensor-01",\n              mqtt_host="iot.tertiaryinfotech.com", mqtt_port=1883)\n\n@iot.on_command\ndef handle(pin, value, text): ...\n\niot.loop_forever()'),
            ("Flip the switch and drag the slider on the dashboard. The LED responds within a second — you are now controlling hardware from the cloud.", ""),
            ("Automate the response. In n8n, add a Webhook node to a new workflow, activate it and copy the Production URL.", ""),
            ("Back in IoTFlow, create an Automation: choose the trigger (telemetry received, alert fired, device online/offline, or command sent), narrow it by device and metric, then paste the n8n webhook URL and save.", ""),
            ("Use Test to send a sample payload to n8n and inspect the JSON the webhook receives, then enable live triggering.", ""),
            ("In n8n, branch the flow: send an Email or Telegram notification and append the reading to Google Sheets, so the event is both escalated and recorded for later analysis.", ""),
            ("Close the loop: add an HTTP Request node that sends a downlink command back to the Pi — for example switching a fan on when the temperature alert fires.",
             'POST https://iot.tertiaryinfotech.com/api/device/command\n{ "pin": "V1", "value": 1 }'),
            ("Secure what you have built: never commit the device token to source control, keep it in an environment variable, use TLS endpoints, and regenerate the token if it is ever exposed.",
             'export IOTFLOW_TOKEN="dev_XXXXXXXXXXXX"   # not hard-coded in the script'),
            ("Monitor effectiveness: check that the alert fired, the notification arrived, the row was logged and the fan switched on. Record how long the whole loop took — that is your response time metric.", ""),
        ],
        test=("Pushing a reading above the threshold fires the automation end to end: the notification arrives, a "
              "row is appended to the sheet, and the command sent back switches the LED/relay on the Raspberry Pi."),
    ),
]
