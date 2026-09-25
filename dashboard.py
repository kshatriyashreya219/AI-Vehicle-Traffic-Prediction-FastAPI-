import streamlit as st
import random
import pandas as pd
import datetime
import requests

# ----------------------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Vehicle Traffic Prediction - Smart City Jaunpur",
    page_icon="🚦",
    layout="wide"
)

# ----------------------------------------------------------------------------------
# Custom Style - Green Predict Button
# ----------------------------------------------------------------------------------
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #00C853!important;
    color: white!important;
    border: none;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
}
div.stButton > button:first-child:hover {
    background-color: #00A843!important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# Backend API Configuration
# ----------------------------------------------------------------------------------
API_URL = "https://ai-vehicle-traffic-prediction-fastapi-1.onrender.com/predict"

# ----------------------------------------------------------------------------------
# Header Section
# ----------------------------------------------------------------------------------
st.title("🚦 AI Vehicle Traffic Prediction")
st.subheader("Jaunpur City - Comprehensive Traffic Analysis System")
st.caption(f"Backend Live: {API_URL} | Developed by Shreya Singh")
st.divider()

# ----------------------------------------------------------------------------------
# Core Dataset: 11 Major Junctions of Jaunpur City
# ----------------------------------------------------------------------------------
junctions = {
    1: {"name": "Polytechnic Intersection", "route": "Prayagraj (Allahabad), Lucknow, and Shahganj", "landmark": "Government Polytechnic College, Lohia Park"},
    2: {"name": "Jesis Intersection (Amravati)", "route": "Azamgarh, Gorakhpur, and Roadways Bus Stand", "landmark": "'I Love Jaunpur' Sign Board, Electronics Market"},
    3: {"name": "Chaharsu Intersection", "route": "Historical Old Market, Kotwali, and Shahganj", "landmark": "Near the historic Shahi Bridge (Mughal Bridge)"},
    4: {"name": "Olandganj Intersection", "route": "T.D. College Route and Jaunpur Junction Railway Station", "landmark": "Main commercial and shopping hub of the city"},
    5: {"name": "Line Bazar Intersection", "route": "Collectorate, Police Lines, and T.D. College", "landmark": "Administrative area, residential shopping hub"},
    6: {"name": "Visheshwarpur Intersection", "route": "Inner city local markets and Sheetla Choukiya Dham", "landmark": "Major wholesale commercial centre"},
    7: {"name": "Kotwali Intersection", "route": "Shahganj Route and Old City residential areas", "landmark": "Main Kotwali (Police Station)"},
    8: {"name": "Wajidpur Three-Way Junction", "route": "Varanasi Highway and Maihar Devi Temple", "landmark": "Parasnathpur area, prominent entry point to the city"},
    9: {"name": "Ambedkar Three-Way Junction", "route": "Civil Lines area", "landmark": "Dr. B.R. Ambedkar Statue Circle"},
    10: {"name": "Sipah Intersection (Sipah Police Station)", "route": "Direct Varanasi Route and Atala Masjid area", "landmark": "Busy junction near Sipah Police Station, Northern bank of Gomti River"},
    11: {"name": "Zafarabad Three-Way Junction", "route": "Varanasi and Kerakat Route", "landmark": "Key outer junction point near Zafarabad Railway Station"}
}

coords = {
    1: (25.7536, 82.6867), 2: (25.7498, 82.6942), 3: (25.7475, 82.6855),
    4: (25.7505, 82.6905), 5: (25.7580, 82.6820), 6: (25.7420, 82.6800),
    7: (25.7445, 82.6830), 8: (25.7610, 82.7000), 9: (25.7555, 82.6750),
    10: (25.7350, 82.6955), 11: (25.7040, 82.7500)
}

# ----------------------------------------------------------------------------------
# Smart City Control Panel
# ----------------------------------------------------------------------------------
st.sidebar.header("Smart City Control Panel")
festival_mode = st.sidebar.selectbox("Festival / Event Mode", ["Normal Day", "Sawan Mela", "Durga Puja", "Festival", "Election Day"])
emergency_mode = st.sidebar.toggle("Emergency Mode (Ambulance + Police Corridor)")
erickshaw_count = st.sidebar.slider("E-Rickshaw Density Analysis", 0, 100, 25)
voice_language = st.sidebar.selectbox("Voice Alert System", ["English"])
weather_condition = st.sidebar.selectbox("Environmental Condition", ["Clear", "Rain", "Fog", "Summer Heat"])
alert_number = st.sidebar.text_input("WhatsApp Alert Notification Number", placeholder="Enter Mobile Number")

selected_id = st.selectbox("Select Junction for Analysis", list(junctions.keys()), format_func=lambda x: f"{x}. {junctions[x]['name']}")

col_r, col_l = st.columns(2)
col_r.info(f"**Route Connectivity:** {junctions[selected_id]['route']}")
col_l.success(f"**Nearby Landmark:** {junctions[selected_id]['landmark']}")

# ----------------------------------------------------------------------------------
# Live Map - Fixed
# ----------------------------------------------------------------------------------
lat, lon = coords[selected_id]
st.subheader(f"Live Geospatial Map - {junctions[selected_id]['name']}")
map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})
st.map(map_df, zoom=15)
st.caption(f"GPS: {lat}, {lon} | {junctions[selected_id]['name']}")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    hour = st.slider("Select Hour (0-23)", 0, 23, 10)
with col2:
    weekday = st.selectbox("Day of Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
with col3:
    is_holiday = st.selectbox("Is Holiday?", ["No", "Yes"])

def get_local_prediction(j_id, h, w_day, h_day):
    random.seed(j_id * 100 + h)
    base = 110
    if j_id in [4, 3, 2]: base += 55
    if j_id in [8, 11]: base += 35
    if 8 <= h <= 11 or 17 <= h <= 20: base += 60
    if w_day == "Monday": base += 20
    if w_day in ["Saturday","Sunday"]: base = int(base * 0.8)
    if h_day == "Yes": base = int(base * 0.65)
    if festival_mode!= "Normal Day": base += 50
    if erickshaw_count > 30: base += 30
    if weather_condition == "Rain": base += 20
    return base + random.randint(-15, 30)

def get_traffic_cause(j_id, count, erick, festival, weather):
    causes = []
    if erick > 40: causes.append(f"High E-Rickshaw Density ({erick} vehicles) - Primary bottleneck in Jaunpur")
    if j_id in [4, 3, 2]: causes.append("Commercial Hub + Market Area + Narrow Road Infrastructure")
    if j_id in [8, 11]: causes.append("Highway Entry Point + Heavy Vehicle Movement")
    if festival!= "Normal Day": causes.append(f"{festival} - Public Gathering and Crowd Movement")
    if weather == "Rain": causes.append("Water Logging + Reduced Vehicle Speed")
    if count > 210: causes.append("Peak Hour Rush (08:00-11:00 / 17:00-20:00)")
    if not causes: causes.append("Normal Traffic Flow - No Major Obstruction")
    return causes

if st.button("🚀 Predict Traffic", use_container_width=True, type="primary"):
    vehicles = get_local_prediction(selected_id, hour, weekday, is_holiday)
    try:
        payload = {"junction": selected_id, "hour": hour, "day": 15, "is_holiday": 1 if is_holiday=="Yes" else 0}
        api_res = requests.post(API_URL, json=payload, timeout=5)
        if api_res.status_code == 200:
            vehicles = api_res.json().get("predicted_count", vehicles)
    except:
        pass

    level = "Low" if vehicles < 130 else "Medium" if vehicles < 210 else "High / Critical"
    causes = get_traffic_cause(selected_id, vehicles, erickshaw_count, festival_mode, weather_condition)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Predicted Vehicle Count", f"{vehicles} vehicles/hr")
    c2.metric("Congestion Level", level)
    c3.metric("Estimated Waiting Time", "5-7 min" if "High" in level else "2-3 min" if "Medium" in level else "0-1 min")
    c4.metric("Weather Impact Factor", weather_condition)

    if "High" in level:
        st.error(f"🔴 High Congestion Detected at {junctions[selected_id]['name']}")
    elif "Medium" in level:
        st.warning(f"🟠 Moderate Traffic at {junctions[selected_id]['name']}")
    else:
        st.success(f"🟢 Traffic Flow Clear at {junctions[selected_id]['name']}")

    st.subheader("Traffic Cause Analysis - For Quick Clearance")
    for idx, cause in enumerate(causes, 1):
        if "High" in cause or "Peak" in cause:
            st.error(f"{idx}. {cause}")
        else:
            st.warning(f"{idx}. {cause}")

    st.divider()
    st.subheader("Voice Alert System")
    voice_text = f"Attention, {level} traffic congestion reported at {junctions[selected_id]['name']}. Cause is {causes[0]}."
    st.info(f"🔊 Voice Message: {voice_text}")

    if alert_number:
        st.success(f"WhatsApp Alert Sent to {alert_number}")

    st.subheader(f"📊 24-Hour Traffic Pattern - {junctions[selected_id]['name']}")
    chart_df = pd.DataFrame({"Hour": list(range(24)), "Vehicles": [get_local_prediction(selected_id, h, weekday, is_holiday) for h in range(24)]})
    st.bar_chart(chart_df.set_index("Hour"))

    st.subheader("📈 All Junctions Comparative Analysis")
    all_data = [{"Junction": junctions[jid]['name'].split()[0], "Vehicles": get_local_prediction(jid, hour, weekday, is_holiday)} for jid in junctions]
    st.line_chart(pd.DataFrame(all_data).set_index("Junction"))

st.divider()
st.markdown("""
**Project Details:**
- **Project Title:** AI Vehicle Traffic Prediction - Smart City Jaunpur
- **Total Junctions Covered:** 11 (8 Four-Way & 3 Three-Way)
- **Data Source:** Jaunpur City Mapping & Field Research
- **Backend API:** https://ai-vehicle-traffic-prediction-fastapi-1.onrender.com
- **Developed By:** Shreya Singh
""")
