# 🚦 AI Vehicle Traffic Prediction - Smart City Jaunpur

An AI-powered Smart Traffic Management System designed specifically for **Jaunpur City** to predict traffic congestion, optimize signal timers, and assist Traffic Police & Municipal Council.

**Live Demo (Frontend):** https://jaunpur-traffic-ai-prediction.streamlit.app
**Backend Live API:** https://ai-vehicle-traffic-prediction-fastapi.onrender.com/predict
**Backend API Docs:** https://ai-vehicle-traffic-prediction-fastapi.onrender.com/docs
**Developed By:** Shreya Singh

---

### 📍 Project Overview
Jaunpur is a heritage city with narrow roads, heavy E-Rickshaw density, and historical zones like Shahi Bridge (1564 AD) and Atala Masjid (1408 AD). This project uses Machine Learning + YOLOv8 + TomTom + Weather + SQLite to predict hourly vehicle count.

### ✨ Key Features
**1. Core Prediction:**
- Vehicle count prediction per hour (AI + FastAPI)
- Congestion Level: Low / Medium / High / Critical
- Dynamic Signal Timer: 30s / 60s / 90s
- YOLO Live Count + TomTom Live Speed + Hospital ETA + Weather

**2. Jaunpur-Specific Intelligence:**
- 11 Major Junctions mapped with real GPS coordinates
- Route Connectivity, Landmark & Parking Info
- Risk & Safety Intelligence
- Live Google Maps Embed

**3. Unique Innovations (Viva Points):**
- Heritage Zone Alert: Alerts for Shahi Bridge & Atala Masjid
- Alternate Route Intelligence: AI suggests alternate route
- Carbon & Fuel Loss Calculator
- Smart City Performance Score: 100/100
- Multi-Language Voice Alert: English, Hindi, Bhojpuri using gTTS
- Emergency Corridor Mode: Green corridor for Ambulance/Police

### 🗺️ Junctions Covered (11 Total)
- 8 Four-Way: Polytechnic, Jesis, Chaharsu, Olandganj, Line Bazar, Visheshwarpur, Kotwali, Sipah
- 3 Three-Way: Wajidpur, Ambedkar, Zafarabad

### 🛠️ Tech Stack
- Frontend: Streamlit
- Backend: FastAPI (on Render)
- ML Model: YOLOv8 + RandomForest
- Libraries: TomTom API, OpenWeather, SQLite, Folium, gTTS

### 🛠️ Installation
```bash
git clone https://github.com/kshatriyashreya219/AI-Vehicle-Traffic-Prediction-FastAPI.git
pip install -r requirements.txt
streamlit run dashboard.py
