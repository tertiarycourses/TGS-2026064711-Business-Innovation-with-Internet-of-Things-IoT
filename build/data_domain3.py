"""
Topic 3 — IoT Data Analytics and Visualization (LO3 / A3, K4, K5).

Lab 3 of the IoTFlow lab set. Replaces the legacy ThingSpeak / MATLAB
visualisation labs from v14 of this course.

All labs run on IoTFlow — https://iot.tertiaryinfotech.com
Platform source: https://github.com/alfredang/iotplatform

The `steps` here drive the LEARNER GUIDE and the labs/*.md files only.
The slide deck shows the lab OVERVIEW + OUTCOME visually — never the steps.
"""

DOMAIN3 = [
    dict(
        num=3,
        topic=3,
        title="Analyse and Visualise Your IoT Data on the Cloud",
        image="lab-05-dashboard.png",
        objective="Use the platform's tools to analyse IoT data and record performance (A3, K4, K5).",
        desc=("Build a live dashboard from the readings your Raspberry Pi is streaming — number cards, gauges, "
              "line charts, LED indicators and a map — then interrogate the history to spot trends and set a "
              "threshold alert at the point where somebody would actually need to act."),
        build="A live monitoring dashboard for your Raspberry Pi, plus a working threshold alert rule",
        services="Display widgets · Number cards · Gauges · Line charts · Maps · Alert rules · Telemetry history",
        business=("This is the screen the supervisor actually looks at. A dashboard makes performance visible, and "
                  "an alert makes a problem timely instead of discovered too late."),
        steps=[
            ("On the Dashboard click Add widget. Widgets are grouped into Display (show data) and Control (send commands). Add a Number card bound to the temperature metric and give it a clear title.", ""),
            ("Add a Gauge for humidity with sensible min/max bounds (0–100 %). A gauge communicates 'where in the safe range are we' far better than a bare number.", ""),
            ("Add a Line chart for temperature to plot the history over time. This is where trends, drift and daily cycles become visible.", ""),
            ("Add an LED indicator for an on/off state, and a Map widget if your device reports a location. Arrange the layout — widgets snap to a responsive grid and refresh automatically every 5 seconds.", ""),
            ("Analyse the history rather than the instant: open the telemetry view and compare the last hour against the last day. Identify the normal operating range, and note the highest and lowest readings.", ""),
            ("Warm the sensor with your hand (or breathe on it) and watch the chart respond. Confirm the reading returns to baseline — this tells you the difference between a genuine event and sensor noise.", ""),
            ("Create an alert rule on a business-meaningful threshold — the value at which a person would need to act, not simply an unusual number.",
             'Alert rule:  temperature > 30  →  raise alert'),
            ("Add a device-offline rule so a Pi that stops reporting raises an alert instead of failing silently. Silent failure is the most common way an IoT deployment quietly stops delivering value.",
             'Alert rule:  device offline for 120 s  →  raise alert'),
            ("Trigger the alert deliberately: warm the sensor past your threshold and confirm the alert appears as Active on the dashboard, then resolve it.", ""),
            ("Record performance: note the readings, the alert that fired and the time it took to resolve. This log is the evidence base for judging whether the solution is effective (Topic 4).", ""),
        ],
        test=("Your dashboard shows live temperature, humidity and history from the Raspberry Pi, and crossing your "
              "threshold raises a visible Active alert that you can resolve."),
    ),
]
