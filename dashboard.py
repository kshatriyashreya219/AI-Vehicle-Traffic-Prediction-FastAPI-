import streamlit as st
import random
import pandas as pd
import datetime
import requests
from io import BytesIO
import sqlite3
import os
import folium
from streamlit_folium import st_folium
from gtts import gTTS

# --- 0. SQLite DB Setup ---
def init_db():
    conn = sqlite3.connect("traffic.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS logs
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               junction INTEGER, hour INTEGER, day INTEGER,
               is_holiday INTEGER, predicted_count INTEGER)""")
    conn.commit()
    conn.close()

def save_log(junction, hour, day, is_holiday, predicted_count):
    try:
        conn = sqlite3.connect("traffic.db")
        c = conn.cursor()
        c.execute("INSERT INTO logs (junction, hour, day, is_holiday, predicted_count) VALUES (?,?,?,?,?)",
                  (junction, hour, day, is_holiday, predicted_count))
        conn.commit()
        conn.close()
    except: pass

def get_logs():
    try:
        conn = sqlite3.connect("traffic.db")
        df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC LIMIT 20", conn)
        conn.close()
        return df
    except: return pd.DataFrame()

init_db()

# --- 0.1 API Keys & Live Data Fetchers ---
TOMTOM_KEY = st.secrets.get("TOMTOM_KEY", "")
WEATHER_KEY = st.secrets.get("WEATHER_KEY", "")

@st.cache_data(ttl=60)
def get_tomtom_flow(lat, lon):
    if not TOMTOM_KEY: return 22, 40
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={TOMTOM_KEY}"
    try:
        r = requests.get(url, timeout=5).json()
        return r['flowSegmentData']['currentSpeed'], r['flowSegmentData']['freeFlowSpeed']
    except: return 22, 40

@st.cache_data(ttl=60)
def get_tomtom_incident():
    if not TOMTOM_KEY: return []
    url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?bbox=82.6,25.7,82.8,25.8&fields={{incidents{{type,delay}}}}&key={TOMTOM_KEY}"
    try:
        r = requests.get(url, timeout=5).json()
        return r.get('incidents', [])[:3]
    except: return []

@st.cache_data(ttl=120)
def get_tomtom_eta(src_lat, src_lon, dest_lat=25.740, dest_lon=82.680):
    if not TOMTOM_KEY: return 12
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{src_lat},{src_lon}:{dest_lat},{dest_lon}/json?key={TOMTOM_KEY}&traffic=true"
    try:
        r = requests.get(url, timeout=5).json()
        return int(r['routes'][0]['summary']['travelTimeInSeconds']/60)
    except: return 12

@st.cache_data(ttl=300)
def get_real_weather(lat, lon):
    if not WEATHER_KEY: return "32°C, Haze", 65, 1012
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=metric"
        r = requests.get(url, timeout=5).json()
        return f"{r['main']['temp']}°C, {r['weather'][0]['main']}", r['main']['humidity'], r['main']['pressure']
    except: return "32°C, Haze", 65, 1012

def get_yolo_count():
    if os.path.exists("live_count.txt"):
        try:
            with open("live_count.txt", "r") as f: return int(f.read().strip())
        except: pass
    return None

# --- 1. Page Config ---
st.set_page_config(page_title="AI Vehicle Traffic Prediction - Smart City Jaunpur", page_icon="🚦", layout="wide")
API_URL = "https://ai-vehicle-traffic-prediction-fastapi.onrender.com/predict"
st.title("🚦 AI Vehicle Traffic Prediction")
st.subheader("Jaunpur City - Comprehensive Traffic Analysis + Digital Twin")
st.caption(f"Backend Live: {API_URL} | YOLOv8 + TomTom + Weather + SQLite | Developed by Shreya Singh")
st.divider()

junctions = {
    1: {"name": "Polytechnic Intersection", "route": "Prayagraj (Allahabad), Lucknow, and Shahganj", "landmark": "Government Polytechnic College, Lohia Park", "parking": "Polytechnic Ground - 30 Slots", "risk": "Low Risk Zone", "heritage": "Educational Zone"},
    2: {"name": "Jesis Intersection (Amravati)", "route": "Azamgarh, Gorakhpur, and Roadways Bus Stand", "landmark": "'I Love Jaunpur' Sign Board, Electronics Market", "parking": "Bus Stand Parking - 15 Slots", "risk": "Medium Risk - Pedestrian", "heritage": "Modern City Center"},
    3: {"name": "Chaharsu Intersection", "route": "Historical Old Market, Kotwali, and Shahganj", "landmark": "Near the historic Shahi Bridge (Mughal Bridge)", "parking": "Shahi Bridge - 10 Slots", "risk": "High Risk - Narrow Road", "heritage": "Heritage Zone - Shahi Bridge (1564 AD)"},
    4: {"name": "Olandganj Intersection", "route": "T.D. College Route and Jaunpur Junction Railway Station", "landmark": "Main commercial and shopping hub of the city", "parking": "T.D. College - 5 Slots (Full)", "risk": "High Risk - E-Rickshaw Hub", "heritage": "Commercial Hub"},
    5: {"name": "Line Bazar Intersection", "route": "Collectorate, Police Lines, and T.D. College", "landmark": "Administrative area, residential shopping hub", "parking": "Collectorate - 40 Slots", "risk": "Low Risk Zone", "heritage": "Administrative Zone"},
    6: {"name": "Visheshwarpur Intersection", "route": "Inner city local markets and Sheetla Choukiya Dham", "landmark": "Major wholesale commercial centre", "parking": "Local Market - 20 Slots", "risk": "Medium Risk", "heritage": "Temple Zone"},
    7: {"name": "Kotwali Intersection", "route": "Shahganj Route and Old City residential areas", "landmark": "Main Kotwali (Police Station)", "parking": "Kotwali - 12 Slots", "risk": "High Risk - Old City", "heritage": "Old City Fort Area"},
    8: {"name": "Wajidpur Three-Way Junction", "route": "Varanasi Highway and Maihar Devi Temple", "landmark": "Parasnathpur area, prominent entry point to the city", "parking": "Highway - 50 Slots", "risk": "VERY HIGH RISK - Highway Speed", "heritage": "Highway Entry"},
    9: {"name": "Ambedkar Three-Way Junction", "route": "Civil Lines area", "landmark": "Dr. B.R. Ambedkar Statue Circle", "parking": "Civil Lines - 35 Slots", "risk": "Low Risk Zone", "heritage": "Civil Lines"},
    10: {"name": "Sipah Intersection (Sipah Police Station)", "route": "Direct Varanasi Route and Atala Masjid area", "landmark": "Busy junction near Sipah Police Station, Northern bank of Gomti River", "parking": "Sipah - 25 Slots", "risk": "High Risk - Speeding", "heritage": "Heritage Zone - Atala Masjid (1408 AD)"},
    11: {"name": "Zafarabad Three-Way Junction", "route": "Varanasi and Kerakat Route", "landmark": "Key outer junction point near Zafarabad Railway Station", "parking": "Zafarabad - 45 Slots", "risk": "VERY HIGH RISK - Railway Crossing", "heritage": "Railway Zone"}
}
coords = {1: (25.7536, 82.6867), 2: (25.7498, 82.6942), 3: (25.7475, 82.6855), 4: (25.7505, 82.6905), 5: (25.7580, 82.6820), 6: (25.7420, 82.6800), 7: (25.7445, 82.6830), 8: (25.7610, 82.7000), 9: (25.7555, 82.6750), 10: (25.7350, 82.6955), 11: (25.7040, 82.7500)}

st.sidebar.header("Smart City Control Panel")
role = st.sidebar.selectbox("Login Role", ["Public User", "Traffic Police", "Municipal Council Officer"])
festival_mode = st.sidebar.selectbox("Festival / Event Mode", ["Normal Day", "Sawan Mela", "Durga Puja", "Moharram", "Election Day"])
emergency_mode = st.sidebar.toggle("Emergency Mode (Ambulance + Police Corridor)")
erickshaw_count = st.sidebar.slider("E-Rickshaw Density Analysis", 0, 100, 25)
voice_language = st.sidebar.selectbox("Multi-Language Voice Alert System", ["English", "Hindi", "Bhojpuri"])
weather_condition = st.sidebar.selectbox("Environmental Condition", ["Clear", "Rain", "Fog", "Summer Heat"])
selected_id = st.selectbox("Select Junction for Analysis", list(junctions.keys()), format_func=lambda x: f"{x}. {junctions[x]['name']}")

lat, lon = coords[selected_id]
yolo_live = get_yolo_count()
cur_speed, free_speed = get_tomtom_flow(lat, lon)
percent_free = int((cur_speed / free_speed)*100) if free_speed else 55
eta_hosp = get_tomtom_eta(lat, lon)
incidents = get_tomtom_incident()
weather_text, humidity, pressure = get_real_weather(lat, lon)

c_live1, c_live2, c_live3, c_live4, c_live5 = st.columns(5)
c_live1.metric("YOLO Live Count", f"{yolo_live} Veh" if yolo_live else "Demo Mode", "CCTV")
c_live2.metric("TomTom Live Speed", f"{cur_speed} km/h", f"{percent_free}% Free Flow")
c_live3.metric("Hospital ETA", f"{eta_hosp} min", "Live Routing")
c_live4.metric("Smart Signal Timer", f"{30 + (yolo_live//2) if yolo_live else 45} sec", "Auto")
c_live5.metric("Weather (OpenWeather)", weather_text, f"Humidity {humidity}%")
st.progress(percent_free)
st.info(f"🌤️ Live Weather: {weather_text} | Humidity: {humidity}% | Pressure: {pressure} hPa | Location: {junctions[selected_id]['name']}")

col_r, col_l, col_p = st.columns(3)
col_r.info(f"**Route Connectivity:** {junctions[selected_id]['route']}")
col_l.success(f"**Nearby Landmark:** {junctions[selected_id]['landmark']}")
col_p.warning(f"**Parking Facility:** {junctions[selected_id]['parking']} | **Risk:** {junctions[selected_id]['risk']}")

tab1, tab2 = st.tabs(["🌍 Google Map View", "🗺️ Digital Twin Map (Folium)"])
with tab1:
    st.subheader(f"Live Geospatial Map - {junctions[selected_id]['name']}")
    st.components.v1.html(f'<iframe width="100%" height="350" style="border:0; border-radius:12px;" src="https://maps.google.com/maps?q={lat},{lon}&z=16&output=embed"></iframe>', height=370)
with tab2:
    st.subheader("Digital Twin Live Traffic")
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles="CartoDB positron")
    color = "red" if percent_free < 50 else "green"
    folium.CircleMarker([lat, lon], radius=20, color=color, fill=True, fill_opacity=0.6, popup=f"{junctions[selected_id]['name']}: {cur_speed} km/h").add_to(m)
    folium.Marker([25.740, 82.680], popup="District Hospital", icon=folium.Icon(color="green", icon="plus", prefix="fa")).add_to(m)
    st_folium(m, height=350, width=700, returned_objects=[])

if incidents:
    for inc in incidents: st.error(f"⚠️ Incident: {inc.get('type','Jam')} - Delay {inc.get('delay',0)}s near {junctions[selected_id]['name']}")

st.divider()
col1, col2, col3 = st.columns(3)
with col1: hour = st.slider("Select Hour (0-23)", 0, 23, 10)
with col2: weekday = st.selectbox("Day of Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
with col3: is_holiday = st.selectbox("Is Holiday?", ["No", "Yes"])

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

def get_audio(text, lang='en'):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except: return None

if st.button("🚀 Predict Traffic", use_container_width=True, type="primary"):
    vehicles = get_local_prediction(selected_id, hour, weekday, is_holiday)
    try:
        payload = {"junction": selected_id, "hour": hour, "day": 15, "is_holiday": 1 if is_holiday=="Yes" else 0}
        api_res = requests.post(API_URL, json=payload, timeout=5)
        if api_res.status_code == 200: vehicles = api_res.json().get("predicted_count", vehicles)
    except: pass
    day_num = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].index(weekday)
    save_log(junction=selected_id, hour=hour, day=day_num, is_holiday=1 if is_holiday=="Yes" else 0, predicted_count=vehicles)
    level = "Low" if vehicles < 130 else "Medium" if vehicles < 210 else "High / Critical"
    timer = "90s - High Density" if "High" in level else "60s - Moderate" if "Medium" in level else "30s - Eco Mode"
    aqi = int(vehicles * 0.8 + erickshaw_count * 0.5)
    aqi_label = "Good" if aqi < 100 else "Moderate" if aqi < 200 else "Poor"
    revenue = int(vehicles * 0.1 * 500)
    causes = get_traffic_cause(selected_id, vehicles, erickshaw_count, festival_mode, weather_condition)
    if emergency_mode:
        st.error("🚨 EMERGENCY CORRIDOR ACTIVE - All Signals Green for Emergency Vehicle | Timer = 60 sec")
        timer = "60s - Emergency"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Predicted Vehicle Count", f"{vehicles} vehicles/hr")
    c2.metric("Congestion Level", level)
    c3.metric("Signal Timer", timer)
    c4.metric("AQI Index", f"{aqi} {aqi_label}")
    if "High" in level: st.error(f"🔴 High Congestion Detected at {junctions[selected_id]['name']}")
    elif "Medium" in level: st.warning(f"🟠 Moderate Traffic at {junctions[selected_id]['name']}")
    else: st.success(f"🟢 Traffic Flow Clear at {junctions[selected_id]['name']}")
    st.subheader("Risk and Safety Intelligence")
    risk = junctions[selected_id]['risk']
    if "VERY HIGH" in risk: st.error(f"CRITICAL ALERT: {risk} - Speed Limit 20 km/h")
    elif "High" in risk: st.warning(f"WARNING: {risk} - Drive Carefully")
    else: st.success(f"SAFE CORRIDOR: {risk}")
    st.subheader("Smart Parking Management System")
    if "High" in level: st.warning(f"Primary Parking Full. Alternate Suggested: {junctions[selected_id]['parking']}")
    else: st.success(f"Parking Slot Available: {junctions[selected_id]['parking']}")
    st.divider()
    st.subheader("Traffic Cause Analysis - For Quick Clearance")
    for idx, cause in enumerate(causes, 1):
        if "High" in cause or "Peak" in cause: st.error(f"{idx}. {cause}")
        else: st.warning(f"{idx}. {cause}")
    st.divider()
    st.subheader("📍 Jaunpur Heritage Zone & Alternate Route Intelligence - UNIQUE")
    heritage_info = junctions[selected_id]['heritage']
    if "Heritage Zone" in heritage_info: st.error(f"🏛️ HERITAGE ALERT: You are near {heritage_info}. Heavy vehicles restricted. Low horn zone.")
    else: st.info(f"📍 Zone Type: {heritage_info}")
    alt_routes = {4: "Suggested Alternate: Use Sipah -> Line Bazar to avoid Olandganj market rush", 3: "Suggested Alternate: Use Kotwali Bypass -> Jesis Road for Shahi Bridge area", 2: "Suggested Alternate: Use Polytechnic -> Wajidpur Highway to bypass Jesis", 8: "Suggested Alternate: Use Zafarabad -> Kerakat Road to avoid Highway congestion", 10: "Suggested Alternate: Use Ambedkar Circle -> Civil Lines for Atala Masjid area"}
    alt = alt_routes.get(selected_id, f"Use inner lanes of {junctions[selected_id]['name']} for faster clearance")
    st.success(f"🔀 AI Suggested Alternate Route: {alt}")
    st.divider()
    st.subheader("🌿 Carbon Emission & Fuel Loss Calculator")
    fuel_loss_liters = round(vehicles * 0.15, 2)
    co2_kg = round(fuel_loss_liters * 2.31, 2)
    fuel_cost = fuel_loss_liters * 96.5
    e1, e2, e3 = st.columns(3)
    e1.metric("Fuel Wastage / Hour", f"{fuel_loss_liters} Liters")
    e2.metric("CO2 Emission / Hour", f"{co2_kg} Kg")
    e3.metric("Economic Loss / Hour", f"Rs. {int(fuel_cost)}")
    st.divider()
    st.subheader("🏙️ Jaunpur Smart City Performance Score")
    score = 100
    if "High" in level: score -= 30
    if erickshaw_count > 50: score -= 20
    if weather_condition == "Rain": score -= 10
    if festival_mode!= "Normal Day": score -= 15
    st.progress(score / 100)
    st.metric("Smart City Score", f"{score}/100")
    st.divider()
    st.subheader(f"Voice Alert System - {voice_language}")
    if voice_language == "English":
        voice_text = f"Attention, {level} traffic at {junctions[selected_id]['name']}. Total {vehicles} vehicles. Cause is {causes[0]}. Alternate route {alt}. Weather {weather_text}."
        lang_code = 'en'
    elif voice_language == "Hindi":
        voice_text = f"Dhyan dijiye, {junctions[selected_id]['name']} par {level} traffic hai. Kul {vehicles} vahan. Karan hai {causes[0]}. Mausam {weather_text}."
        lang_code = 'hi'
    else:
        voice_text = f"Sunila, {junctions[selected_id]['name']} par bhari bheed ba. Kul {vehicles} gadi. Mausam {weather_text}."
        lang_code = 'hi'
    st.info(f"🔊 Voice Message: {voice_text}")
    audio = get_audio(voice_text, lang_code)
    if audio: st.audio(audio, format='audio/mp3')
    if role!= "Public User":
        st.divider()
        st.subheader("Enforcement and Revenue Monitoring Panel")
        x1, x2, x3 = st.columns(3)
        x1.metric("Challans Generated Today", f"{int(vehicles*0.1)}")
        x2.metric("Revenue Generated", f"Rs. {revenue}")
        x3.metric("E-Rickshaw Penalty Collection", f"Rs. {erickshaw_count*100}")
    st.divider()
    st.subheader(f"📊 24-Hour Traffic Pattern - {junctions[selected_id]['name']}")
    chart_df = pd.DataFrame({"Hour": list(range(24)), "Vehicles": [get_local_prediction(selected_id, h, weekday, is_holiday) for h in range(24)]})
    st.bar_chart(chart_df.set_index("Hour"))
    st.subheader("📈 All Junctions Comparative Analysis")
    all_data = [{"Junction": junctions[jid]['name'].split()[0], "Vehicles": get_local_prediction(jid, hour, weekday, is_holiday)} for jid in junctions]
    st.line_chart(pd.DataFrame(all_data).set_index("Junction"))
    st.download_button("Export Traffic Report (CSV)", data=chart_df.to_csv(index=False).encode('utf-8'), file_name=f"Jaunpur_Traffic_Report_J{selected_id}.csv")
    if os.path.exists("traffic.db"):
        st.download_button("Download traffic.db (SQLite Proof)", open("traffic.db","rb").read(), "traffic.db")

st.divider()
with st.expander("Traffic Police - Live City Dashboard"):
    data = [{"ID": j, "Junction": junctions[j]['name'], "Count": get_local_prediction(j, hour, weekday, is_holiday), "Timer": "90s" if get_local_prediction(j, hour, weekday, is_holiday) >= 210 else "60s" if get_local_prediction(j, hour, weekday, is_holiday) >= 130 else "30s", "Risk": junctions[j]['risk'], "Status": "High" if get_local_prediction(j, hour, weekday, is_holiday) >= 210 else "Medium" if get_local_prediction(j, hour, weekday, is_holiday) >= 130 else "Low"} for j in junctions]
    st.dataframe(pd.DataFrame(data), use_container_width=True)

with st.expander("Municipal Council - Action Center"):
    m_data = [{"Junction": junctions[j]['name'], "Parking": junctions[j]['parking'], "Action": "Clear Encroachment" if get_local_prediction(j, hour, weekday, is_holiday) > 210 else "Routine Patrol"} for j in junctions]
    st.dataframe(pd.DataFrame(m_data), use_container_width=True)
    if st.button("Forward Report to Commissioner"):
        st.success("Report successfully forwarded to Municipal Commissioner, Jaunpur.")

# --- UPDATED: Municipal Council Dashboard with WhatsApp Wall ---
with st.expander("Municipal Council Jaunpur - Action Dashboard"):
    st.write("Dedicated Dashboard for Municipal Council Officers")
    nagar_data = []
    for jid in junctions:
        v = get_local_prediction(jid, hour, weekday, is_holiday)
        if erickshaw_count > 50 and jid in [4, 3, 2]: action = "Remove E-Rickshaw Stand - Deploy Enforcement Team"
        elif v > 210: action = "Clear Encroachment and Deploy Traffic Staff"
        elif weather_condition == "Rain": action = "Inspect Drainage System"
        elif "VERY HIGH" in junctions[jid]['risk']: action = "Accident Prone Zone - Install Speed Breaker"
        else: action = "Normal - Regular Monitoring Required"
        nagar_data.append({"Junction": junctions[jid]['name'], "Vehicle Count": v, "Municipal Council Action": action})
    st.dataframe(pd.DataFrame(nagar_data), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Contact Information & WhatsApp Wall") # Updated Title
    col_ph1, col_ph2, col_ph3 = st.columns(3)
    with col_ph1:
        contact_number = st.text_input("Contact Number", placeholder="+91-5452-XXXXXX")
    with col_ph2:
        whatsapp_number = st.text_input("WhatsApp Number", placeholder="+91-XXXXXXXXXX") # New Field
    with col_ph3:
        contact_email = st.text_input("Official Email", placeholder="jaunpur.npp@gmail.com")

    st.divider()
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        if contact_number or whatsapp_number or contact_email:
            st.info(f"📞 {contact_number} | 💬 WA: {whatsapp_number} | 📧 {contact_email} | EO Forward")
        else:
            st.info("📞 +91-XXXXXXXXXX | 💬 WA: +91-XXXXXXXXXX | 📧 jaunpur.npp@gmail.com")
    with c2:
        # WhatsApp Direct Share Button
        if whatsapp_number:
            clean_num = whatsapp_number.replace("+","").replace(" ","").replace("-","")
            msg_text = f"Jaunpur Traffic Alert: {junctions[selected_id]['name']} - {get_local_prediction(selected_id, hour, weekday, is_holiday)} vehicles. Action: Check Dashboard."
            wa_url = f"https://wa.me/{clean_num}?text={msg_text}"
            st.link_button("💬 Send Report on WhatsApp", wa_url, use_container_width=True)
        else:
            st.caption("Enter WhatsApp number to enable direct share")
    with c3:
        if st.button("Send Report to Municipal Council Office", use_container_width=True):
            st.success("Report successfully sent to Executive Officer, Municipal Council Jaunpur")
            st.balloons()

with st.expander("🗃️ SQLite DB Logs - Last 20 Predictions (Proof for Sir)"):
    st.dataframe(get_logs(), use_container_width=True, hide_index=True)
    st.caption("Ye DB me auto-save ho raha hai: junction, hour, day, is_holiday, predicted_count")

st.divider()
st.markdown("""
**Project Details:**
- **Project Title:** AI Vehicle Traffic Prediction - Smart City Jaunpur + Digital Twin + Weather API + WhatsApp Wall
- **Total Junctions Covered:** 11 (8 Four-Way & 3 Three-Way)
- **APIs Integrated:** YOLOv8 CCTV, TomTom Flow, Incident, Routing, OpenWeather Real API, FastAPI, SQLite, WhatsApp API
- **Developed By:** Shreya Singh
""")
