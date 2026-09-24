import pandas as pd, random, pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

JUNCTION_DATA = {
    1: {"name": "Olandganj", "base": 60}, 2: {"name": "Chaharsu", "base": 55},
    3: {"name": "Sadbhavna Bridge", "base": 70}, 4: {"name": "JCiz", "base": 50},
    5: {"name": "Polytechnic", "base": 45}, 6: {"name": "Jogiyapur", "base": 40},
    7: {"name": "Mungra Highway", "base": 80}, 8: {"name": "Shahganj", "base": 65},
}

def generate_dataset(n=800):
    data = []
    for _ in range(n):
        junction = random.randint(1, 8)
        hour = random.randint(0, 23)
        is_holiday = random.choice(["Yes", "No"])
        base_load = JUNCTION_DATA[junction]["base"]
        if 8 <= hour <= 11 or 17 <= hour <= 20:
            time_factor = random.randint(30, 50)
        elif 12 <= hour <= 16:
            time_factor = random.randint(15, 30)
        else:
            time_factor = random.randint(-40, -10)
        holiday_factor = random.randint(-25, -10) if is_holiday=="Yes" else random.randint(15, 35)
        vehicles = max(20, 100 + base_load + (hour*5) + time_factor + holiday_factor + random.randint(-10,10))
        data.append([junction, hour, 1 if is_holiday=="Yes" else 0, vehicles, is_holiday])
    return pd.DataFrame(data, columns=["junction","hour","is_holiday_num","vehicles","is_holiday"])

print("Generating 800 rows...")
df = generate_dataset(800)
df.to_csv("jaunpur_traffic_dataset.csv", index=False)

X = df[["junction","hour","is_holiday_num"]]
y = df["vehicles"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print(f"Accuracy: {r2_score(y_test, model.predict(X_test))*100:.2f}%")

with open("traffic_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved!")
