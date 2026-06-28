# AI Vehicle Traffic Prediction API 🚦

A FastAPI-based Machine Learning API that predicts traffic congestion levels based on junction, time, and day inputs.

## 🚀 Features
- Predicts traffic volume using ML model
- Returns congestion level: High / Medium / Low
- Built with FastAPI for high performance
- Easy to test with automatic Swagger UI docs

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **ML:** Pandas, Scikit-learn
- **Server:** Uvicorn

## 📸 Demo

### 1. FastAPI Response
![FastAPI Response](./api-response.png)

### 2. Streamlit Web App UI  
![Streamlit UI](./ui-result.png)

## 📍 How to Run Locally

1. **Clone the repo**
   ```bash
 git clone https://github.com/kshatriyashreya219/AI-Vehicle-Traffic-Prediction-FastAPI
 cd AI-Vehicle-Traffic-Prediction-FastAPI
 pip install -r requirements.txt
 uvicorn main:app --reload
 ```

**Test API**
 Open: `http://127.0.0.1:8000/docs`
---
**Made by Shreya** | MCA Student
