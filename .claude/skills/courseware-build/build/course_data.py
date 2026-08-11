"""
SINGLE SOURCE OF TRUTH — Business Innovation with Internet-of-Things (IoT).

WSQ Course Code: TGS-2026064711
TSC: ICT-SNA-4003-1.1 Business Innovation (Level 4)

Every artifact — the slide deck (PPT), Lesson Plan (LP), Learner Guide (LG) and
the labs/ folder — is generated from the data in this module plus
data_domain1.py … data_domain5.py, so titles, learning-unit numbering,
activities, learning outcomes and the schedule can never drift apart.

Course structure is taken from the approved Course Proposal
(CA-WSQ-2020-007388): ONE training day of 8 hours =
  5.0 h Classroom Facilitation + 1.5 h Practical/Practicum + 1.5 h Assessment.

All hands-on labs run on IoTFlow — https://iot.tertiaryinfotech.com
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Business Innovation with Internet-of-Things (IoT)"
SHORT_TITLE  = "Business Innovation with IoT"          # used in output filenames
COURSE_CODE  = "TGS-2026064711"
VERSION      = "v10.1"
VERSION_DATE = "11 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 1

# TSC reference (printed on the Skills Framework slide + LP/LG)
TSC_TITLE = "Business Innovation"
TSC_CODE  = "ICT-SNA-4003-1.1"
TSC_DESC  = ("Identify and evaluate digitisation and innovative business opportunities provided by "
             "new advancements in information and communication technology to establish new services "
             "or businesses to bridge the physical and digital worlds.")

# The IoT platform every lab runs on
PLATFORM      = "IoTFlow"
PLATFORM_URL  = "https://iot.tertiaryinfotech.com"
PLATFORM_DOCS = "https://iot.tertiaryinfotech.com/tutorials"

# ------------------------------------------------------------------ TSC abilities & knowledge
ABILITIES = [
    ("A1", "Compare current business model for the organisation with the other business models in the industry"),
    ("A2", "Explore potential opportunities for business innovation to be introduced within the organisation"),
    ("A3", "Identify ways in which digitisation can be applied to the business"),
    ("A4", "Conduct feasibility analysis and weigh the costs-benefits of potential business innovation opportunities"),
    ("A5", "Implement business innovation processes in line with a defined action plan"),
]
KNOWLEDGE = [
    ("K1", "New and emerging innovative business processes / models deployed in the industry"),
    ("K2", "Concept and principles of digitisation"),
    ("K3", "Factors to consider to assess the viability of business innovation for a given organisation context"),
    ("K4", "Success factors for implementation of business innovation"),
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Compare the organisation's current business model with emerging IoT-enabled business models in the industry. (A1, K1)",
    "LO2: Explore potential opportunities for business innovation using IoT across industry use cases. (A2, K1)",
    "LO3: Identify how IoT works and the ways digitisation can be applied to the business. (A3, K2)",
    "LO4: Conduct a feasibility analysis and weigh the costs and benefits of adopting IoT. (A4, K3)",
    "LO5: Implement business innovation processes with IoT in line with a defined action plan. (A5, K4)",
]

# ------------------------------------------------------------------ topics (= learning units)
# num, code, title, subtitle, weighting (LP time), concept bullets for the section
TOPICS = [
    dict(num=1, code="01",
         title="Overview of Internet of Things (IoT)",
         subtitle="Industry 4.0 · IoT business models · Sensors & actuators · Wireless technologies",
         weighting="LO1 · A1, K1 · 60 min",
         concepts=[
            ("Industry 4.0", "IoT, AI, 5G, cloud and robotics converge so physical assets report their own state in real time."),
            ("What IoT is", "Connecting everyday objects to the internet to cut cost, lift productivity and open new revenue."),
            ("The four building blocks", "Sensors/devices capture data, connectivity moves it, cloud processes it, a UI acts on it."),
            ("Why now", "Cheap sensors, long-range low-power wireless and 5G removed the cost barrier to mass adoption."),
            ("Product to service", "IoT shifts firms from one-off product sales to subscription, outcome and pay-per-use models."),
            ("Data as the asset", "The recurring value is the telemetry stream, not the device — it compounds over time."),
         ]),
    dict(num=2, code="02",
         title="Potential Opportunities of IoT Innovation",
         subtitle="Agriculture · Autonomous vehicles · Logistics · Smart buildings · Healthcare · Drones",
         weighting="LO2 · A2, K1 · 60 min",
         concepts=[
            ("Agriculture", "Soil, weather and crop sensing drive precision irrigation and fertiliser decisions — e.g. IBM AgroPad."),
            ("Autonomous vehicles", "Vehicle telemetry and sensor fusion enable driver assistance and highly automated driving."),
            ("Logistics & fleet", "Location, temperature and fuel telemetry give end-to-end shipment visibility and route optimisation."),
            ("Smart buildings", "Occupancy, energy and equipment sensing cut utility cost and enable predictive maintenance."),
            ("Healthcare & wearables", "Continuous patient monitoring feeds records securely, supporting earlier clinical intervention."),
            ("Drones", "Aerial inspection, survey and delivery reach places people cannot, safely and at lower cost."),
         ]),
    dict(num=3, code="03",
         title="IoT Technology",
         subtitle="Cloud platforms · Post data · Read & control · Analytics & visualisation · Automation",
         weighting="LO3 · A3, K2 · 60 min + 90 min practical",
         concepts=[
            ("Cloud for IoT", "A platform ingests telemetry, stores history, visualises it and triggers actions — no servers to run."),
            ("IoTFlow", "Our platform: projects, devices, tokens, dashboards, alerts and automations in one place."),
            ("Uplink: posting data", "Devices POST readings over HTTP REST or publish over MQTT, authenticated by a device token."),
            ("Downlink: control", "Virtual pins carry commands from the dashboard back to the device to switch a relay or set a value."),
            ("Analytics & visualisation", "Number cards, gauges, charts and maps turn raw readings into an operational picture."),
            ("Automation & AI", "Rules and n8n workflows notify, log and let AI summarise readings and recommend an action."),
         ]),
    dict(num=4, code="04",
         title="IoT Adoption",
         subtitle="Adoption challenges · IoT security · Edge computing · Cost-benefit analysis",
         weighting="LO4 · A4, K3 · 60 min",
         concepts=[
            ("Barriers to adoption", "Data privacy, security, cost, skills gaps, weak standards and interoperability with legacy systems."),
            ("Why IoT security differs", "Constrained devices, long unattended lifetimes and physical consequences to a breach."),
            ("Mirai botnet", "Default credentials on cameras and routers built a botnet that took down much of the US east coast."),
            ("Edge computing", "Processing near the source cuts latency, bandwidth and cost, and keeps sensitive data local."),
            ("Falling hardware cost", "Sensor, gateway and connectivity prices keep dropping, improving the business case each year."),
            ("Cost-benefit analysis", "Weigh hardware, connectivity, platform and integration against savings, uptime and new revenue."),
         ]),
    dict(num=5, code="05",
         title="IoT Implementation",
         subtitle="Success factors · Design thinking · A 7-step action plan",
         weighting="LO5 · A5, K4 · 60 min",
         concepts=[
            ("Lead with business value", "Start from the business outcome IoT delivers, not from the technology itself."),
            ("Strategic alignment", "The initiative must serve the business strategy and respect technology constraints."),
            ("Business process focus", "Integrate IoT into existing workflows so the new way is clearly better than today."),
            ("Operating model & capability", "Value networks and new skills are needed; give people a common IoT language."),
            ("Security by design", "Build end-to-end security in from the start — it is a selection criterion, not an add-on."),
            ("Design thinking", "Empathise, Define, Ideate, Prototype, Test — start small, prove value, then scale."),
         ]),
]

# ------------------------------------------------------------------ discussion activities
# Topics 1, 2, 4 and 5 are delivered by lecture + didactic questioning + facilitated
# discussion (no hands-on lab). These are the in-class activities the Lesson Plan
# schedules and the Learner Guide writes up. Each maps to the ability it develops.
DISCUSSIONS = [
    dict(topic=1, code="A1",
         title="Discussion — Compare Business Models",
         mins=15,
         brief=("In pairs, describe how your organisation earns revenue today. Then pick one IoT-enabled "
                "competitor or industry example and compare the two."),
         prompts=[
            "How does your organisation make money today — product sale, project fee, subscription?",
            "Which IoT-enabled model could apply: outcome-based, pay-per-use, subscription, or predictive service?",
            "What data would you need to collect before that model becomes possible?",
            "What would customers gain, and what would they be willing to pay for?",
         ],
         output="A short written comparison of your current model against one IoT-enabled model."),
    dict(topic=2, code="A2",
         title="Discussion — Spot an IoT Opportunity",
         mins=15,
         brief=("Working from the six industry use cases, identify one process in your own organisation that "
                "is currently invisible, manual or reactive, and could be sensed instead."),
         prompts=[
            "Which process today relies on someone physically checking something?",
            "What would you measure, how often, and who would act on the reading?",
            "What is the cost of the current blind spot — downtime, spoilage, overtime, penalties?",
            "Which of the six use cases is closest to your scenario, and what can you borrow from it?",
         ],
         output="One clearly stated IoT opportunity: the asset, the measurement, and the decision it improves."),
    dict(topic=4, code="A4",
         title="Discussion — Cost-Benefit Analysis",
         mins=20,
         brief=("Take the opportunity you identified in Topic 2 and build a first-pass feasibility and "
                "cost-benefit case for it, including the security and privacy risks."),
         prompts=[
            "Costs: devices, connectivity, platform subscription, integration, installation, maintenance.",
            "Benefits: labour saved, downtime avoided, energy or wastage reduced, new revenue enabled.",
            "Risks: data privacy, device security, interoperability with legacy systems, skills gaps.",
            "Roughly how long before the benefits exceed the costs — and what would break that estimate?",
         ],
         output="A cost-benefit summary with an estimated payback period and the top three risks."),
    dict(topic=5, code="A5",
         title="Discussion — Your Implementation Action Plan",
         mins=20,
         brief=("Apply design thinking and the success factors to turn your opportunity into a staged action "
                "plan you could actually pitch to management."),
         prompts=[
            "Empathise & Define: whose problem is this, and how would you state it in one sentence?",
            "Ideate & Prototype: what is the smallest pilot that proves the value — one device, one site?",
            "Test & scale: what measurable result would justify rolling it out further?",
            "Which success factor is weakest in your organisation today, and how will you address it?",
         ],
         output="A staged action plan: pilot scope, success measure, owner, and the case for scaling."),
]

# ------------------------------------------------------------------ day theme (single 8-hour day)
DAY_THEMES = {
    1: "IoT Business Innovation — Opportunity, Technology, Adoption & Implementation",
}

# ------------------------------------------------------------------ assessment
# Per the approved Course Proposal: WA(Q&A) 75 min + Oral Questioning 15 min = 90 min (1.5 h)
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (Q&A), 75 minutes, open book. Covers A1–A5.",
    practical="Oral Questioning (OQ) — 15 minutes, 1:1 with the assessor, open book. Covers K1–K4.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
