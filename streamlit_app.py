import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="dexdogs | Supplier Defense", layout="wide")

# --- HEADER ---
st.title("🏭 dexdogs: The Supplier Survival Simulator")
st.markdown("### Moving from *Static Averages* to *Activity-Based* Carbon Defense")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Factory Settings")
    daily_target = st.slider("Daily Production (Tonnes of Glass)", 5, 100, 20)
    efficiency = st.slider("Process Optimization (%)", 0, 40, 0)
    st.divider()
    st.info("Goal: Defend your Apple contract with high-fidelity data.")

# --- THE MATH ENGINE ---
# 1. The "Average" Way (Spend-based/Industry Average)
avg_intensity = 0.62  # tCO2e per tonne of glass
guess_total = daily_target * avg_intensity

# 2. The "dexdogs" Way (Stoichiometry + Activity)
# Stoichiometry: Soda Ash + Heat = 0.21 tCO2e/tonne (Fixed by Chemistry)
stoic_floor = daily_target * 0.21 
# Activity: Energy used by the furnace (Variable by efficiency)
energy_load = (daily_target * 0.41) * (1 - (efficiency / 100))
dexdogs_total = stoic_floor + energy_load

# --- VISUAL 1: THE METRIC SHOWDOWN ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Industry Average Reporting", f"{guess_total:.2f} tCO2e", delta="STATIC GUESS", delta_color="off")
with col2:
    diff = dexdogs_total - guess_total
    st.metric("dexdogs Digital Twin", f"{dexdogs_total:.2f} tCO2e", delta=f"{diff:.2f} tCO2e SAVED", delta_color="normal")

# --- VISUAL 2: THE CARBON PULSE ---
# Generating 24 hours of simulated activity
hours = np.linspace(0, 24, 48)
# Create a 'pulse' effect where energy spikes when a batch enters the furnace
pulse = [dexdogs_total/12 * (1.5 if i%4==0 else 0.7) for i in range(len(hours))]
df_pulse = pd.DataFrame({'Hour': hours, 'Emissions (kg CO2e)': pulse})

fig = px.area(df_pulse, x='Hour', y='Emissions (kg CO2e)', 
              title="Real-Time Carbon Pulse: Batch Processing vs. Idle Time",
              color_discrete_sequence=['#00d4ff'])
fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# --- THE "AUDIT" DEFENSE ---
st.subheader("🛡️ Auditor Defense Log")
st.write(f"""
- **Stoichiometric Reality**: {stoic_floor:.2f} tonnes of CO2 are chemically locked to your production.
- **Activity Efficiency**: Your furnace idle-time was reduced by {efficiency}%, saving {guess_total - dexdogs_total:.2f} tonnes vs. the industry average.
""")
