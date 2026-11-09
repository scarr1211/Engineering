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
    "Base_Emissions_Co2": [45, 60, 50]
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
    df['Base_Congestion'] += 0.4  
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
    crash_multiplier *= 0.75  
    df['Base_Time_Min'] *= 1.15 

if policy_tool == "Dynamic Congestion Pricing (Toll Highway)":
    df.loc[df['Route'] == "Route 1: Major Highway", 'Base_Congestion'] -= 0.25
    df.loc[df['Route'] == "Route 2: Curvy Bypass", 'Base_Congestion'] += 0.15
elif policy_tool == "Emergency Shuttle Bus Deployment":
    df['Base_Congestion'] -= 0.15  

# Final Calculations
df['Simulated_Travel_Time'] = df['Base_Time_Min'] * time_multiplier
df['Congestion_Percentage'] = np.clip(df['Base_Congestion'], 0.05, 0.98) * 100
df['Safety_Risk_Score'] = df['Base_Crash_Risk'] * crash_multiplier
df['Total_Emissions_Co2'] = df['Base_Emissions_Co2'] * (df['Congestion_Percentage'] / 50) * emissions_multiplier

# --- HANDLE LOGGING ---
if log_button:
    trial_num = len(st.session_state.decision_log) + 1
    avg_time = df['Simulated_Travel_Time'].mean()
    max_congestion = df['Congestion_Percentage'].max()
    total_safety = df['Safety_Risk_Score'].sum()
    total_emissions = df['Total_Emissions_Co2'].sum()
    
    log_entry = {
        "Trial": f"Trial {trial_num}",
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
    st.sidebar.success(f"Trial {trial_num} logged successfully!")

# --- ORGANIZE INTO STREAMLINED TABS ---
tab1, tab2 = st.tabs([
    "🚦 Live Route Status", 
    "📋 Student Decision Log & Graphs"
])

# --- TAB 1: LIVE ROUTE STATUS ---
with tab1:
    st.subheader("Current Corridor Status")
    col1, col2, col3 = st.columns(3)

    for i, col in enumerate([col1, col2, col3]):
        with col:
            st.markdown(f"### {df.loc[i, 'Route']}")
            st.write(df.loc[i, "Description"])
            st.metric(label="Travel Time", value=f"{df.loc[i, 'Simulated_Travel_Time']:.1f} mins", delta=None)
            st.metric(label="Congestion Level", value=f"{df.loc[i, 'Congestion_Percentage']:.0f}%")
            st.metric(label="Safety Risk Index", value=f"{df.loc[i, 'Safety_Risk_Score']:.1f}")
            st.metric(label="Est. CO2 Emissions", value=f"{df.loc[i, 'Total_Emissions_Co2']:.1f} kg")
            st.markdown("---")

# --- TAB 2: STUDENT DECISION LOG & GRAPHS ---
with tab2:
    st.subheader("📋 Student Decision Log & Strategy Comparison")
    
    if len(st.session_state.decision_log) > 0:
        log_df = pd.DataFrame(st.session_state.decision_log)
        
        # Display Data Table
        st.markdown("#### Logged Trials Data Table")
        st.dataframe(log_df, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### 📊 Strategy Comparison Graphs")
        st.markdown("Compare how your different engineering trials performed against each other across all key metrics:")
        
        # Metric Selector for the Comparison Graph
        metric_to_compare = st.selectbox(
            "Select Metric to Compare Across Trials", 
            ["Avg Time (min)", "Max Congestion (%)", "Safety Risk Score", "CO2 Emissions (kg)"]
        )
        
        # Bar chart comparing the trials for the selected metric
        fig_compare = px.bar(
            log_df,
            x="Trial",
            y=metric_to_compare,
            color="Scenario",
            text=metric_to_compare,
            hover_data=["Signals", "Speed Control", "Policy"],
            title=f"Comparison of Logged Strategies: {metric_to_compare}"
        )
        fig_compare.update_traces(textposition='outside')
        fig_compare.update_layout(height=450)
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # Download and Clear options
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
        st.info("Test out different scenarios and policies, then click **'📝 Log Strategy & System Data'** in the sidebar to populate your comparison graphs!")

# --- CHALLENGES ---
st.markdown("---")
with st.expander("🎓 Advanced Systems Engineering Missions"):
    st.markdown("""
    * **Mission 1 (The Blizzard Challenge):** Set the scenario to **Severe Winter Storm**. Log a trial with *Standard Speed Limits*, then log a second trial with *Dynamic Variable Speed Limits (VSL)*. Check the **Student Decision Log & Graphs** tab to visually compare how much VSL dropped your Safety Risk score!
    * **Mission 2 (The Transit Strike Crisis):** During a **Metro / Transit Strike**, compare CO2 emissions across multiple policy choices using the comparison bar chart.
    * **Mission 3 (The Multi-Objective Dilemma):** Use the dropdown menu in the comparison tab to cycle through Travel Time, Congestion, Safety, and Emissions. Which trial was your most balanced engineering success? Prove it using the charts and download your CSV report.
    """)