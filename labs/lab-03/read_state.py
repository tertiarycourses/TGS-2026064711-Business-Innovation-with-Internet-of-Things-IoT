#!/usr/bin/env python3
"""
Lab 3 — Read Data Back from the Cloud
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    Reads your device's current virtual-pin state back out of IoTFlow with
    state(). These are the values the DASHBOARD sets — the switches and sliders
    you added — not the telemetry the device sent up.

        uplink   device  -> cloud   (telemetry, Lab 2)
        downlink cloud   -> device  (commands, this lab)

RUN IT
    python read_state.py            # print the state once
    python read_state.py --watch    # poll every 3s and print changes

    While it runs, flip a Switch on your dashboard and watch the value change.

BUSINESS CONTEXT
    Reading state back is what lets a device recover after a reboot: it asks the
    cloud "what should I be doing?" instead of guessing.
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import config
except ImportError:
    sys.exit("Missing config.py — run:  cp ../config.example.py ../config.py")

from iotflow import IoTFlow

POLL_INTERVAL_S = 3


def show(state: dict) -> None:
    if not state:
        print("  (no control pins set yet — add a Switch or Slider widget on "
              "the dashboard and move it)")
        return
    for pin, value in sorted(state.items()):
        print(f"  {pin:<12} = {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read virtual-pin state from IoTFlow.")
    parser.add_argument("--watch", action="store_true",
                        help=f"poll every {POLL_INTERVAL_S}s and print changes")
    args = parser.parse_args()

    if config.DEVICE_TOKEN.startswith("dev_XXX"):
        sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder.")

    iot = IoTFlow(config.SERVER, config.DEVICE_TOKEN, config.DEVICE_ID)

    print(f"Current control-pin state for {config.DEVICE_ID}:")
    show(iot.state())

    if not args.watch:
        print("\nTip: run with --watch, then flip a Switch on the dashboard.")
        return 0

    print(f"\nWatching every {POLL_INTERVAL_S}s — Ctrl+C to stop.")
    previous = iot.state()
    try:
        while True:
            time.sleep(POLL_INTERVAL_S)
            current = iot.state()
            # Report only what actually moved, so the output stays readable.
            for pin, value in sorted(current.items()):
                if previous.get(pin) != value:
                    stamp = time.strftime("%H:%M:%S")
                    print(f"[{stamp}] {pin} changed: {previous.get(pin)} -> {value}")
            previous = current
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
