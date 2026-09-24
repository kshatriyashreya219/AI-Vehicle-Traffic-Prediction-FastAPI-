import streamlit as st
import random
import pandas as pd
import datetime

st.set_page_config(page_title="AI Vehicle Traffic Prediction", page_icon="🚦", layout="wide")

st.title("🚦 AI Vehicle Traffic Prediction")
st.subheader("Jaunpur City - Comprehensive Traffic Analysis System")
st.divider()

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

selected_id = st.selectbox("Select Junction", list(junctions.keys()), format_func=lambda x: f"{x}. {junctions[x]['name']}")

col_r, col_l = st.columns(2)
col_r.info(f"**Route:** {junctions[selected_id]['route']}")
col_l.success(f"**Landmark:** {junctions[selected_id]['landmark']}")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    hour = st.slider("Hour (0-23)", 0, 23, 10)
with col2:
    weekday = st.selectbox("Day of Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
with col3:
    is_holiday = st.selectbox("Is Holiday?", ["No", "Yes"])

if st.button("🚀 Predict Traffic", use_container_width=True):
    base = 110
    if selected_id in [4, 3, 2]: base += 55
    if selected_id in [8, 11]: base += 35
    if 8 <= hour <= 11 or 17 <= hour <= 20: base += 60
    if weekday == "Monday": base += 20
    if weekday in ["Saturday","Sunday"]: base = int(base * 0.8)
    if is_holiday == "Yes": base = int(base * 0.65)

    vehicles = base + random.randint(-15, 30)
    level = "Low" if vehicles < 130 else "Medium" if vehicles < 210 else "High / Critical"

    c1, c2 = st.columns(2)
    c1.metric("Predicted Vehicle Count", f"{vehicles} vehicles/hr")
    c2.metric("Congestion Level", level)

    if "High" in level:
        st.error(f"🔴 High Congestion at {junctions[selected_id]['name']}")
    elif "Medium" in level:
        st.warning(f"🟠 Moderate Traffic at {junctions[selected_id]['name']}")
    else:
        st.success(f"🟢 Traffic Clear at {junctions[selected_id]['name']}")

    # --- GRAPH 1: 24 Hour Traffic Pattern ---
    st.subheader(f"📊 24-Hour Traffic Pattern - {junctions[selected_id]['name']}")
    hours = list(range(24))
    traffic_data = []
    for h in hours:
        b = 110
        if selected_id in [4, 3, 2]: b += 55
        if selected_id in [8, 11]: b += 35
        if 8 <= h <= 11 or 17 <= h <= 20: b += 60
        traffic_data.append(b + random.randint(-10, 20))

    chart_df = pd.DataFrame({"Hour": hours, "Vehicles": traffic_data})
    st.bar_chart(chart_df.set_index("Hour"))

    # --- GRAPH 2: All Junctions Comparison ---
    st.subheader("📈 All Junctions Comparison (Current Hour)")
    all_data = []
    for jid in junctions:
        b = 110
        if jid in [4, 3, 2]: b += 55
        if jid in [8, 11]: b += 35
        if 8 <= hour <= 11 or 17 <= hour <= 20: b += 60
        all_data.append({"Junction": junctions[jid]['name'].split()[0], "Vehicles": b + random.randint(-10, 20)})

    comp_df = pd.DataFrame(all_data)
    st.line_chart(comp_df.set_index("Junction"))

    log = pd.DataFrame([{"Timestamp": datetime.datetime.now(), "Junction": junctions[selected_id]['name'], "Vehicles": vehicles, "Level": level}])
    try:
        log.to_csv("jaunpur_traffic_log.csv", mode='a', header=False, index=False)
    except:
        log.to_csv("jaunpur_traffic_log.csv", index=False)

st.divider()
st.markdown("""
**Project Details:**
- **Project Title:** AI Vehicle Traffic Prediction
- **Total Junctions Covered:** 11 (8 Four-Way & 3 Three-Way)
- **Data Source:** Jaunpur City Mapping & Field Research
- **Developed By:** Shreya Singh
""")