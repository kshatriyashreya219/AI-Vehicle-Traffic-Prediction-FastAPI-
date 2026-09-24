import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Jaunpur Traffic AI | Shreya Singh", page_icon="🚦", layout="wide")

JUNCTION_DATA = {
    1: {"name": "Olandganj Commercial Hub", "type": "CBD", "load": 60},
    2: {"name": "Chaharsu Central Intersection", "type": "City Center", "load": 55},
    3: {"name": "Sadbhavna Bridge - Gomti Corridor", "type": "Bridge Link", "load": 70},
    4: {"name": "JCiz Chauraha", "type": "Transit Junction", "load": 50},
    5: {"name": "Polytechnic Square", "type": "Institutional", "load": 45},
    6: {"name": "Jogiyapur - Sutarhatti", "type": "Old City", "load": 40},
    7: {"name": "Mungra Badshahpur Highway", "type": "Highway - 12KM Jam", "load": 80},
    8: {"name": "Shahganj Road - Station Road", "type": "Logistics Hub", "load": 65}
}

st.title("🚦 Jaunpur TrafficAI")
st.subheader("👩‍💻 Developed by Shreya Singh | Jaunpur Smart City Project")
st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    j_id = st.selectbox("📍 Select Zone", list(JUNCTION_DATA.keys()), format_func=lambda x: JUNCTION_DATA[x]["name"])
with c2:
    hour = st.slider("⏰ Hour", 0, 23, 11)
with c3:
    holiday = st.selectbox("📅 Day Type", ["No", "Yes"])

if st.button("Predict Traffic", use_container_width=True):
    zone = JUNCTION_DATA[j_id]
    base = 120 + (hour*12) + zone["load"] + (0 if holiday=="Yes" else 25)
    if base >= 260: level = "CRITICAL JAM"
    elif base >= 200: level = "HIGH"
    elif base >= 130: level = "MODERATE"
    else: level = "LOW"

    st.metric("Predicted Vehicles", base)
    st.metric("Zone", zone["name"])
    st.metric("Status", level)

    df = pd.DataFrame({"Hour": list(range(24)), "Traffic": [120 + (h*12)+zone["load"] for h in range(24)]})
    fig = px.line(df, x="Hour", y="Traffic", title=f"Forecast for {zone['name']}")
    st.plotly_chart(fig, use_container_width=True)
