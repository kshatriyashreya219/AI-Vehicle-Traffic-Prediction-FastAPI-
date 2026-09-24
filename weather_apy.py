import random

def get_weather_impact():
    weather = random.choice(["Sunny", "Rainy", "Foggy", "Cloudy"])
    if weather == "Rainy":
        impact = 20
    elif weather == "Foggy":
        impact = 10
    elif weather == "Cloudy":
        impact = 5
    else:
        impact = 0
    return {"weather": weather, "jam_increase_percent": impact}
