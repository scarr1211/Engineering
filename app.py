import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="Smart City Traffic Operations Center", layout="wide")

st.title("🏙️ Traffic Operations Center: Advanced Systems Manager")
st.markdown("""
Welcome back, Chief Engineers! The city is facing complex, multi-layered crises today. 
Use your advanced control panel to balance **Travel Time**, **Safety Risk**, **Budget/Pricing**, and **Environmental Emissions**.
""")

# --- INITIALIZE SESSION STATE ---
if 'decision_log' not in st.session_state:
    st.session_state.decision_log = []

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Advanced TOC Control Panel")

scenario = st.sidebar.selectbox(
    "Active City Event / Crisis", 
    [
        "Normal Operations", 
        "🎸 Major Concert at Stadium (Peak Outflow)", 
        "💥 Major Crash on Highway", 
        "🚧 Construction Lane Closure on Urban Grid",
        "🌨️ Severe Winter Storm / Ice Storm",
        "🚇 Metro / Transit Strike (Surge)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Infrastructure & Policy Controls")

signal_strategy = st.sidebar.selectbox(
    "Urban Grid Signal Timing", 
    ["Standard Fixed Timing", "Green Wave (Synchronized)", "Manual Flush (Priority Flow)"]
)

speed_control = st.sidebar.selectbox(
    "Highway Speed Management", 
    ["Standard Speed Limits", "Dynamic Variable Speed Limits (VSL)", "Speed Reduction Warning Signs"]
)

policy_tool = st.sidebar.selectbox(
    "Economic / Transit Policy", 
    ["No Tolls (Free Flow)", "Dynamic Congestion Pricing (Toll Highway)", "Emergency Shuttle Bus Deployment"]
)

log_button = st.sidebar.button("📝 Log Strategy & System Data", type="primary")

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
    "Base_Congestion": [0.4, 0.2, 0.5], 
    "Base_Crash_Risk": [20, 10, 15],
    "Base_Emissions_Co2": [4.5, 6.0, 5.0] # kg of CO2 per trip average
}

df = pd.DataFrame(routes_data)

# --- SCENARIO LOGIC ---
time_multiplier = 1.0
crash_multiplier = 1.0
emissions_multiplier = 1.0

if scenario == "🎸 Major Concert at Stadium (Peak Outflow)":
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] += 0.45
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Congestion'] += 0.25
    time_multiplier = 1.4

elif scenario == "💥 Major Crash on Highway":
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Time_Min'] *= 2.5
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Congestion'] = 0.95
    crash_multiplier = 2.2

elif scenario == "🚧 Construction Lane Closure on Urban Grid":
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Time_Min'] *= 1.6
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] = 0.8

elif scenario == "🌨️ Severe Winter Storm / Ice Storm":
    time_multiplier = 1.8
    crash_multiplier = 3.0
    df['Base_Congestion'] += 0.3
    emissions_multiplier = 1.5

elif scenario == "🚇 Metro / Transit Strike (Surge)":
    df['Base_Congestion'] += 0.4  # Everyone forced into cars
    time_multiplier = 1.5
    emissions_multiplier = 1.8

# --- INTERVENTION LOGIC ---
if signal_strategy == "Green Wave (Synchronized)":
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Time_Min'] *= 0.8
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] -= 0.15
elif signal_strategy == "Manual Flush (Priority Flow)":
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Time_Min'] *= 0.7
    df.loc[df['Route'] == "Route 3: Urban Grid (Downtown)", 'Base_Congestion'] -= 0.25

if speed_control == "Dynamic Variable Speed Limits (VSL)":
    crash_multiplier *= 0.75  # Calms traffic down, reduces severe crashes
    df['Base_Time_Min'] *= 1.15 # Slight time penalty for lower speeds

if policy_tool == "Dynamic Congestion Pricing (Toll Highway)":
    # Shifts traffic away from highway onto bypass
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Congestion'] -= 0.25
    df.loc[df['Route'] == "Route 2: Curvy Bypass", 'Base_Congestion'] += 0.15
elif policy_tool == "Emergency Shuttle Bus Deployment":
    df['Base_Congestion'] -= 0.15  # Takes cars off the road globally

# Final Calculations
df['Simulated_Travel_Time'] = df['Base_Time_Min'] * time_multiplier
df['Congestion_Percentage'] = np.clip(df['Base_Congestion'], 0.05, 0.98) * 100
df['Safety_Risk_Score'] = df['Base_Crash_Risk'] * crash_multiplier
df['Total_Emissions_Co2'] = df['Base_Emissions_Co2'] * (df['Congestion_Percentage'] / 50) * emissions_multiplier

# --- HANDLE LOGGING ---
if log_button:
    avg_time = df['Simulated_Travel_Time'].mean()
    max_congestion = df['Congestion_Percentage'].max()
    total_safety = df['Safety_Risk_Score'].sum()
    total_emissions = df['Total_Emissions_Co2'].sum()
    
    log_entry = {
        "Scenario": scenario,
        "Signals": signal_strategy,
        "Speed Control": speed_control,
        "Policy": policy_tool,
        "Avg Time (min)": round(avg_time, 1),
        "Max Congestion (%)": round(max_congestion, 1),
        "Safety Risk Score": round(total_safety, 1),
        "CO2 Emissions (kg)": round(total_emissions, 1)
    }
    st.session_state.decision_log.append(log_entry)
    st.sidebar.success("Trial successfully logged!")

# --- MAIN METRICS DISPLAY ---
col1, col2, col3 = st.columns(3)

for i, col in enumerate([col1, col2, col3]):
    with col:
        st.subheader(df.loc[i, "Route"])
        st.write(df.loc[i, "Description"])
        st.metric(label="Travel Time", value=f"{df.loc[i, 'Simulated_Travel_Time']:.1f} mins")
        st.metric(label="Congestion Level", value=f"{df.loc[i, 'Congestion_Percentage']:.0f}%")
        st.metric(label="Safety Risk Index", value=f"{df.loc[i, 'Safety_Risk_Score']:.1f}")
        st.metric(label="Est. CO2 Emissions", value=f"{df.loc[i, 'Total_Emissions_Co2']:.1f} kg")
        st.markdown("---")

# --- VISUALIZATION ---
st.subheader("📊 System Trade-Off Analysis: Delay vs. Safety Risk")

fig = px.scatter(
    df, 
    x="Simulated_Travel_Time", 
    y="Safety_Risk_Score", 
    size="Congestion_Percentage", 
    color="Route",
    hover_name="Route",
    text="Route",
    labels={"Simulated_Travel_Time": "Travel Time (Minutes)", "Safety_Risk_Score": "Safety Risk Index"},
    title="Network Performance (Bubble size = Congestion Level)"
)
fig.update_traces(textposition='top center')
fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

# --- STUDENT DECISION LOG ---
st.markdown("---")
st.subheader("📋 Student Decision Log & Environmental Report")

if len(st.session_state.decision_log) > 0:
    log_df = pd.DataFrame(st.session_state.decision_log)
    st.dataframe(log_df, use_container_width=True)
    
    csv_data = log_df.to_csv(index=False).encode('utf-8')
    col_dl1, col_dl2 = st.columns([1, 4])
    with col_dl1:
        st.download_button(
            label="📥 Download Report (.csv)",
            data=csv_data,
            file_name="advanced_traffic_report.csv",
            mime="text/csv",
        )
    with col_dl2:
        if st.button("🗑️ Clear Log"):
            st.session_state.decision_log = []
            st.rerun()
else:
    st.info("Test out different severe weather or strike scenarios combined with toll policies and signal timing, then click **'📝 Log Strategy'** to build your report!")

# --- CHALLENGES ---
with st.expander("🎓 Advanced Systems Engineering Missions"):
    st.markdown("""
    * **Mission 1 (The Blizzard Challenge):** Set the scenario to **Severe Winter Storm**. Notice how dangerous the highway becomes. Test whether **Dynamic Variable Speed Limits (VSL)** successfully lower the safety risk score, and calculate the time trade-off.
    * **Mission 2 (The Transit Strike Crisis):** During a **Metro / Transit Strike**, congestion spikes everywhere. Compare what happens to $CO_2$ emissions if you use **Congestion Pricing** versus doing nothing. How do economic policies protect air quality?
    * **Mission 3 (The Multi-Objective Dilemma):** As chief city planners, you can't minimize everything at once. Find a strategy combination that keeps safety high and emissions low *without* doubling the average travel time. Prove it using your downloaded CSV data!
    """)