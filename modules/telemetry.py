import pandas as pd
import plotly.express as px
import streamlit as st

def render_telemetry_charts(drones):
    df = pd.DataFrame(drones)

    st.markdown("### 📈 Speed Chart")
    fig_speed = px.bar(df, x="id", y="speed", color="id", title="Drone Speeds (km/h)")
    fig_speed.update_layout(transition={'duration': 0})
    st.plotly_chart(fig_speed, use_container_width=True)

    st.markdown("### 🛫 Altitude Chart")
    fig_alt = px.line(df, x="id", y="altitude", markers=True, title="Drone Altitudes (m)")
    fig_alt.update_layout(transition={'duration': 0})
    st.plotly_chart(fig_alt, use_container_width=True)

    st.markdown("### 🔋 Battery Chart")
    fig_battery = px.pie(df, names="id", values="battery", title="Battery Levels (%)")
    st.plotly_chart(fig_battery, use_container_width=True)