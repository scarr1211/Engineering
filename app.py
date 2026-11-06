import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="Smart City Traffic Operations Center", layout="wide")

st.title("🏙️ Traffic Operations Center: City Network Manager")
st.markdown("""
Welcome to the TOC, Engineers! You are managing the city's main transportation corridor connecting **Downtown to the Suburbs**. 
Today, unexpected events are happening. Use the control panel on the sidebar to deploy **Signal Timing Strategies** and **Incident Management Protocols** to minimize delays and prevent gridlock!
""")

# --- SIDEBAR CONTROLS (ENGINEER PERSPECTIVE) ---
st.sidebar.header("🎛️ TOC Incident & Control Panel")

scenario = st.sidebar.selectbox(
    "Active City Event / Incident", 
    [
        "Normal Operations", 
        "🎸 Major Concert at Stadium (Peak Outflow)", 
        "💥 Major Crash on Highway", 
        "🚧 Construction Lane Closure on Urban Grid"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Engineer Interventions")
signal_strategy = st.sidebar.selectbox(
    "Urban Grid Signal Timing", 
    ["Standard Fixed Timing", "Green Wave (Synchronized)", "Manual Flush (Priority Flow)"]
)

incident_response = st.sidebar.selectbox(
    "Incident Management Protocol", 
    ["Do Nothing (Wait for Clearance)", "Deploy Variable Message Signs (Reroute Traffic)", "Emergency Lane Reversal / Closure"]
)

# --- BASE ROUTE DATA MODEL ---
routes_data = {
    "Route": [
        "Route 1: Major Highway", 
        "Route 2: Curvy Bypass", 
        "Route 3: Urban Grid (Downtown)"
    ],
    "Description": [
        "High-speed, multi-lane expressway. Vulnerable to sudden bottleneck crashes.",
        "Winding secondary road. Lower speed limit, acts as a natural bypass.",
        "Dense network with 9 traffic lights and pedestrian crossings."
    ],
    "Base_Time_Min": [15.0, 26.0, 20.0],
    "Base_Congestion": [0.4, 0.2, 0.5], # 0 to 1 scale
    "Base_Crash_Risk": [20, 10, 15]   # Arbitrary safety risk index
}

df = pd.DataFrame(routes_data)

# --- SCENARIO & INTERVENTION LOGIC ---
time_multiplier = 1.0
congestion_adder = 0.0
crash_multiplier = 1.0

# 1. Apply Scenarios
if scenario == "🎸 Major Concert at Stadium (Peak Outflow)":
    # Heavily impacts Urban Grid and Highway near stadium
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] += 0.45
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Congestion'] += 0.25
    time_multiplier = 1.4

elif scenario == "💥 Major Crash on Highway":
    # Major bottleneck on Highway, forces traffic onto alternatives
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Time_Min'] *= 2.5
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Congestion'] = 0.95
    crash_multiplier = 2.0

elif scenario == "🚧 Construction Lane Closure on Urban Grid":
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Time_Min'] *= 1.6
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] = 0.8

# 2. Apply Engineer Interventions
if signal_strategy == "Green Wave (Synchronized)":
    # Improves urban grid flow significantly
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Time_Min'] *= 0.8
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] -= 0.15
elif signal_strategy == "Manual Flush (Priority Flow)":
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Time_Min'] *= 0.7
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] -= 0.25

if incident_response == "Deploy Variable Message Signs (Reroute Traffic)":
    # Alleviates the worst-hit route by spreading traffic across the bypass
    df.loc['Base_Congestion'] = df['Base_Congestion'] * 0.85
    df.loc[df['Route'] == "Route 2: Curvy Bypass", 'Base_Time_Min'] *= 0.9  # smoother flow

# Final calculations
df['Simulated_Travel_Time'] = df['Base_Time_Min'] * time_multiplier
df['Congestion_Percentage'] = np.clip(df['Base_Congestion'], 0.05, 0.98) * 100
df['Safety_Risk_Score'] = df['Base_Crash_Risk'] * crash_multiplier

# --- MAIN DASHBOARD LAYOUT ---
col1, col2, col3 = st.columns(3)

for i, col in enumerate([col1, col2, col3]):
    with col:
        st.subheader(df.loc[i, "Route"])
        st.write(df.loc[i, "Description"])
        st.metric(label="Network Travel Time", value=f"{df.loc[i, 'Simulated_Travel_Time']:.1f} mins")
        st.metric(label="Congestion Level", value=f"{df.loc[i, 'Congestion_Percentage']:.0f}%")
        st.metric(label="Incident / Safety Risk Score", value=f"{df.loc[i, 'Safety_Risk_Score']:.1f}")
        st.markdown("---")

# --- VISUALIZATIONS ---
st.subheader("📊 TOC System Performance: Delay vs. Safety Risk")

fig = px.scatter(
    df, 
    x="Simulated_Travel_Time", 
    y="Safety_Risk_Score", 
    size="Congestion_Percentage", 
    color="Route",
    hover_name="Route",
    text="Route",
    labels={"Simulated_Travel_Time": "Travel Time (Minutes)", "Safety_Risk_Score": "Safety Risk Index"},
    title="Network Corridor Performance (Bubble size = Congestion Level)"
)
fig.update_traces(textposition='top center')
fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

# --- CLASSROOM ENGINEERING CHALLENGES ---
with st.expander("🎓 Traffic Engineering Mission Prompts for Students"):
    st.markdown("""
    * **Mission 1 (The Stadium Event):** Switch the scenario to **Major Concert at Stadium**. Watch how the Urban Grid locks up. Now, test different **Signal Timing Strategies**. Which strategy successfully lowers congestion without shifting all the risk to the highway?
    * **Mission 2 (The Highway Crisis):** Select **Major Crash on Highway**. Look at how high the travel time shoots up. If you choose *Do Nothing*, what happens to secondary roads? Now test *Variable Message Sign Rerouting*—how does active intervention save the system?
    * **Mission 3 (The Trade-Off Dilemma):** As city planners, you have limited police and digital signage resources. When a crisis happens, is it better to optimize speed or prioritize safety? Defend your choice using the bubble chart data!
    """)