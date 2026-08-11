#!/usr/bin/env python3
"""
Lab 4 — Turn IoT Data into Business Insight (fire the alert)
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    Drives a temperature excursion on purpose so you can watch your alert
    pipeline fire end to end. The chain it exercises is:

        this script -> IoTFlow alert rule -> Automation -> n8n webhook
                    -> email/Telegram + Google Sheet + AI summary

    It ramps the temperature from a normal value up through your alert
    threshold, holds it there, then cools back down — the shape of a real
    cold-room door being left open.

RUN IT
    python simulate_breach.py                 # ramp through 30 °C
    python simulate_breach.py --threshold 25  # match your own alert rule

BUSINESS CONTEXT
    An alert is only worth building if someone acts on it. This is the rehearsal
    that proves the whole chain — sensor to decision — actually works.
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

STEP_INTERVAL_S = 5


def ramp(start: float, end: float, steps: int) -> list[float]:
    """Evenly spaced values from start to end, inclusive."""
    if steps < 2:
        return [end]
    stride = (end - start) / (steps - 1)
    return [round(start + stride * i, 1) for i in range(steps)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Simulate a temperature excursion to fire your IoTFlow alert.")
    parser.add_argument("--threshold", type=float, default=30.0,
                        help="the alert threshold set in IoTFlow (default: 30)")
    parser.add_argument("--hold", type=int, default=3,
                        help="readings to send above the threshold (default: 3)")
    args = parser.parse_args()

    if config.DEVICE_TOKEN.startswith("dev_XXX"):
        sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder.")

    iot = IoTFlow(config.SERVER, config.DEVICE_TOKEN, config.DEVICE_ID)

    # Climb from comfortably normal to clearly over the line, hold, then recover.
    normal = args.threshold - 8
    peak = args.threshold + 3
    sequence = (ramp(normal, peak, 6)
                + [peak] * args.hold
                + ramp(peak, normal, 4))

    print(f"Alert threshold ... {args.threshold} °C")
    print(f"Device ............ {config.DEVICE_ID}")
    print(f"Sending {len(sequence)} readings, one every {STEP_INTERVAL_S}s. "
          "Ctrl+C to stop.\n")

    try:
        for temperature in sequence:
            ok = iot.send(temperature=temperature, humidity=65)
            stamp = time.strftime("%H:%M:%S")
            flag = "  <-- OVER THRESHOLD" if temperature > args.threshold else ""
            print(f"[{stamp}] temperature={temperature:5.1f} "
                  f"{'OK' if ok else 'FAILED'}{flag}")
            time.sleep(STEP_INTERVAL_S)
    except KeyboardInterrupt:
        print("\nStopped early.")
        return 0

    print("\nDone. Now check that every stage fired:")
    print("  1. IoTFlow  — the alert shows in the project's alert list")
    print("  2. n8n      — the workflow has a new successful execution")
    print("  3. Inbox    — the notification email / Telegram message arrived")
    print("  4. Sheet    — a row was appended with the reading")
    print("  5. AI node  — the summary recommends an action")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
