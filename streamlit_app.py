import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="dexdogs | Digital Twin", layout="wide")
st.title("🏗️ dexdogs: Glass Factory Digital Twin")
st.caption("Defending Tier 1 Supplier Contracts with High-Fidelity Data")

# --- SIDEBAR: CONTROL THE REALITY ---
with st.sidebar:
    st.header("Factory Controls")
    furnace_temp = st.slider("Furnace Temp (°C)", 1400, 1700, 1550)
    leak_rate = st.slider("Fuel Line Inefficiency (%)", 0, 20, 5)
    st.divider()
    if st.button("🔄 Reset Simulation"):
        st.rerun()

# --- 1. THE VISUAL DES MODEL (Gantt Chart) ---
st.subheader("1. Discrete Event Model: Batch Flow")
# We simulate 3 typical processes: Melting, Forming, Annealing
tasks = []
start_time = datetime(2026, 2, 6, 8, 0)
for i in range(1, 6): # 5 Batches
    m_start = start_time + timedelta(minutes=(i-1)*30)
    tasks.append(dict(Batch=f"Batch {i}", Start=m_start, Finish=m_start + timedelta(minutes=25), Process="1. Melting (1550°C)"))
    tasks.append(dict(Batch=f"Batch {i}", Start=m_start + timedelta(minutes=26), Finish=m_start + timedelta(minutes=45), Process="2. Fusion Draw (Forming)"))
    tasks.append(dict(Batch=f"Batch {i}", Start=m_start + timedelta(minutes=46), Finish=m_start + timedelta(minutes=70), Process="3. Annealing (Cooling)"))

df_tasks = pd.DataFrame(tasks)
fig_gantt = px.timeline(df_tasks, x_start="Start", x_end="Finish", y="Process", color="Batch", title="Glass Batch Sequencing")
fig_gantt.update_yaxes(autorange="reversed")
st.plotly_chart(fig_gantt, use_container_width=True)

# --- 2. RAW TELEMETRY & WASTE LOG ---
st.subheader("2. Live Telemetry Data (Activity Feed)")
# Generating fake 'sensor' data based on your sliders
telemetry = []
for i in range(10):
    noise = np.random.uniform(-1, 1)
    power = (furnace_temp / 20) + leak_rate + noise
    waste = "Leak Detected" if power > 80 else "Normal"
    telemetry.append({"Timestamp": datetime.now() - timedelta(seconds=i*10), "Sensor_ID": "Furnace_01", "KW_Load": f"{power:.2f}", "Status": waste})

col_a, col_b = st.columns([2, 3])
with col_a:
    st.dataframe(telemetry, use_container_width=True)
with col_b:
    # --- 4. EMISSIONS SPIKE VISUAL ---
    hours = np.linspace(0, 10, 100)
    # The spike is caused by the 'leak_rate' slider
    base_load = np.sin(hours) * 5 + 20
    spike = base_load + (leak_rate * 2) 
    df_pulse = pd.DataFrame({'Time': hours, 'Carbon_Pulse': spike})
    st.plotly_chart(px.line(df_pulse, x='Time', y='Carbon_Pulse', title="Real-Time Carbon Spike (Fuel Inefficiency)"), use_container_width=True)

# --- 3. MATH vs. REALITY ---
st.divider()
st.subheader("3. The 'Gap': Theoretical vs. Actual")
theoretical = (furnace_temp * 0.05) # Stoichiometry math
actual = theoretical + (leak_rate * 1.5) # The reality of waste

m1, m2, m3 = st.columns(3)
m1.metric("Theoretical (Stoichiometry)", f"{theoretical:.2f} kg/t", help="Based on chemical reactions")
m2.metric("Actual (Sensor Data)", f"{actual:.2f} kg/t", delta=f"{actual-theoretical:.2f} WASTE", delta_color="inverse")
m3.metric("Apple Compliance Score", f"{100-leak_rate}%", delta="-4%" if leak_rate > 10 else "Optimal")

st.info("💡 **Demo Strategy**: Show how 'Theoretical Math' is a lie. Only dexdogs captures the **Waste Gap** through real-time telemetry.")
