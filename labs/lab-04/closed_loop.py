#!/usr/bin/env python3
"""
Lab 4 — Close the Loop (sense -> decide -> act)
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    Runs the full IoT business loop — sense, decide, act, verify — on one device
    in one file. The four stages are:

        1. SENSE   read the temperature and report it to IoTFlow
        2. DECIDE  compare it against the business threshold
        3. ACT     switch the cooling relay on or off via its virtual pin
        4. VERIFY  read state() back to confirm the command landed

    This is the same loop an n8n automation performs in the cloud — running it
    locally makes the logic visible, which is what you are assessed on.

RUN IT
    python closed_loop.py                     # threshold 30 °C
    python closed_loop.py --threshold 25

BUSINESS CONTEXT
    A dashboard needs a human to look at it. A closed loop does not — that is
    the difference between visibility and automation, and it is where the
    labour savings in your feasibility analysis come from.
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab-02"))
from send_telemetry_http import read_sensor  # noqa: E402  (same simulated sensor)

CYCLE_INTERVAL_S = 10


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the sense-decide-act loop.")
    parser.add_argument("--threshold", type=float, default=30.0,
                        help="switch cooling on above this temperature (default: 30)")
    args = parser.parse_args()

    if config.DEVICE_TOKEN.startswith("dev_XXX"):
        sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder.")

    iot = IoTFlow(config.SERVER, config.DEVICE_TOKEN, config.DEVICE_ID)

    print(f"Closed loop on {config.DEVICE_ID} — cooling ON above "
          f"{args.threshold} °C, every {CYCLE_INTERVAL_S}s. Ctrl+C to stop.\n")

    # Track what we last commanded so we only send a command on a real change.
    last_command: float | None = None

    try:
        while True:
            # 1. SENSE
            temperature, humidity = read_sensor()
            iot.send(temperature=temperature, humidity=humidity)

            # 2. DECIDE
            cooling = 1.0 if temperature > args.threshold else 0.0

            stamp = time.strftime("%H:%M:%S")
            print(f"[{stamp}] temperature={temperature:5.1f} -> "
                  f"cooling should be {'ON' if cooling else 'OFF'}")

            # 3. ACT — only when the decision actually changes, so we do not
            #    hammer the relay (and the platform) with redundant commands.
            if cooling != last_command:
                iot.virtual_write(config.CONTROL_PIN, cooling)
                print(f"           command sent: {config.CONTROL_PIN} = {cooling:.0f}")
                last_command = cooling

                # 4. VERIFY — read the cloud's view back.
                time.sleep(1)
                state = iot.state()
                print(f"           cloud state:  {state or '(empty)'}")

            time.sleep(CYCLE_INTERVAL_S)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
