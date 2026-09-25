import streamlit as st
import random
import pandas as pd
import requests
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Jaunpur Smart City - AI Traffic System",
    page_icon="🚦",
    layout="wide"
)

# Premium UI Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: #000000; }
section[data-testid="stSidebar"] { background: #0A0A0A; border-right: 1px solid #1E1E1E; }

h1 { font-weight: 700; letter-spacing: -0.5px; }
h2, h3 { font-weight: 600; }

div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #EAEAEA;
    transition: all 0.3s ease;
}
div[data-testid="stMetric"]:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(255,255,255,0.15); }
div[data-testid="stMetric"] label { color: #8B8B8B!important; font-size: 11px; letter-spacing: 1px; }
div[data-testid="stMetric"] div { color: #000000!important; font-weight: 800; }

div.stButton > button:first-child {
    background: linear-gradient(90deg, #00C853, #00E676);
    color: white;
    height: 58px;
    font-weight: 700;
    border-radius: 14px;
    font-size: 16px;
    border: none;
    box-shadow: 0 6px 20px rgba(0,200,83,0.3);
}
div.stButton > button:first-child:hover { background: linear-gradient(90deg, #00B34A, #00C853); transform: scale(1.01); }

.stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

API_URL = "https://ai-vehicle-traffic-prediction-fastapi-1.onrender.com/predict"

JUNCTIONS = {
    1: {"name": "Polytechnic Intersection", "route": "Prayagraj | Lucknow | Shahganj", "parking": "Polytechnic Ground - 30 Slots", "risk": "Low Risk Zone"},
    2: {"name": "Jesis Intersection", "route": "Azamgarh | Bus Stand | Gorakhpur", "parking": "Bus Stand Parking - 15 Slots", "risk": "Medium Risk - Pedestrian"},
    3: {"name": "Chaharsu Intersection", "route": "Old Market | Kotwali", "parking": "Shahi Bridge - 10 Slots", "risk": "High Risk - Narrow Road"},
    4: {"name": "Olandganj Intersection", "route": "T.D. College | Railway Station", "parking": "T.D. College - 5 Slots (Full)", "risk": "High Risk - E-Rickshaw Hub"},
    5: {"name": "Line Bazar Intersection", "route": "Collectorate | Police Lines", "parking": "Collectorate - 40 Slots", "risk": "Low Risk Zone"},
    6: {"name": "Visheshwarpur Intersection", "route": "Sheetla Dham | Wholesale", "parking": "Local Market - 20 Slots", "risk": "Medium Risk"},
    7: {"name": "Kotwali Intersection", "route": "Shahganj | Old City", "parking": "Kotwali - 12 Slots", "risk": "High Risk - Old City"},
    8: {"name": "Wajidpur Three-Way", "route": "Varanasi Highway | Entry Point", "parking": "Highway - 50 Slots", "risk": "VERY HIGH RISK - Highway Speed"},
    9: {"name": "Ambedkar Three-Way", "route": "Civil Lines", "parking": "Civil Lines - 35 Slots", "risk": "Low Risk Zone"},
    10: {"name": "Sipah Intersection", "route": "Varanasi | Atala Masjid", "parking": "Sipah - 25 Slots", "risk": "High Risk - Speeding"},
    11: {"name": "Zafarabad Three-Way", "route": "Varanasi | Kerakat", "parking": "Zafarabad - 45 Slots", "risk": "VERY HIGH RISK - Railway Crossing"}
}

COORDINATES = {
    1:(25.7536,82.6867),2:(25.7498,82.6942),3:(25.7475,82.6855),4:(25.7505,82.6905),
    5:(25.7580,82.6820),6:(25.7420,82.6800),7:(25.7445,82.6830),8:(25.7610,82.7000),
    9:(25.7555,82.6750),10:(25.7350,82.6955),11:(25.7040,82.7500)
}

# Sidebar
with st.sidebar:
    st.markdown("## 🚦 JAUNPUR SMART CITY")
    st.caption("AI Traffic Management v3.0")
    st.divider()
    role = st.selectbox("Login Role", ["Public User", "Traffic Police", "Municipal Council Officer"])
    festival = st.selectbox("Operational Mode", ["Normal Day", "Sawan Mela", "Durga Puja", "Festival", "Election Day"])
    emergency = st.toggle("🚨 Emergency Corridor")
    e_density = st.slider("E-Rickshaw Density", 0, 100, 25)
    weather = st.selectbox("Weather", ["Clear", "Rain", "Fog", "Summer Heat"])
    st.divider()
    st.markdown("**Developed by** \nShreya Singh \n*Smart City Jaunpur*")

# Header Section
st.markdown("<h1 style='margin-bottom:0px;'>AI Vehicle Traffic Prediction System</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#9E9E9E!important; font-size:14px;'>Live Monitoring | Role: {role} | Powered by AI & IoT</p>", unsafe_allow_html=True)
st.divider()

selected = st.selectbox("📍 Select Junction for Analysis", list(JUNCTIONS.keys()), format_func=lambda x: f"{x}. {JUNCTIONS[x]['name']}")

c1, c2 = st.columns(2)
c1.info(f"**Route:** {JUNCTIONS[selected]['route']}")
c2.success(f"**Parking:** {JUNCTIONS[selected]['parking']}")

lat, lon = COORDINATES[selected]
st.subheader(f"Geospatial Intelligence - {JUNCTIONS[selected]['name']}")
st.map(pd.DataFrame({"lat":[lat],"lon":[lon]}), zoom=15)
st.markdown(f"[View on Google Maps ↗](https://www.google.com/maps/search/?api=1&query={lat},{lon})")
st.divider()

a1, a2, a3 = st.columns(3)
with a1: hour = st.slider("Hour", 0, 23, 10)
with a2: day = st.selectbox("Day", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
with a3: holiday = st.selectbox("Holiday", ["No","Yes"])

def predict(jid, h):
    random.seed(jid * 100 + h)
    base = 110
    if jid in [4,3,2]: base += 55
    if jid in [8,11]: base += 35
    if 8 <= h <= 11 or 17 <= h <= 20: base += 60
    if festival!= "Normal Day": base += 50
    if e_density > 30: base += 30
    if weather == "Rain": base += 20
    return base + random.randint(-15, 30)

def get_audio(text, lang):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except:
        return None

if st.button("🚀 PREDICT & ANALYZE TRAFFIC", use_container_width=True):
    count = predict(selected, hour)
    try:
        payload = {"junction": selected, "hour": hour, "day": 15, "is_holiday": 1 if holiday == "Yes" else 0}
        r = requests.post(API_URL, json=payload, timeout=4)
        if r.status_code == 200:
            count = r.json().get("predicted_count", count)
    except: pass

    level = "Low" if count < 130 else "Medium" if count < 210 else "High / Critical"
    timer = "90s - High Density" if "High" in level else "60s - Moderate" if "Medium" in level else "30s - Eco Mode"
    aqi = int(count * 0.8 + e_density * 0.5)
    aqi_label = "Good" if aqi < 100 else "Moderate" if aqi < 200 else "Poor"
    revenue = int(count * 0.1 * 500)

    if emergency:
        st.error("🚨 EMERGENCY CORRIDOR ACTIVE - All Signals GREEN for Ambulance")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("VEHICLES / HR", f"{count}")
    m2.metric("CONGESTION", level)
    m3.metric("SIGNAL TIMER", timer)
    m4.metric("AQI INDEX", f"{aqi} {aqi_label}")

    st.divider()
    st.subheader("🚨 Risk & Safety Intelligence")
    risk = JUNCTIONS[selected]['risk']
    if "VERY HIGH" in risk: st.error(f"CRITICAL ALERT: {risk} - Limit 20 km/h")
    elif "High" in risk: st.warning(f"WARNING: {risk} - Drive Carefully")
    else: st.success(f"SAFE CORRIDOR: {risk}")

    st.subheader("🅿️ Smart Parking Engine")
    if "High" in level: st.warning(f"Primary Full. Alternate Suggested: {JUNCTIONS[selected]['parking']}")
    else: st.success(f"Slot Available: {JUNCTIONS[selected]['parking']}")

    # Triple Language Voice System
    st.divider()
    st.subheader("🔊 Multilingual Voice Assistant")
    en_text = f"Attention. {level} traffic at {JUNCTIONS[selected]['name']}. Count {count} vehicles per hour. Signal green for {timer}. AQI {aqi}. {risk}."
    hi_text = f"Dhyan dijiye. {JUNCTIONS[selected]['name']} par {level} traffic hai. Gaadiyon ki sankhya {count} prati ghante hai. Signal {timer} hara hai. AQI {aqi} hai."
    bho_text = f"Sunli. {JUNCTIONS[selected]['name']} par bhari jaam ba. {count} gaadi ek ghanta me ba. {level} jaam ba. Signal {timer} khula ba."

    col_en, col_hi, col_bho = st.columns(3)
    with col_en:
        st.markdown("#### English")
        st.caption(en_text)
        aud = get_audio(en_text, 'en')
        if aud: st.audio(aud, format='audio/mp3')
    with col_hi:
        st.markdown("#### Hindi")
        st.caption(hi_text)
        aud = get_audio(hi_text, 'hi')
        if aud: st.audio(aud, format='audio/mp3')
    with col_bho:
        st.markdown("#### Bhojpuri")
        st.caption(bho_text)
        aud = get_audio(bho_text, 'hi')
        if aud: st.audio(aud, format='audio/mp3')

    if role!= "Public User":
        st.divider()
        st.subheader("💰 Enforcement & Revenue Panel")
        x1, x2, x3 = st.columns(3)
        x1.metric("Challans Today", f"{int(count*0.1)}")
        x2.metric("Revenue", f"₹ {revenue}")
        x3.metric("E-Rickshaw Fine", f"₹ {e_density*100}")

    st.divider()
    st.subheader("📈 24-Hour Traffic Forecast")
    hourly_df = pd.DataFrame({"Hour": list(range(24)), "Vehicles": [predict(selected, h) for h in range(24)]})
    st.bar_chart(hourly_df.set_index("Hour"))

    st.subheader("📊 City-Wide Junction Comparison")
    comp_df = pd.DataFrame([{"Junction": JUNCTIONS[j]['name'].split()[0], "Vehicles": predict(j, hour)} for j in JUNCTIONS])
    st.line_chart(comp_df.set_index("Junction"))

    st.download_button("📥 Export Traffic Report", data=hourly_df.to_csv(index=False).encode('utf-8'), file_name=f"Jaunpur_Traffic_Report_J{selected}.csv")

# Admin Panels
st.divider()
with st.expander("🚔 Traffic Police - Live City Dashboard"):
    data = [{"ID": j, "Junction": JUNCTIONS[j]['name'], "Count": predict(j, hour), "Timer": "90s" if predict(j, hour) >= 210 else "60s" if predict(j, hour) >= 130 else "30s", "Risk": JUNCTIONS[j]['risk'], "Status": "🔴 High" if predict(j, hour) >= 210 else "🟠 Med" if predict(j, hour) >= 130 else "🟢 Low"} for j in JUNCTIONS]
    st.dataframe(pd.DataFrame(data), use_container_width=True)

with st.expander("🏛️ Municipal Council - Action Center"):
    m_data = [{"Junction": JUNCTIONS[j]['name'], "Parking": JUNCTIONS[j]['parking'], "Action": "Clear Encroachment" if predict(j, hour) > 210 else "Routine Patrol"} for j in JUNCTIONS]
    st.dataframe(pd.DataFrame(m_data), use_container_width=True)
    if st.button("📤 Forward Report to Commissioner"):
        st.success("Report forwarded to Municipal Commissioner, Jaunpur.")

st.divider()
st.markdown("<center style='color:#666; font-size:12px;'>Jaunpur Smart City Project | AI Traffic Management System | Designed & Developed by Shreya Singh</center>", unsafe_allow_html=True)
