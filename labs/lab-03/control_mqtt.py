#!/usr/bin/env python3
"""
Lab 3 — Remotely Control the Asset (real-time MQTT)
Business Innovation with Internet-of-Things (IoT) · TGS-2026064711

WHAT THIS SCRIPT DOES
    The same @on_command handler as control_http.py, but delivered over MQTT.
    The handler code is IDENTICAL — only the transport changes:

        control_http.py   iot.run(interval=3)   command arrives within 3s
        control_mqtt.py   iot.loop_forever()    command arrives immediately

    loop_forever() subscribes to the device's downlink topic and blocks,
    dispatching each command the moment the broker delivers it.

BEFORE YOU RUN IT
    pip install "iotflow[mqtt]"

RUN IT
    python control_mqtt.py

    Drag the dashboard Slider and watch the values stream in with no lag.

BUSINESS CONTEXT
    Latency decides which use cases are viable. A 3-second delay is fine for a
    thermostat and unacceptable for a safety interlock.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    import config
except ImportError:
    sys.exit("Missing config.py — run:  cp ../config.example.py ../config.py")

from iotflow import IoTFlow

if config.DEVICE_TOKEN.startswith("dev_XXX"):
    sys.exit("Edit ../config.py first — DEVICE_TOKEN is still the placeholder.")

iot = IoTFlow(
    config.SERVER,
    config.DEVICE_TOKEN,
    config.DEVICE_ID,
    mqtt_host=config.MQTT_HOST,
    mqtt_port=config.MQTT_PORT,
)


@iot.on_command
def handle(pin: str, value: float, text: str | None) -> None:
    """Identical to the HTTP version — the handler does not care how the
    command reached it. That portability is the whole point of the client."""
    if pin == config.CONTROL_PIN:
        state = "ON" if value else "OFF"
        print(f"  relay ({pin}) -> {state}")
    else:
        print(f"  {pin} -> {value}" + (f" (text={text!r})" if text else ""))


def main() -> int:
    print(f"Subscribing to downlink commands for {config.DEVICE_ID} over MQTT "
          f"({config.MQTT_HOST}:{config.MQTT_PORT}).")
    print("Flip the Switch or drag the Slider on your dashboard. Ctrl+C to stop.\n")
    try:
        # Blocks forever; commands are dispatched to handle() as they arrive.
        iot.loop_forever()
    except RuntimeError as e:
        # paho-mqtt missing, or mqtt_host was never set.
        sys.exit(f"MQTT setup failed: {e}\n"
                 'Install the MQTT extra with:  pip install "iotflow[mqtt]"')
    except OSError as e:
        # The broker refused the connection or could not be reached.
        sys.exit(f"Could not reach the MQTT broker at "
                 f"{config.MQTT_HOST}:{config.MQTT_PORT} — {e}\n"
                 "Check MQTT_HOST/MQTT_PORT in ../config.py, and that your "
                 "network allows outbound port 1883 (many corporate and campus "
                 "Wi-Fi networks block it — use the HTTP version instead: "
                 "python control_http.py).")
    except KeyboardInterrupt:
        print("\nStopping …")
        iot.disconnect()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
