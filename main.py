from fastapi import FastAPI
from pydantic import BaseModel
from model import traffic_ai_model
from database import init_db, save_log
from weather_api import get_weather_impact

app = FastAPI(title="Jaunpur TrafficAI - by Shreya Singh")
init_db()

class Request(BaseModel):
    junction: int
    hour: int
    is_holiday: str # Yes / No - Vacation logic

@app.get("/")
def home():
    return {"message": "Jaunpur TrafficAI Live - Weekly + Vacation Mode ON", "developer": "Shreya Singh"}

@app.post("/predict")
def predict(req: Request):
    vehicles, level, score, rec, m_type = traffic_ai_model.predict(req.junction, req.hour, req.is_holiday)
    weather = get_weather_impact()
    # Vacation adjustment
    if req.is_holiday == "Yes":
        vehicles = max(20, vehicles - 15)
    
    final_vehicles = vehicles + weather['jam_increase_percent']
    
    # Save to DB
    save_log(f"Junction-{req.junction}", int(final_vehicles), level)
    
    return {
        "junction": req.junction,
        "vehicles_predicted": int(final_vehicles),
        "congestion_level": level,
        "congestion_score": score,
        "recommendation": rec,
        "model_type": m_type,
        "is_holiday": req.is_holiday,
        "weather": weather,
        "vacation_note": "15% traffic kam - School/College band" if req.is_holiday=="Yes" else "Normal working day"
    }
