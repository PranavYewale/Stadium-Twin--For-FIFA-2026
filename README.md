# 🏟️ Arena.Twin OS - Stadium Digital Twin AI Console

> **Imagine a video game dashboard, but for a real-life giant sports stadium! That is Arena.Twin.**

Arena.Twin is an intelligent operating system built for a FIFA World Cup 2026 stadium. It acts like a "magic mirror"—a digital model that connects to simulated sensors, ticketing gates, security feeds, and transit hubs to show operators exactly what is happening in real-time, predict crowd bottlenecks before they happen, and use Google Gemini AI to suggest smart solutions!

> [!IMPORTANT]
> **Prototype Disclaimer**: This project is a **high-fidelity operational prototype**. It runs on simulated IoT data and mock camera feeds to demonstrate stadium control center features, emergency drill training, and AI decision-making.

---

## 📸 Interface Preview

* [Placeholder: Main Operator Console Overview]<img width="1918" height="908" alt="image" src="https://github.com/user-attachments/assets/930bd4cd-f677-4043-82ad-b398d6388a21" />

* [Placeholder: 3D Twin & Live GIS Map]<img width="1287" height="656" alt="image" src="https://github.com/user-attachments/assets/885e9d20-5a03-41cf-9a80-5ca533dbda45" />

* [Placeholder: AI Queue Optimizer & Lost Child Dispatcher]<img width="830" height="299" alt="image" src="https://github.com/user-attachments/assets/a5df1e40-45c8-4c9a-9993-1481e0414598" />


---

## 🧠 What does what? (The Operator Dashboard)

Here is a simple breakdown of the widgets on your screen, how to use them, and why they help:

| Section | What is it? | How to use it? | How does it help? |
| :--- | :--- | :--- | :--- |
| **3D Digital Twin** | A glowing 3D miniature model of the stadium stands. | **Left-click** to rotate, zoom, and inspect different tiers. | The stands glow **Green** (empty/normal), **Yellow** (filling up), or **Red** (overcrowded) so you spot problems instantly. |
| **GIS Perimeter Map** | A live tracking map of gates, transit lines, and parking. | Drag to pan, scroll to zoom. Watch for flashing red circles. | Pins show live locations. Flashing red dots show where emergency teams or missing people are spotted. |
| **Real-time Dynamics** | Two interactive line charts showing crowds and power usage. | Read the flowing lines to watch trends over the last few minutes. | Helps track if stands are filling up too fast, or if the stadium is wasting water and electricity. |
| **System Log Console** | A scrolling stream of text messages at the bottom. | Read the log lines. Colored lines represent warnings (yellow) or emergencies (red). | Tells the operator exactly what is happening second-by-second (e.g. *"VIP gate ticket scanned"*). |
| **Gemini OS Brain** | An AI decision-making assistant powered by Google Gemini. | Read the "Core Analysis" and click **Read Aloud** to hear the public announcement. | Autonomously suggests where to deploy staff and broadcasts safety warnings in multiple languages. |
| **Emergency Command** | Two action buttons: **Simulate Alert** and **Reset**. | Click **Simulate Alert** to test evacuation. Click **Reset** to restore normalcy. | Evacuates the stadium during training drills. Resetting clears all alarms and returns the crowd to normal. |
| **Simulation Control Panel** | A controls deck to change weather, crowd size, temperature, or grid power. | Press buttons (e.g. *Heatwave* or *Trigger Power Outage*) and watch the dashboard react! | Allows operators to test different scenarios to make sure the stadium is ready for anything. |

---

## 🛠️ Specialist Assistant Tabs

At the right-center of the console is a tabbed toolbox. Switching tabs unlocks smart specialized operations:

### 1. 🎯 Zone Tech
*   **What it does**: Displays detailed statistics (spectator count, temperature, queue wait times) for the selected stand or gate.
*   **How it helps**: Gives operators granular telemetry for any single coordinate they click on the 3D model or map.

### 2. 👶 Lost Child Radar
*   **What it does**: Lets you type in a missing child's name, shirt color, and last seen gate.
*   **How it helps**: Automatically runs a camera feed scan, predicts where they walked based on crowd flow, notifies volunteer nodes, and flashes a pulsing red radar circle on the Leaflet map!

### 3. ♿ Accessible Transit Router
*   **What it does**: Computes step-free, wheelchair-friendly routes from parking lots to seats.
*   **How it helps**: Predicts elevator wait times and provides voice-guided turn-by-turn directions for visually impaired fans.

### 4. 🧮 AI Queue Optimizer
*   **What it does**: Monitors concession stand queue delays and forecasts 15-minute wait times.
*   **How it helps**: Clicking **Balance Grid** reallocates registers and staff from less crowded stalls to busy ones, lowering wait times instantly.

### 5. 💬 Fan Assistance Portal
*   **What it does**: A smart multilingual chatbot that fans can talk to (or use voice input).
*   **How it helps**: Instantly answers questions about transport schedules, nearest restrooms, gates, and concessions.

---

## 📁 Project Architecture

```text
digital_twin_ai/
├── app.py                     # Main server, database seeder, and WebSockets loop
├── config.py                  # Server configuration properties
├── requirements.txt           # Python library dependencies
├── verify_digital_twin.py     # Auto-testing script to check all API endpoints
├── database/
│   └── models.py              # SQLite Database schemas (User, Zone, Alert, Sustainability)
├── routes/
│   ├── dashboard.py           # Login auth and dashboard views pager
│   ├── prediction.py          # Crowd prediction APIs
│   ├── emergency.py           # Emergency trigger & reset APIs
│   ├── analytics.py           # Report PDF compilation routes
│   └── api.py                 # Core REST APIs (lost-child, accessibility, simulator overrides)
├── services/
│   ├── simulation.py          # Background simulator ticker thread (ticks every 3 seconds)
│   ├── camera.py              # Computer Vision simulator rolls
│   ├── iot.py                 # Electricity/HVAC utility monitors
│   └── [weather/parking/...]  # External sensor models
├── ai/
│   ├── gemini.py              # Google Gemini LLM API connection (with offline simulation backup)
│   ├── prediction_engine.py   # Regression forecasting logic (15-60m out)
│   ├── risk_engine.py         # Multi-factor risk calculation
│   └── report_generator.py    # ReportLab PDF generator
└── templates/                 # UI HTML templates (landing page, dashboard, login)
```

---

## 🚀 How to Run the App (Step-by-Step)

Follow these simple steps to boot the stadium console:

### Step 1: Set Up Python
Ensure you have Python 3.10+ installed. Open a terminal/powershell inside this folder, create a virtual environment, and activate it:
```bash
python -m venv venv
# On Windows Powershell:
.\venv\Scripts\Activate.ps1
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Libraries
Install the required code dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Gemini API Key (Optional)
If you have a Google Gemini API Key, set it in your terminal environment:
```powershell
# On Windows Powershell:
$env:GEMINI_API_KEY="your-api-key-here"
# On Mac/Linux:
export GEMINI_API_KEY="your-api-key-here"
```
*Note: If you do not have a key, don't worry! The application automatically falls back to a high-fidelity local AI decision simulator that outputs situation-specific guidance.*

### Step 4: Run the Server
Start your Flask server:
```bash
python app.py
```

### Step 5: Open in Browser
Open your web browser and navigate to:
👉 **[http://localhost:5000/](http://localhost:5000/)**

#### Default Login Credentials:
*   **Username**: `admin` (or `operator` / `security` / `volunteer` / `medical`)
*   **Password**: `worldcup2026`

---

## 🧪 Automated Testing
We have included a full test suite to check that all routes, simulation parameters, and assistant modules compile and calculate values correctly. You can trigger it anytime:
```bash
python verify_digital_twin.py
```
