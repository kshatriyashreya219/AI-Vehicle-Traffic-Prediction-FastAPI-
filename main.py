"""
Jaunpur TrafficAI - Smart City Traffic Intelligence System
Developed by: Shreya Singh
GitHub: https://github.com/kshatriyashreya219
Project: AI Vehicle Traffic Prediction for Jaunpur Smart City
"""

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Jaunpur TrafficAI - Smart City API",
    description="AI-powered traffic prediction system for Jaunpur's most congested corridors | Developed by Shreya Singh",
    version="5.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrafficInput(BaseModel):
    junction: int
    hour: int
    is_holiday: str = "No"

class TrafficOutput(BaseModel):
    predicted_vehicles: int
    congestion_level: str
    junction_name: str
    zone_type: str
    developed_by: str = "Shreya Singh"

# --- REAL JAUNPUR HIGH CONGESTION ZONES (Professional Mapping) ---
JUNCTION_DATA = {
    1: {"name": "Olandganj Commercial Hub", "type": "Central Business District (CBD)", "load": 60},
    2: {"name": "Chaharsu Central Intersection", "type": "City Center Core - High Density Zone", "load": 55},
    3: {"name": "Sadbhavna Bridge - Gomti Corridor", "type": "River Bridge - Primary Inter-City Link", "load": 70},
    4: {"name": "JCiz Chauraha - Azamgarh Route", "type": "Inter-District Transit Junction", "load": 50},
    5: {"name": "Polytechnic Square", "type": "Institutional & Mandi Access Corridor", "load": 45},
    6: {"name": "Jogiyapur - Sutarhatti Junction", "type": "Old City Commercial Lanes", "load": 40},
    7: {"name": "Mungra Badshahpur Highway Stretch", "type": "National Highway Corridor (4-12 KM Jam Zone)", "load": 80},
    8: {"name": "Shahganj Road - Railway Corridor", "type": "Major Transit & Logistics Hub", "load": 65}
}

def traffic_prediction_model(junction: int, hour: int, is_holiday: str):
    zone = JUNCTION_DATA.get(junction, JUNCTION_DATA[1])

    # Base traffic calculation with zone weightage
    base_volume = 120 + (hour * 12) + zone["load"]

    if is_holiday.lower() == "no":
        base_volume += 25 # Working day congestion

    # Congestion classification
    if base_volume >= 260:
        level = "CRITICAL"
    elif base_volume >= 200:
        level = "HIGH"
    elif base_volume >= 130:
        level = "MODERATE"
    else:
        level = "LOW"

    return int(base_volume), level, zone["name"], zone["type"]

@app.get("/")
def root():
    return {
        "project": "Jaunpur TrafficAI",
        "developed_by": "Shreya Singh",
        "location": "Jaunpur, Uttar Pradesh, India",
        "total_monitoring_zones": 8,
        "status": "Active & Deployed"
    }

@app.post("/predict", response_model=TrafficOutput)
def predict(data: TrafficInput):
    volume, level, name, ztype = traffic_prediction_model(data.junction, data.hour, data.is_holiday)
    return TrafficOutput(
        predicted_vehicles=volume,
        congestion_level=level,
        junction_name=name,
        zone_type=ztype,
        developed_by="Shreya Singh"
    )
