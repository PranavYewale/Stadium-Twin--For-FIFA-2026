# FIFA World Cup 2026 Stadium Digital Twin AI OS

A production-quality, real-time stadium management system. It acts as an intelligent operating system for a FIFA World Cup 2026 venue. It monitors crowds, ticketing, transit, parking, concessions, weather, safety alerts, and energy grids, simulates predictions, and applies Google Gemini reasoning to automate dispatcher guidance and fan assistant queries.

---

## Technical Features

1.  **3D digital Twin Interface**: Rendered interactively with Three.js (color-coded stands/gates, clickable sectors for detailed inspection).
2.  **Live Heatmap GIS Tracking**: Rendered with Leaflet.js utilizing cartographical overlays ofMetLife Stadium perimeter (crowd density expansion rings, coordinates tracking).
3.  **Real-Time Data Streams**: WebSocket connection using Flask-SocketIO pushes updates every 3 seconds representing IoT and computer vision cameras.
4.  **Forecasting Predictors**: Regression modules that calculate queue congestion and risk indicators 15, 30, and 60 minutes out.
5.  **Gemini AI Brain Integration**: Takes real-time state telemetry, predicts bottleneck scenarios, and yields structured operational priorities, volunteer dispatches, and public bilingual announcements. (Falls back to dynamic offline local simulation if API key is not configured).
6.  **Fan Assistant Portal**: NLP simulation answering transit pathing, concessions stock levels, lost & found coordinates, and emergency guidelines.
7.  **PDF Analytics Exporter**: Generates visual PDF stadium summaries.

---

## Directory Architecture

```
digital_twin_ai/
├── app.py                     # Main server and WebSocket routing
├── config.py                  # Environment properties
├── requirements.txt           # Python dependencies
├── database/
│   └── models.py              # User, Zone, Alert, Prediction, Sustainability schemas
├── routes/
│   ├── dashboard.py           # Dashboard rendering & auth
│   ├── prediction.py          # Forecast telemetry endpoints
│   ├── emergency.py           # Emergency triggers & alarms
│   ├── analytics.py           # Report compilation & PDF downloads
│   └── api.py                 # REST API endpoints (GET/POST/PUT/DELETE)
├── services/
│   ├── simulation.py          # Core background simulation thread loop
│   ├── camera.py              # Computer Vision simulator
│   ├── iot.py                 # Power / Water load monitor
│   └── [weather/parking/...]  # Auxiliary sensor simulators
├── ai/
│   ├── gemini.py              # Gemini model interface & prompts
│   ├── prediction_engine.py   # Regression forecasting
│   ├── risk_engine.py         # Risk & color status indexer
│   └── report_generator.py    # ReportLab PDF compile engine
└── templates/                 # Glassmorphic Dark UI HTML layouts
```

---

## Setup & Running Instructions

### 1. Configure the Environment
Ensure Python 3.10+ is installed. Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate
```

Install requirements:
```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key (Optional)
If you want to use the live Google Gemini API, set your API key in the shell environment:
```powershell
$env:GEMINI_API_KEY="your-gemini-api-key-here"
```
*Note: If the key is not set, the platform will automatically activate the local AI Simulation Engine to generate high-fidelity, situation-specific recommendations.*

### 3. Seed and Run the Application
Start the Flask development server:
```bash
python app.py
```

Once running, navigate your web browser to:
[http://localhost:5000/](http://localhost:5000/)

#### Authorization Credentials:
- Username: `admin` (or `operator` / `security` / `volunteer` / `medical`)
- Password: `worldcup2026`
