# 🚦 AI Vehicle Traffic Prediction - Smart City Jaunpur

An AI-powered Smart Traffic Management System designed specifically for **Jaunpur City** to predict traffic congestion, optimize signal timers, and assist Traffic Police & Municipal Council.

**Live Demo:** https://traffic-ai-prediction.streamlit.app  
**Backend API:** https://ai-vehicle-traffic-prediction-fastapi.onrender.com/predict  
**Developed By:** Shreya Singh

---

### 📍 Project Overview
Jaunpur is a heritage city with narrow roads, heavy E-Rickshaw density, and historical zones like Shahi Bridge (1564 AD) and Atala Masjid (1408 AD). This project uses Machine Learning to predict hourly vehicle count and provides actionable insights for quick traffic clearance.

### ✨ Key Features

**1. Core Prediction:**
- Vehicle count prediction per hour (AI + FastAPI)
- Congestion Level: Low / Medium / High / Critical
- Dynamic Signal Timer: 30s / 60s / 90s
- AQI & Environmental Impact

**2. Jaunpur-Specific Intelligence:**
- **11 Major Junctions** mapped with real GPS coordinates
- Route Connectivity, Landmark & Parking Info
- Risk & Safety Intelligence (High Risk / Very High Risk Zones)
- Live Google Maps Embed

**3. Unique Innovations (Viva Points):**
- **🏛️ Heritage Zone Alert:** Alerts for Shahi Bridge & Atala Masjid - Heavy vehicle restricted, Low horn zone
- **🔀 Alternate Route Intelligence:** AI suggests alternate route to bypass congestion (e.g., Sipah -> Line Bazar to avoid Olandganj)
- **🌿 Carbon & Fuel Loss Calculator:** Calculates fuel wastage, CO2 emission, and economic loss per hour
- **🏙️ Smart City Performance Score:** 100/100 scoring based on traffic, weather, festival
- **🗣️ Multi-Language Voice Alert:** English, Hindi, Bhojpuri using gTTS
- **🚨 Emergency Corridor Mode:** One-click Green corridor for Ambulance/Police

**4. Role-Based Dashboards:**
- **Public User:** Prediction, Maps, Parking, Alternate Routes
- **Traffic Police:** Live City Dashboard, Challan & Revenue Monitoring (Challans Generated, Revenue, E-Rickshaw Penalty)
- **Municipal Council Officer:** Encroachment clearance, Drainage inspection, Speed breaker installation, Contact & Report Forwarding to Executive Officer

### 🗺️ Junctions Covered (11 Total)
- 8 Four-Way: Polytechnic, Jesis (Amravati), Chaharsu, Olandganj, Line Bazar, Visheshwarpur, Kotwali, Sipah
- 3 Three-Way: Wajidpur, Ambedkar, Zafarabad

### 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI (on Render)
- **ML Model:** RandomForest / Regression Model for traffic prediction
- **Libraries:** Pandas, Requests, gTTS, Random, Datetime
- **Mapping:** Google Maps Embed API

### 📊 Logic Used
```python
Base = 110
+55 if junction in [Olandganj, Chaharsu, Jesis] (Commercial Hub)
+35 if junction in [Wajidpur, Zafarabad] (Highway Entry)
+60 if Peak Hour (8-11 AM / 5-8 PM)
+50 if Festival Mode
+30 if E-Rickshaw > 30
