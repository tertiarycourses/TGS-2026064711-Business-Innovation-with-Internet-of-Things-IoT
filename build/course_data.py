"""
SINGLE SOURCE OF TRUTH — IoT with Raspberry Pi.

WSQ Course Code: TGS-2020505433
TSC: EVS-TEM-4002-1.1 Internet of Things Management (Level 4)

Formerly delivered as "Mastering Raspberry Pi: Hands-On Practical Applications
for Beginners" (v14). The course has been retitled to "IoT with Raspberry Pi"
and every hands-on lab has been replaced with the IoTFlow labs
(https://iot.tertiaryinfotech.com — https://github.com/alfredang/iotplatform),
retiring the legacy ThingSpeak / Adafruit IO / Node-RED lab set.

Every artifact — the slide deck (PPT), Lesson Plan (LP), Learner Guide (LG) and
the labs/ folder — is generated from the data in this module plus
data_domain1.py … data_domain4.py, so titles, learning-unit numbering,
activities, learning outcomes and the schedule can never drift apart.

Course structure: TWO training days of 8 hours each (16 h total), plus a
2-hour final assessment, per the approved Course Proposal
(CA-WSQ-2020-010764).

All hands-on labs run on IoTFlow — https://iot.tertiaryinfotech.com
"""

# ------------------------------------------------------------------ metadata
TITLE        = "IoT with Raspberry Pi"
SHORT_TITLE  = "IoT with Raspberry Pi"                 # used in output filenames
COURSE_CODE  = "TGS-2020505433"
VERSION      = "v15.0"
VERSION_DATE = "8 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 2

# TSC reference (printed on the Skills Framework slide + LP/LG)
TSC_TITLE = "Internet of Things Management"
TSC_CODE  = "EVS-TEM-4002-1.1"
TSC_DESC  = ("Manage the deployment of Internet of Things (IoT) solutions, including the collection and "
             "analysis of data from connected sensors and devices, to monitor and control equipment and "
             "the environment, and to drive process improvement.")

# The IoT platform every lab runs on
PLATFORM      = "IoTFlow"
PLATFORM_URL  = "https://iot.tertiaryinfotech.com"
PLATFORM_DOCS = "https://iot.tertiaryinfotech.com/tutorials"
PLATFORM_REPO = "https://github.com/alfredang/iotplatform"

# The hardware used in class
HARDWARE      = "Raspberry Pi"
HARDWARE_ALT  = "Raspberry Pi Pico W"

# ------------------------------------------------------------------ TSC abilities & knowledge
ABILITIES = [
    ("A1", "Analyse relevant data to recommend control actions"),
    ("A2", "Identify areas for implementing IoT solutions for process improvement"),
    ("A3", "Use relevant tool to analyse and record performance"),
    ("A4", "Monitor the effectiveness of IoT solutions"),
]
KNOWLEDGE = [
    ("K1", "IoT concept and technical knowledge of IoT implementation"),
    ("K2", "Connectivity in devices using sensors, smart devices and other technologies for data collection and communication"),
    ("K3", "Equipment automation"),
    ("K4", "Building and/or Environment automation"),
    ("K5", "Advanced process control"),
    ("K6", "Security and privacy applications for IoT"),
    ("K7", "IoT guidelines and communication standards"),
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Analyse the uses and functions of IoT technologies. (A1, K1)",
    "LO2: Collect environment data with Raspberry Pi and post the data to cloud computing. (A2, K2, K3)",
    "LO3: Use cloud computing to analyse and visualise IoT data. (A3, K4, K5)",
    "LO4: Monitor data and trigger control on devices. (A4, K6, K7)",
]

# ------------------------------------------------------------------ topics (= learning units)
# num, code, title, subtitle, weighting (LP time), concept bullets for the section
TOPICS = [
    dict(num=1, code="01",
         title="Overview of Internet of Things (IoT)",
         subtitle="Industry 4.0 · What IoT is · Sensors & actuators · Wireless technologies · Use cases",
         weighting="LO1 · A1, K1 · Day 1 AM",
         concepts=[
            ("Industry 4.0", "Steam, electricity, computers and now cyber-physical systems — assets report their own state in real time."),
            ("What IoT is", "A network of physical objects embedded with sensors and connectivity that collect and exchange data."),
            ("The four building blocks", "Sensors/devices capture data, connectivity moves it, cloud processes it, a UI acts on it."),
            ("Sensors and actuators", "Sensors turn a physical phenomenon into a signal; actuators turn a decision back into physical action."),
            ("Wireless technologies", "WiFi, BLE, Zigbee, LoRaWAN, NB-IoT and 5G trade range against power, bandwidth and cost."),
            ("Types of IoT", "Consumer, commercial, industrial (IIoT) and infrastructure IoT each serve a different context."),
         ]),
    dict(num=2, code="02",
         title="Collect and Post Environmental Data to Cloud",
         subtitle="Cloud platforms · Raspberry Pi · Sensors · Device tokens · HTTP REST & MQTT uplink",
         weighting="LO2 · A2, K2, K3 · Day 1 PM",
         concepts=[
            ("Cloud computing for IoT", "The cloud gives constrained devices the storage, compute and availability they lack."),
            ("IoTFlow", "Our platform: projects, devices, tokens, dashboards, alerts and automations in one place."),
            ("Raspberry Pi as gateway", "A low-cost Linux computer with GPIO, WiFi and Python — it reads sensors and speaks to the cloud."),
            ("Reading environmental data", "Temperature, humidity and pressure from a Sense HAT, DHT11/DHT22 or a simulated source."),
            ("Device tokens", "A token authenticates every message a device sends — and is why credential management matters."),
            ("HTTP REST & MQTT uplink", "POST JSON to a REST endpoint, or publish over MQTT for lightweight real-time streaming."),
         ]),
    dict(num=3, code="03",
         title="IoT Data Analytics and Visualization",
         subtitle="Dashboards · Number cards, gauges & charts · Maps · Alert rules · Analysing trends",
         weighting="LO3 · A3, K4, K5 · Day 2 AM",
         concepts=[
            ("Why visualise", "A dashboard turns a stream of raw readings into an operational picture a manager can act on."),
            ("Display widgets", "Number cards, gauges, line and bar charts, LED indicators and maps, refreshed automatically."),
            ("Analysing the data", "Compare current readings against history to spot trends, drift and abnormal behaviour."),
            ("Alert rules", "Threshold and device-offline rules fire the moment a reading crosses a business-meaningful limit."),
            ("Recording performance", "Telemetry history is the evidence base for measuring whether the solution actually works."),
            ("From data to decision", "Analytics only pays off when a reading changes what somebody — or something — does next."),
         ]),
    dict(num=4, code="04",
         title="Monitor Data to Trigger Control from Cloud",
         subtitle="Downlink control · Virtual pins · Automations & n8n · Monitoring effectiveness · IoT security",
         weighting="LO4 · A4, K6, K7 · Day 2 PM",
         concepts=[
            ("Reading data back", "Query the current state of every metric and virtual pin over the REST API or MQTT."),
            ("Downlink control", "Virtual pins carry commands from the dashboard back to the device to switch a relay or set a value."),
            ("Closing the loop", "Monitoring tells you what happened; control lets the system act without anyone driving to site."),
            ("Automation with n8n", "Alerts fire a webhook into a low-code workflow that notifies, logs, and can ask AI to recommend."),
            ("Monitoring effectiveness", "Track uptime, alert response and the metric you set out to improve — then tune the rules."),
            ("IoT security", "Constrained, unattended devices with physical consequences — protect tokens, transport and firmware."),
         ]),
]

# ------------------------------------------------------------------ discussion activities
# Topics 1, 3 and 4 carry a facilitated discussion in addition to the hands-on labs.
DISCUSSIONS = [
    dict(topic=1, code="A1",
         title="Discussion — Analyse an IoT Use Case",
         mins=20,
         brief=("In pairs, pick one of the IoT use cases covered (healthcare, agriculture, connected vehicles, "
                "smart home, smart city, smart building, logistics, manufacturing or retail) and analyse how the "
                "data collected leads to a recommended control action."),
         prompts=[
            "What is physically being sensed, how often, and by what kind of sensor?",
            "Which wireless technology suits that deployment — and why does range or power decide it?",
            "What control action does the data recommend, and who or what carries it out?",
            "What would the organisation lose if that measurement did not exist?",
         ],
         output="A short analysis linking the sensed data to a specific recommended control action."),
    dict(topic=3, code="A3",
         title="Discussion — Design Your Monitoring Dashboard",
         mins=20,
         brief=("Working from the data your Raspberry Pi is now streaming, decide what a supervisor actually needs "
                "to see on one screen, and which threshold would justify interrupting somebody."),
         prompts=[
            "Which three widgets earn their place on the screen, and what does each one answer?",
            "What is the normal operating range, and at what value does it become a problem?",
            "How would you tell a genuine fault apart from a single noisy reading?",
            "What performance record would you need to prove the solution is working?",
         ],
         output="A dashboard layout plus one justified alert threshold with its rationale."),
    dict(topic=4, code="A4",
         title="Discussion — Monitor Effectiveness and Manage Risk",
         mins=20,
         brief=("Take the IoT solution you have built across the labs and plan how you would monitor its "
                "effectiveness in production — and how you would secure it."),
         prompts=[
            "Which metrics tell you the solution is working — uptime, response time, or the business outcome?",
            "How would you know a device had silently stopped reporting?",
            "Where are the credentials in your solution, and what happens if one leaks?",
            "Which standard or guideline would you cite when asked how the data is protected?",
         ],
         output="A monitoring and security plan: the effectiveness metrics, the offline strategy, and the top three risks."),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "IoT Foundations and Collecting Data — From Sensor to Cloud",
    2: "Analytics, Visualisation and Control — From Data to Action",
}

# ------------------------------------------------------------------ assessment
# Per the approved Course Proposal: WA(Q&A) 60 min + Practical Performance 60 min = 2 h
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (Q&A), 60 minutes, open book. Covers K1–K7.",
    practical="Practical Performance (PP) — 60 minutes, open book, individually completed. Covers A1–A4.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
