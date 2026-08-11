#!/usr/bin/env python3
"""
Lab 3 — Remotely Control the Asset (HTTP polling)
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    Reacts to the dashboard's Switch and Slider widgets. You register a handler
    with the @iot.on_command decorator, then iot.run() polls the cloud and calls
    your handler whenever a pin CHANGES.

    This is the HTTP version — no extra packages needed, but a command only
    arrives on the next poll (up to `interval` seconds late). For instant
    response use control_mqtt.py.

RUN IT
    python control_http.py

    Then flip the Switch and drag the Slider on your IoTFlow dashboard.

BUSINESS CONTEXT
    Monitoring tells you what happened; control means the system acts without
    anyone driving to the site. That avoided truck roll is usually the largest
    single line in an IoT cost-benefit case.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import config
except ImportError:
    sys.exit("Missing config.py — run:  cp ../config.example.py ../config.py")

from iotflow import IoTFlow

POLL_INTERVAL_S = 3

if config.DEVICE_TOKEN.startswith("dev_XXX"):
    sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder.")

iot = IoTFlow(config.SERVER, config.DEVICE_TOKEN, config.DEVICE_ID)


@iot.on_command
def handle(pin: str, value: float, text: str | None) -> None:
    """Called once per pin change.

    pin   the virtual pin the widget writes to, e.g. "V1"
    value always a float — a Switch sends 0.0 or 1.0, a Slider its position
    text  the string payload of a Terminal widget, otherwise None
    """
    if pin == config.CONTROL_PIN:
        # A Switch is on/off; treat anything non-zero as ON.
        state = "ON" if value else "OFF"
        print(f"  relay ({pin}) -> {state}")
        # On real hardware you would drive a GPIO here, e.g.:
        #   GPIO.output(RELAY_PIN, GPIO.HIGH if value else GPIO.LOW)
    elif pin == "brightness":
        print(f"  dimmer -> {value:.0f}%")
    else:
        print(f"  {pin} -> {value}" + (f" (text={text!r})" if text else ""))


def main() -> int:
    print(f"Listening for commands on {config.DEVICE_ID} "
          f"(polling every {POLL_INTERVAL_S}s).")
    print("Flip the Switch or drag the Slider on your dashboard. Ctrl+C to stop.\n")
    try:
        # run() blocks forever, polling state() and dispatching changes.
        iot.run(interval=POLL_INTERVAL_S)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
