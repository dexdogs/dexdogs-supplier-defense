import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="dexdogs | Digital Twin", layout="wide")

# --- CUSTOM CSS FOR THE 'APPLE' LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { border: 1px solid #333; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_base_with_logic=True)

st.title("🏗️ dexdogs: Glass Factory Digital Twin")
st.caption("Verifying the 'Carbon Pulse' for Apple Supplier Compliance (2026)")

# --- SOURCES & COMPLIANCE LINKS ---
with st.expander("📚 Official Compliance Sources"):
    st.write("Apple requires facility-level data. Reference these for your audit:")
    st.markdown("- [Apple 2025 Environmental Progress Report](https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2025.pdf)")
    st.markdown("- [Apple Supplier Code of Conduct v5.0](https://www.apple.com/euro/supplier-responsibility/k/generic/pdf/Apple-Supplier-Code-of-Conduct-and-Supplier-Responsibility-Standards.pdf)")
    st.markdown("- [Supplier Clean Energy Program Update](https://www.apple.com/environment/pdf/Apple_Supplier_Clean_Energy_Program_Update_2022.pdf)")

# --- SIDEBAR: SIMULATION CONTROLS ---
with st.sidebar:
    st.header("Factory Controls")
    furnace_temp = st.slider("Furnace Temp (°C)", 1400, 1750, 1550)
    waste_leak = st.slider("Fuel Line Inefficiency (%)", 0, 25, 5)
    
    st.divider()
    sim_start = st.button("🚀 Start 5-Min Simulation", type="primary")

# --- THE SIMULATION ENGINE ---
if sim_start:
    t_end = time.time() + 60 * 5 # 5 Minutes
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Placeholders for live-updating charts
    m1, m2 = st.columns(2)
    with m1: pulse_chart = st.empty()
    with m2: gantt_chart = st.empty()
    log_table = st.empty()

    # Data lists to store simulation history
    history = []
    
    while time.time() < t_end:
        rem_time = int(t_end - time.time())
        mins, secs = divmod(rem_time, 60)
        
        # 1. Update Progress & Timer
        status_text.metric("Simulation Time Remaining", f"{mins:02d}:{secs:02d}")
        progress_bar.progress(1 - (rem_time / 300))
        
        # 2. Generate Real-Time Telemetry
        current_load = (furnace_temp / 20) + (waste_leak * 1.8) + np.random.uniform(-2, 2)
        history.append({"Time": datetime.now(), "Load_kW": current_load})
        df_history = pd.DataFrame(history)
        
        # 3. Visual 1: The Carbon Pulse (Line Chart)
        fig_pulse = px.line(df_history.tail(30), x='Time', y='Load_kW', 
                           title="Real-Time Carbon Pulse (kW Load)",
                           color_discrete_sequence=['#00d4ff'])
        fig_pulse.update_layout(template="plotly_dark", height=300)
        pulse_chart.plotly_chart(fig_pulse, use_container_width=True)
        
        # 4. Visual 2: The Sequence (Gantt Chart)
        # Showing batches moving through: Melting -> Forming -> Annealing
        tasks = []
        now = datetime.now()
        for i in range(1, 4):
            tasks.append(dict(Batch=f"Batch {i}", Start=now - timedelta(minutes=i*2), Finish=now + timedelta(minutes=5-i), Process="Melting"))
            tasks.append(dict(Batch=f"Batch {i}", Start=now + timedelta(minutes=6), Finish=now + timedelta(minutes=10), Process="Forming"))
        
        df_tasks = pd.DataFrame(tasks)
        fig_gantt = px.timeline(df_tasks, x_start="Start", x_end="Finish", y="Process", color="Batch")
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(template="plotly_dark", height=300)
        gantt_chart.plotly_chart(fig_gantt, use_container_width=True)

        # 5. Reality Check Metrics
        theoretical = (furnace_temp * 0.04)
        actual = theoretical + (waste_leak * 1.2)
        
        # Show Metrics at the bottom
        c1, c2, c3 = st.columns(3)
        c1.metric("Theory (Stoichiometry)", f"{theoretical:.2f} kg/t")
        c2.metric("Actual (Digital Twin)", f"{actual:.2f} kg/t", delta=f"{actual-theoretical:.2f} Waste")
        c3.metric("Apple Compliance", f"{100-waste_leak}%", delta="-5%" if waste_leak > 10 else "Optimal")
        
        time.sleep(2) # Update every 2 seconds for a smooth 'Live' feel
else:
    st.info("Click 'Start Simulation' in the sidebar to begin the 5-minute Digital Twin run.")
