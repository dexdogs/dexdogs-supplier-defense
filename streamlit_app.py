import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="dexdogs | Factory Twin", layout="wide")

# --- IMPROVED CSS FOR READABILITY ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { border: 1px solid #444; padding: 15px; border-radius: 12px; background-color: #161b22; }
    [data-testid="stMetricValue"] { color: white !important; }
    [data-testid="stMetricLabel"] { color: #888 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ dexdogs: Glass Factory Flow Simulator")
st.caption("Discrete Event Visualization for Apple Tier 1 Compliance")

# --- SOURCES ---
with st.expander("📚 Compliance Documentation"):
    st.markdown("- [Apple Supplier Code of Conduct v5.0](https://www.apple.com/euro/supplier-responsibility/k/generic/pdf/Apple-Supplier-Code-of-Conduct-and-Supplier-Responsibility-Standards.pdf)")
    st.markdown("- [Facility-Level GHG Data Requirements](https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2025.pdf)")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("🎛️ Telemetry Controls")
    furnace_temp = st.slider("Furnace Temp (°C)", 1400, 1750, 1550)
    efficiency_gap = st.slider("System Leak/Waste (%)", 0, 30, 5)
    st.divider()
    sim_start = st.button("🚀 Start 5-Min Production Run", type="primary")

# --- VISUAL SIMULATION ENGINE ---
if sim_start:
    t_end = time.time() + 300 # 5 Minutes
    history = []
    
    # Placeholders for dynamic updates
    flow_placeholder = st.empty()
    metric_col = st.columns(3)
    chart_col = st.columns(2)
    pulse_placeholder = chart_col[0].empty()
    gantt_placeholder = chart_col[1].empty()

    iteration = 0 # Used for unique keys to prevent DuplicateElementId error

    while time.time() < t_end:
        iteration += 1
        
        # 1. THE VISUAL FLOW MODEL (Fixed Visibility)
        node_x = [0, 1, 2, 3]
        node_y = [1, 1, 1, 1]
        node_text = ["<b>Raw Materials</b>", "<b>Melting (Furnace)</b>", "<b>Fusion Draw</b>", "<b>Annealing</b>"]
        
        link_color = "#00d4ff" if efficiency_gap < 15 else "#ff4b4b"
        
        fig_flow = go.Figure()
        fig_flow.add_trace(go.Scatter(x=node_x, y=node_y, mode='lines+markers+text',
                                    text=node_text, textposition="top center",
                                    line=dict(color=link_color, width=6),
                                    marker=dict(size=45, color="#1f2937", line=dict(color=link_color, width=3)),
                                    textfont=dict(color="white", size=14)))
        
        fig_flow.update_layout(template="plotly_dark", height=300, 
                              margin=dict(l=50, r=50, t=50, b=50),
                              xaxis=dict(visible=False), yaxis=dict(visible=False, range=[0.5, 1.5]))
        flow_placeholder.plotly_chart(fig_flow, use_container_width=True, key=f"flow_{iteration}")

        # 2. TELEMETRY & MATH
        theoretical = (furnace_temp * 0.045)
        actual = theoretical + (efficiency_gap * 1.35)
        now = datetime.now()
        history.append({"Time": now, "Load": actual})
        df_history = pd.DataFrame(history)

        # 3. METRICS UPDATES
        metric_col[0].metric("Theoretic Reaction", f"{theoretical:.2f} kg/t")
        metric_col[1].metric("Actual Emissions", f"{actual:.2f} kg/t", delta=f"{actual-theoretical:.2f} WASTE", delta_color="inverse")
        metric_col[2].metric("Compliance Status", "PASS" if efficiency_gap < 15 else "AUDIT REQ", delta=f"{100-efficiency_gap}% Score")

        # 4. CARBON PULSE CHART (Fixed Unique Key)
        fig_pulse = px.line(df_history.tail(30), x='Time', y='Load', title="Real-Time Carbon Pulse (Digital Twin)")
        fig_pulse.update_layout(template="plotly_dark", height=350, margin=dict(t=40, b=20))
        pulse_placeholder.plotly_chart(fig_pulse, use_container_width=True, key=f"pulse_{iteration}")

        # 5. SEQUENCE PROOF (Fixed Unique Key)
        tasks = [
            dict(Process="Melting", Start=now-timedelta(minutes=2), Finish=now, Batch="Batch A"),
            dict(Process="Forming", Start=now, Finish=now+timedelta(minutes=2), Batch="Batch A"),
            dict(Process="Annealing", Start=now+timedelta(minutes=2), Finish=now+timedelta(minutes=4), Batch="Batch A")
        ]
        fig_gantt = px.timeline(pd.DataFrame(tasks), x_start="Start", x_end="Finish", y="Process", color="Batch")
        fig_gantt.update_layout(template="plotly_dark", height=350, margin=dict(t=40, b=20))
        gantt_placeholder.plotly_chart(fig_gantt, use_container_width=True, key=f"gantt_{iteration}")

        time.sleep(2)
else:
    st.info("Start the 5-minute production run to visualize the Glass Factory Flow.")

