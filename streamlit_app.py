import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime, timedelta

# --- PAGE SETUP ---
st.set_page_config(page_title="dexdogs | Digital Twin", layout="wide")

# --- CUSTOM CSS (Apple-Style Dark Theme) ---
st.markdown("""
    <style>
    .main { background-color: #808080; }
    .stMetric { 
        border: 1px solid #444; 
        padding: 15px; 
        border-radius: 12px; 
        background-color: #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ dexdogs: Glass Factory Digital Twin")
st.caption("Verifying the 'Carbon Pulse' for Apple Supplier Compliance (2026)")

# --- SOURCES & COMPLIANCE LINKS ---
with st.expander("📚 Official Compliance Sources (Tier 1 Auditing)"):
    st.write("Apple requires activity-based facility data. Reference these for your audit:")
    st.markdown("- [Apple 2025 Environmental Progress Report](https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2025.pdf)")
    st.markdown("- [Apple Supplier Code of Conduct v5.0](https://www.apple.com/euro/supplier-responsibility/k/generic/pdf/Apple-Supplier-Code-of-Conduct-and-Supplier-Responsibility-Standards.pdf)")
    st.markdown("- [Supplier Clean Energy Program Update](https://www.apple.com/environment/pdf/Apple_Supplier_Clean_Energy_Program_Update_2022.pdf)")

# --- SIDEBAR: SIMULATION CONTROLS ---
with st.sidebar:
    st.header("🎛️ Factory Telemetry Controls")
    furnace_temp = st.slider("Furnace Temp (°C)", 1400, 1750, 1550)
    waste_leak = st.slider("Fuel Line Inefficiency (%)", 0, 25, 5)
    
    st.divider()
    sim_start = st.button("🚀 Start 5-Min Digital Twin Run", type="primary")
    st.info("The simulation models Melting, Forming, and Annealing sequences.")

# --- THE SIMULATION ENGINE ---
if sim_start:
    t_end = time.time() + 60 * 5  # 5 Minute Countdown
    progress_bar = st.progress(0)
    
    # Visual Layout
    col_metrics = st.columns(3)
    m1_placeholder = col_metrics[0].empty()
    m2_placeholder = col_metrics[1].empty()
    m3_placeholder = col_metrics[2].empty()
    
    st.divider()
    
    chart_col1, chart_col2 = st.columns(2)
    pulse_placeholder = chart_col1.empty()
    gantt_placeholder = chart_col2.empty()
    
    status_timer = st.empty()

    # Simulation Data History
    history = []
    
    while time.time() < t_end:
        rem_time = int(t_end - time.time())
        mins, secs = divmod(rem_time, 60)
        
        # 1. Update Progress & Timer
        status_timer.subheader(f"⏱️ Live Run Time Remaining: {mins:02d}:{secs:02d}")
        progress_bar.progress(1 - (rem_time / 300))
        
        # 2. Generate Real-Time Telemetry Load
        # Math: Base load from temp + inefficiency waste + random fluctuation
        current_load = (furnace_temp / 20) + (waste_leak * 1.8) + np.random.uniform(-1.5, 1.5)
        history.append({"Time": datetime.now(), "Load_kW": current_load})
        df_history = pd.DataFrame(history)
        
        # 3. Visual: The Carbon Pulse (Line Chart)
        fig_pulse = px.line(df_history.tail(40), x='Time', y='Load_kW', 
                           title="Real-Time Carbon Pulse (Sensor Data)",
                           color_discrete_sequence=['#00d4ff'])
        fig_pulse.update_layout(template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20))
        pulse_placeholder.plotly_chart(fig_pulse, use_container_width=True)
        
        # 4. Visual: The Sequence Proof (Gantt Chart)
        now = datetime.now()
        tasks = []
        for i in range(1, 4): # Showing last 3 batches
            tasks.append(dict(Batch=f"Batch {i}", Start=now - timedelta(minutes=i*2), Finish=now + timedelta(minutes=1-i), Process="Melting"))
            tasks.append(dict(Batch=f"Batch {i}", Start=now + timedelta(minutes=2), Finish=now + timedelta(minutes=5), Process="Forming"))
            tasks.append(dict(Batch=f"Batch {i}", Start=now + timedelta(minutes=6), Finish=now + timedelta(minutes=9), Process="Annealing"))
        
        df_tasks = pd.DataFrame(tasks)
        fig_gantt = px.timeline(df_tasks, x_start="Start", x_end="Finish", y="Process", color="Batch",
                               title="Verified Production Sequence (Activity-Based)")
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20))
        gantt_placeholder.plotly_chart(fig_gantt, use_container_width=True)

        # 5. The 'Contract Defense' Metrics
        # Stoichiometry logic: Chemical emissions are tied to temp/production
        theoretical = (furnace_temp * 0.045)
        actual = theoretical + (waste_leak * 1.35)
        
        m1_placeholder.metric("Theory (Stoichiometry)", f"{theoretical:.2f} kg/t")
        m2_placeholder.metric("Actual (Digital Twin)", f"{actual:.2f} kg/t", delta=f"{actual-theoretical:.2f} WASTE", delta_color="inverse")
        m3_placeholder.metric("Apple Compliance Score", f"{100-waste_leak}%", delta="-3%" if waste_leak > 10 else "Optimal")
        
        time.sleep(1.5) # Refresh rate for the 'Live' feel
else:
    st.info("👉 Click the blue **'Start 5-Min Digital Twin Run'** button in the sidebar to begin the simulation.")
    st.write("This demo illustrates how activity-based data defends your contract by identifying inefficiencies that static averages hide.")

# --- FOOTER ---
st.divider()
st.caption("dexdogs © 2026 | Built for the 30-Day Climate Tech Challenge")

