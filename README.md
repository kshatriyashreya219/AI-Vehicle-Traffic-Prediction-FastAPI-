# 🚦 AI Vehicle Traffic Prediction - Smart City Jaunpur

An AI-powered Smart Traffic Management System designed specifically for **Jaunpur City** to predict traffic congestion, optimize signal timers, and assist Traffic Police & Municipal Council.

**🌐 Live Demo (Frontend):** https://jaunpur-traffic-ai-prediction.streamlit.app/
**⚙️ Backend API:** https://ai-vehicle-traffic-prediction-fastapi-1.onrender.com
**📚 API Docs (Swagger):** https://ai-vehicle-traffic-prediction-fastapi-1.onrender.com/docs
**👩‍💻 Developed By:** Shreya Singh
**📍 City Focus:** Jaunpur, Uttar Pradesh, India

---

### 📍 Project Overview
Jaunpur is a heritage city with narrow roads, heavy E-Rickshaw density, and historical zones like Shahi Bridge (1564 AD) and Atala Masjid (1408 AD). This project uses Machine Learning + YOLOv8 + TomTom + Weather + SQLite to predict hourly vehicle count and manage traffic smartly.

### ✨ Key Features

**1. Core Prediction System:**
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
- **8 Four-Way:** Polytechnic, Jesis, Chaharsu, Olandganj, Line Bazar, Visheshwarpur, Kotwali, Sipah
- **3 Three-Way:** Wajidpur, Ambedkar, Zafarabad

### 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI (Deployed on Render)
- **ML Model:** YOLOv8 + RandomForest Regressor
- **Libraries:** TomTom API, OpenWeather, SQLite, Folium, gTTS

### 🔗 API Endpoints
- `GET /` - Health Check
- `POST /predict` - Predict Traffic
- `GET /docs` - Swagger UI

### 🛠️ Installation (Local)
```bash
git clone https://github.com/kshatriyashreya219/AI-Vehicle-Traffic-Prediction-FastAPI.git
cd AI-Vehicle-Traffic-Prediction-FastAPI
pip install -r requirements.txt
streamlit run dashboard.py
uvicorn main:app --reload
