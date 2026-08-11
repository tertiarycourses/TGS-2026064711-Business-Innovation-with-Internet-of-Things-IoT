#!/usr/bin/env python3
"""
Lab 2 — Post Business Data to the Cloud (MQTT)
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    Streams the same readings as send_telemetry_http.py, but over MQTT — a
    lightweight publish/subscribe protocol built for fleets of devices.

    connect()      opens the MQTT connection in a background thread
    mqtt_publish() pushes a reading down that open connection

    HTTP opens a new connection for every reading; MQTT keeps one open. Over
    thousands of devices that difference is the battery and the bandwidth bill.

BEFORE YOU RUN IT
    pip install "iotflow[mqtt]"        # the [mqtt] extra adds paho-mqtt

RUN IT
    python send_telemetry_mqtt.py

BUSINESS CONTEXT
    This is the uplink a real deployment uses. Cost per device per month is a
    line in the feasibility analysis you build in Topic 4.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import config
except ImportError:
    sys.exit("Missing config.py — run:  cp ../config.example.py ../config.py")

from iotflow import IoTFlow

from send_telemetry_http import read_sensor  # same simulated sensor as the HTTP lab

PUBLISH_INTERVAL_S = 10


def main() -> int:
    if config.DEVICE_TOKEN.startswith("dev_XXX"):
        sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder.")

    # mqtt_host / mqtt_port are keyword-only arguments on the client.
    iot = IoTFlow(
        config.SERVER,
        config.DEVICE_TOKEN,
        config.DEVICE_ID,
        mqtt_host=config.MQTT_HOST,
        mqtt_port=config.MQTT_PORT,
    )

    print(f"Connecting to MQTT broker {config.MQTT_HOST}:{config.MQTT_PORT} …")
    try:
        # connect() is non-blocking: the client keeps the socket alive on a
        # background thread so this script stays free to do its own work.
        iot.connect()
    except RuntimeError as e:
        # Raised when paho-mqtt is missing or mqtt_host was never set.
        sys.exit(f"MQTT setup failed: {e}\n"
                 'Install the MQTT extra with:  pip install "iotflow[mqtt]"')
    except OSError as e:
        # The broker refused the connection or could not be reached.
        sys.exit(f"Could not reach the MQTT broker at "
                 f"{config.MQTT_HOST}:{config.MQTT_PORT} — {e}\n"
                 "Check MQTT_HOST/MQTT_PORT in ../config.py, and that your "
                 "network allows outbound port 1883 (many corporate and campus "
                 "Wi-Fi networks block it — use HTTP mode instead: "
                 "python send_telemetry_http.py --loop).")

    print(f"Connected. Publishing every {PUBLISH_INTERVAL_S}s — Ctrl+C to stop.\n")
    try:
        while True:
            temperature, humidity = read_sensor()
            iot.mqtt_publish(temperature=temperature, humidity=humidity, voltage=3.7)
            stamp = time.strftime("%H:%M:%S")
            print(f"[{stamp}] published temperature={temperature} humidity={humidity}")
            time.sleep(PUBLISH_INTERVAL_S)
    except KeyboardInterrupt:
        print("\nStopping …")
    finally:
        # Always close the connection cleanly so the broker does not hold a
        # stale session for this device.
        iot.disconnect()
        print("Disconnected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
