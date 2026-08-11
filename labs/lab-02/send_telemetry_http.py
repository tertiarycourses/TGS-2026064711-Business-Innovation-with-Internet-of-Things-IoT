#!/usr/bin/env python3
"""
Lab 2 — Post Business Data to the Cloud (HTTP)
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    Sends readings to IoTFlow over plain HTTP — the simplest uplink there is.
    It shows both ways of reporting a value:
        send(...)          several metrics in one request
        virtual_write(...) one metric at a time

    HTTP mode needs no extra packages at all: the client uses only the Python
    standard library.

RUN IT
    python send_telemetry_http.py            # one batch of readings
    python send_telemetry_http.py --loop     # a reading every 10 seconds

BUSINESS CONTEXT
    Each reading is an operational fact with a timestamp. Once this stream
    exists, the business can finally ask how often, how long, how bad — and at
    what cost.
"""
import argparse
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import config
except ImportError:
    sys.exit("Missing config.py — run:  cp ../config.example.py ../config.py")

from iotflow import IoTFlow

PUBLISH_INTERVAL_S = 10


def read_sensor() -> tuple[float, float]:
    """Stand in for a real sensor.

    On an ESP32/Raspberry Pi you would read a DHT22 or BME280 here. The rest of
    the script does not change — which is the point: the business logic is the
    same whether the number comes from silicon or from random().
    """
    return round(random.uniform(18.0, 32.0), 1), round(random.uniform(40.0, 75.0), 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Send telemetry to IoTFlow over HTTP.")
    parser.add_argument("--loop", action="store_true",
                        help=f"keep sending every {PUBLISH_INTERVAL_S} seconds")
    args = parser.parse_args()

    if config.DEVICE_TOKEN.startswith("dev_XXX"):
        sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder.")

    iot = IoTFlow(config.SERVER, config.DEVICE_TOKEN, config.DEVICE_ID)

    # --- several metrics in a single request --------------------------------
    temperature, humidity = read_sensor()
    ok = iot.send(temperature=temperature, humidity=humidity, voltage=3.7)
    print(f"send()          temperature={temperature} humidity={humidity} -> "
          f"{'OK' if ok else 'FAILED'}")

    # --- one metric at a time -----------------------------------------------
    # virtual_write is just send() for a single named metric. The metric name is
    # what you bind a dashboard widget to, so keep it stable.
    ok = iot.virtual_write("temperature", temperature)
    print(f"virtual_write() temperature={temperature} -> {'OK' if ok else 'FAILED'}")

    if not args.loop:
        print("\nOpen the Dashboard — the values appear under Latest Telemetry "
              "within about 5 seconds.")
        print("Tip: run with --loop to watch a live chart build up.")
        return 0

    # --- continuous mode: the shape of a real production sensor -------------
    print(f"\nLooping every {PUBLISH_INTERVAL_S}s — press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(PUBLISH_INTERVAL_S)
            temperature, humidity = read_sensor()
            ok = iot.send(temperature=temperature, humidity=humidity)
            stamp = time.strftime("%H:%M:%S")
            print(f"[{stamp}] temperature={temperature} humidity={humidity} -> "
                  f"{'OK' if ok else 'FAILED'}")
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
