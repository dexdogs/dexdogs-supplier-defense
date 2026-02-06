import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="dexdogs | Factory Twin", layout="wide")

# --- APPLE-STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { border: 1px solid #444; padding: 15px; border-radius: 12px; background-color: #161b22; }
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

    while time.time() < t_end:
        # 1. THE VISUAL FLOW MODEL (Like your reference image)
        # We use a Scatter plot with lines to mimic the 'Process Modeling' look
        node_x = [0, 1, 2, 3]
        node_y = [1, 1, 1, 1]
        node_text = ["Raw Materials", "Melting (1550°C)", "Fusion Draw", "Annealing"]
        
        # Color changes based on efficiency gap
        link_color = "#00d4ff" if efficiency_gap < 15 else "#ff4b4b"
        
        fig_flow = go.Figure()
        # Add the connections (Links)
        fig_flow.add_trace(go.Scatter(x=node_x, y=node_y, mode='lines+markers',
                                    line=dict(color=link_color, width=4),
                                    marker=dict(size=40, color="#1f2937", line=dict(color=link_color, width=2))))
        # Add labels
        for x, y, label in zip(node_x, node_y, node_text):
            fig_flow.add_annotation(x=x, y=y-0.2, text=label, showarrow=False, font=dict(color="white"))
        
        fig_flow.update_layout(template="plotly_dark", height=250, xaxis=dict(visible=False), yaxis=dict(visible=False, range=[0, 2]))
        flow_placeholder.plotly_chart(fig_flow, use_container_width=True)

        # 2. TELEMETRY & MATH
        theoretical = (furnace_temp * 0.045)
        actual = theoretical + (efficiency_gap * 1.35)
        now = datetime.now()
        history.append({"Time": now, "Load": actual})
        df_history = pd.DataFrame(history)

        # 3. METRICS UPDATES
        metric_col[0].metric("Theoretic Reaction", f"{theoretical:.2f} kg/t")
        metric_col[1].metric("Actual Emissions", f"{actual:.2f} kg/t", delta=f"{actual-theoretical:.2f} WASTE", delta_color="inverse")
        metric_col[2].metric("Compliance Status", "PASS" if efficiency_gap < 15 else "AUDIT REQ", 
                             delta=f"{100-efficiency_gap}% Score")

        # 4. CARBON PULSE CHART
        fig_pulse = px.line(df_history.tail(30), x='Time', y='Load', title="Real-Time Carbon Pulse")
        fig_pulse.update_layout(template="plotly_dark", height=300)
        chart_col[0].plotly_chart(fig_pulse, use_container_width=True)

        # 5. SEQUENCE PROOF (Gantt)
        tasks = [
            dict(Process="Melting", Start=now-timedelta(minutes=2), Finish=now, Batch="Batch A"),
            dict(Process="Forming", Start=now, Finish=now+timedelta(minutes=2), Batch="Batch A")
        ]
        fig_gantt = px.timeline(pd.DataFrame(tasks), x_start="Start", x_end="Finish", y="Process", color="Batch")
        fig_gantt.update_layout(template="plotly_dark", height=300)
        chart_col[1].plotly_chart(fig_gantt, use_container_width=True)

        time.sleep(2)
else:
    st.info("Start the 5-minute production run to see the Visual Flow Model.")
