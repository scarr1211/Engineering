import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="Transportation Route Optimizer", layout="wide")

st.title("🚦 Smart City Transportation Dashboard")
st.markdown("""
Welcome, Traffic Engineers! Your goal is to analyze three different routes from **Home (Point A)** to **School/Work (Point B)**. 
Use the controls on the sidebar to change environmental conditions and see how each route performs in terms of **Travel Time**, **Congestion Risk**, and **Crash History**.
""")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Simulation Controls")
time_of_day = st.sidebar.selectbox("Time of Day", ["Off-Peak / Midday", "Morning Rush Hour", "Late Night"])
weather = st.sidebar.selectbox("Weather Conditions", ["Clear & Dry", "Heavy Rain / Snow", "Foggy"])
accident_factor = st.sidebar.slider("Driver Aggressiveness / Incident Multiplier", 0.5, 2.0, 1.0, 0.1)

# --- ROUTE DATA MODEL ---
routes_data = {
    "Route": [
        "Route 1: Straight Highway", 
        "Route 2: Curvy Scenic Road", 
        "Route 3: Urban Grid (Intersections)"
    ],
    "Description": [
        "High speed limit, 0 intersections, high traffic volume.",
        "Winding roads, low traffic, longer distance, low crash rate.",
        "Multiple traffic lights, pedestrian crossings, moderate speed."
    ],
    "Base_Time_Min": [15.0, 28.0, 22.0],
    "Base_Congestion_Risk": [0.7, 0.1, 0.5],
    "Base_Crash_History_Per_Year": [45, 12, 28],
    "Intersections": [0, 1, 9]
}

df = pd.DataFrame(routes_data)

# --- DYNAMIC ADJUSTMENTS BASED ON CONTROLS ---
time_multiplier = 1.0
congestion_adder = 0.0
if time_of_day == "Morning Rush Hour":
    time_multiplier = 1.6
    congestion_adder = 0.25
elif time_of_day == "Late Night":
    time_multiplier = 0.8
    congestion_adder = -0.1

weather_multiplier = 1.0
if weather == "Heavy Rain / Snow":
    weather_multiplier = 1.4
elif weather == "Foggy":
    weather_multiplier = 1.2

df['Expected_Time'] = df['Base_Time_Min'] * time_multiplier * weather_multiplier
np.random.seed(42)
df['Simulated_Time'] = df['Expected_Time'] + np.random.uniform(-2, 3, len(df))
df['Congestion_Probability'] = np.clip(df['Base_Congestion_Risk'] + congestion_adder, 0.05, 0.95) * 100
df['Adjusted_Crash_Risk'] = df['Base_Crash_History_Per_Year'] * weather_multiplier * accident_factor

# --- MAIN DASHBOARD LAYOUT ---
col1, col2, col3 = st.columns(3)

for i, col in enumerate([col1, col2, col3]):
    with col:
        st.subheader(df.loc[i, "Route"])
        st.write(df.loc[i, "Description"])
        st.metric(label="Estimated Travel Time", value=f"{df.loc[i, 'Simulated_Time']:.1f} mins")
        st.metric(label="Congestion Probability", value=f"{df.loc[i, 'Congestion_Probability']:.0f}%")
        st.metric(label="Annual Crash History Index", value=f"{df.loc[i, 'Adjusted_Crash_Risk']:.1f}")
        st.markdown("---")

# --- VISUALIZATIONS ---
st.subheader("📊 Trade-off Analysis: Time vs. Safety")

fig = px.scatter(
    df, 
    x="Simulated_Time", 
    y="Adjusted_Crash_Risk", 
    size="Congestion_Probability", 
    color="Route",
    hover_name="Route",
    text="Route",
    labels={"Simulated_Time": "Expected Travel Time (Minutes)", "Adjusted_Crash_Risk": "Crash Risk Index"},
    title="Route Comparison Bubble Chart (Bubble size = Congestion Probability)"
)
fig.update_traces(textposition='top center')
fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

# --- CLASSROOM CHALLENGE SECTION ---
with st.expander("🎓 Engineering Challenge Prompts for Students"):
    st.markdown("""
    * **Scenario A (The Speed Demon):** If a commuter values time above everything else, which route should they pick during **Morning Rush Hour**? What is the hidden cost?
    * **Scenario B (Weather Emergency):** Switch the weather to **Heavy Rain / Snow**. Notice how Route 1 (Highway) changes compared to Route 2 (Curvy). Why do highways become much more dangerous in bad weather?
    * **Scenario C (Infrastructure Fix):** Imagine you are city planners. If you have a budget to add smart traffic lights to Route 3 or widen Route 1, which project gives the best safety-to-time ratio?
    """)