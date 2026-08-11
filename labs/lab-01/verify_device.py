#!/usr/bin/env python3
"""
Lab 1 — Register Your First IoT Device on IoTFlow
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    Proves that the device you just registered on the IoTFlow dashboard is real:
    it authenticates with your device token and sends one "hello" reading.
    If it prints OK, your token is valid and every later lab will work.

BEFORE YOU RUN IT
    1. pip install iotflow
    2. cp ../config.example.py ../config.py
    3. Paste your DEVICE_TOKEN and DEVICE_ID into ../config.py

RUN IT
    python verify_device.py

BUSINESS CONTEXT
    This is the moment an ordinary asset becomes a digital one: it now has an
    identity, an owner and a data stream the business can measure and manage.
"""
import sys
from pathlib import Path

# Let this script import config.py from the labs/ folder one level up.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import config
except ImportError:
    sys.exit("Missing config.py — run:  cp ../config.example.py ../config.py  "
             "then paste in your device token from the Add Device wizard.")

from iotflow import IoTFlow


def main() -> int:
    if config.DEVICE_TOKEN.startswith("dev_XXX"):
        sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder. "
                 "Copy the real token from IoTFlow (it is shown only once).")

    # The first positional argument is the server URL, then the token, then the
    # device id — the same three values shown on the device's Integrate page.
    iot = IoTFlow(config.SERVER, config.DEVICE_TOKEN, config.DEVICE_ID)

    print(f"Server ....... {config.SERVER}")
    print(f"Device ....... {config.DEVICE_ID}")
    print(f"Token ........ {config.DEVICE_TOKEN[:8]}…  (masked)")
    print("Sending a test reading …")

    # send() returns True only when the platform accepted the reading, so a
    # False here means the token is wrong or the device was deleted.
    ok = iot.send(temperature=22.5, humidity=60)

    if ok:
        print("\nOK — the platform accepted the reading.")
        print("Open your IoTFlow Dashboard: the value appears under Latest "
              "Telemetry within about 5 seconds.")
        return 0

    print("\nFAILED — the platform rejected the reading.")
    print("Check that DEVICE_TOKEN is copied in full and that the device still "
          "exists in your project.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
