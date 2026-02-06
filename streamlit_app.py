import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="dexdogs | Automated Twin", layout="wide")

# --- IMPROVED VISIBILITY CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { border: 1px solid #444; padding: 15px; border-radius: 12px; background-color: #161b22; }
    [data-testid="stMetricValue"] { color: white !important; }
    [data-testid="stMetricLabel"] { color: #888 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ dexdogs: Automated Glass Factory Twin")
st.caption("1-Minute Autonomous Simulation for Apple Tier 1 Compliance")

# --- COMPLIANCE LINKS ---
with st.expander("📚 Compliance Documentation"):
    st.markdown("- [Apple Supplier Code of Conduct v5.0](https://www.apple.com/euro/supplier-responsibility/k/generic/pdf/Apple-Supplier-Code-of-Conduct-and-Supplier-Responsibility-Standards.pdf)")
    st.markdown("- [Facility-Level GHG Data Requirements](https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2025.pdf)")

if st.button("🚀 Start 1-Minute Automated Run", type="primary"):
    t_start = time.time()
    t_end = t_start + 60 # 60 Second Duration
    history = []
    
    # Placeholders
    flow_placeholder = st.empty()
    metric_col = st.columns(3)
    chart_col = st.columns(2)
    iteration = 0

    while time.time() < t_end:
        iteration += 1
        elapsed = time.time() - t_start
        
        # --- AUTOMATED LOGIC ---
        # 1. Normal State (0-30s) vs. Spike State (30-60s)
        is_spiking = True if elapsed > 30 else False
        base_temp = 1550
        waste_factor = 1.2 if not is_spiking else 4.5 # Automatic spike at 30s
        link_color = "#00d4ff" if not is_spiking else "#ff4b4b"
        status_msg = "OPTIMAL" if not is_spiking else "INEFFICIENCY DETECTED"

        # 2. FLOW MODEL (2 STEPS)
        node_x = [0.5, 2.5]
        node_y = [1, 1]
        node_text = ["<b>Step 1: Melting (1550°C)</b>", "<b>Step 2: Fusion Draw (Forming)</b>"]
        
        fig_flow = go.Figure()
        fig_flow.add_trace(go.Scatter(x=node_x, y=node_y, mode='lines+markers+text',
                                    text=node_text, textposition="top center",
                                    line=dict(color=link_color, width=8),
                                    marker=dict(size=50, color="#1f2937", line=dict(color=link_color, width=3)),
                                    textfont=dict(color="white", size=16)))
        fig_flow.update_layout(template="plotly_dark", height=250, xaxis=dict(visible=False), yaxis=dict(visible=False, range=[0.5, 1.5]))
        flow_placeholder.plotly_chart(fig_flow, use_container_width=True, key=f"f_{iteration}")

        # 3. THE MATH & TELEMETRY
        theoretical = (base_temp * 0.045)
        actual = theoretical + (waste_factor * 2.5)
        now = datetime.now()
        history.append({"Time": now, "Load": actual})
        df_history = pd.DataFrame(history)

        # 4. METRICS
        metric_col[0].metric("Theoretical Reaction", f"{theoretical:.2f} kg/t")
        metric_col[1].metric("Actual Emissions", f"{actual:.2f} kg/t", delta=f"{actual-theoretical:.2f} WASTE", delta_color="inverse")
        metric_col[2].metric("Process Status", status_msg)

        # 5. CARBON PULSE (Line Chart)
        fig_pulse = px.line(df_history, x='Time', y='Load', title="Autonomous Carbon Pulse Tracking")
        fig_pulse.update_layout(template="plotly_dark", height=350)
        chart_col[0].plotly_chart(fig_pulse, use_container_width=True, key=f"p_{iteration}")

        # 6. SEQUENCE PROOF (Gantt)
        tasks = [dict(Process="Melting", Start=now-timedelta(seconds=10), Finish=now, Batch="Batch 01")]
        if elapsed > 10:
             tasks.append(dict(Process="Forming", Start=now, Finish=now+timedelta(seconds=10), Batch="Batch 01"))
        
        fig_gantt = px.timeline(pd.DataFrame(tasks), x_start="Start", x_end="Finish", y="Process", color="Batch")
        fig_gantt.update_layout(template="plotly_dark", height=350)
        chart_col[1].plotly_chart(fig_gantt, use_container_width=True, key=f"g_{iteration}")

        time.sleep(1) # Faster refresh for 1-min demo
else:
    st.info("Click 'Start 1-Minute Automated Run' to begin. The simulation will auto-trigger a waste event at 30 seconds.")
