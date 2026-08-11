"""
Shared lab settings — copy this file to config.py and fill in your own values.

    cp config.example.py config.py

Every lab script imports from here, so you paste your device token ONCE and all
four labs work. config.py is git-ignored so your token is never committed.

Where the values come from:
  SERVER        the IoTFlow platform URL (leave as-is for the class)
  DEVICE_TOKEN  shown ONCE when you create the device in Lab 1 (starts dev_)
  DEVICE_ID     the device name you chose in Lab 1
  MQTT_HOST     same host as the platform, used by the MQTT labs
"""

SERVER = "https://iot.tertiaryinfotech.com"

# --- paste these two from Lab 1 -------------------------------------------
DEVICE_TOKEN = "dev_XXXXXXXXXXXX"
DEVICE_ID = "cold-room-sensor-01"

# --- MQTT (Labs 2 and 3) ---------------------------------------------------
MQTT_HOST = "iot.tertiaryinfotech.com"
MQTT_PORT = 1883

# --- the virtual pin the dashboard Switch/Slider writes to (Lab 3) ---------
CONTROL_PIN = "V1"
