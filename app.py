import streamlit as st
import pandas as pd
from modules.simulator import load_drones, simulate_drones
from modules.map import render_map
from modules.alerts import get_all_alerts
from modules.telemetry import render_telemetry_charts
from modules.auth import login, has_permission
from modules.copilot import handle_query
from modules.anomaly import detect_anomalies
from modules.replay import render_replay

# 🔧 Page config
st.set_page_config(page_title="Flight of the Future", layout="wide")

# 🎨 Custom styling
st.markdown("""
    <style>
    .main { background-color: #0f1117; color: #f5f5f5; }
    .block-container { padding: 2rem; }
    h1, h2, h3 { color: #00ffe0; }
    .stButton>button { background-color: #00ffe0; color: black; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# 🏁 Hero Banner
st.markdown("""
<div style="text-align:center; padding:2rem 0;">
    <img src="assets/logo.png" width="200" style="margin-bottom:1rem;" />
    <h1 style="color:#00ffe0; font-size:3rem; margin-bottom:0;">AeroStream</h1>
    <h3 style="color:#f5f5f5; font-weight:normal;">Drone Traffic Manager for the Skies of Tomorrow</h3>
</div>
""", unsafe_allow_html=True)

# 🔐 Sidebar Branding + Login
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.markdown("## 🛩️ AeroStream")
st.sidebar.markdown("Secure. Scalable. Smart.")
st.sidebar.divider()
role = login()
st.sidebar.markdown(f"👤 Role: **{role}**")

# 🔒 Load drones from session
if "drones" not in st.session_state:
    st.session_state.drones = load_drones()

# 🛠️ Refresh button (Operator only)
if has_permission("Operator"):
    if st.sidebar.button("🔄 Refresh Drone Data", key="refresh_operator"):
        st.session_state.drones = simulate_drones(st.session_state.drones)
else:
    st.sidebar.warning("You need Operator access to refresh data.")

# ✅ Define drones before using
drones = st.session_state.drones

# 🎯 Drone Filter Dropdown
drone_ids = [drone["id"] for drone in drones]
selected_drone = st.selectbox("🎯 Focus on a Drone", drone_ids, index=0)
focused = next(d for d in drones if d["id"] == selected_drone)

# 🗂️ Dynamic Tabs Based on Role
tabs = []
tab_labels = []

if has_permission("Viewer"):
    tabs.append("🗺️ Map")
    tab_labels.append("map")

    tabs.append("📊 Metrics")
    tab_labels.append("metrics")

if has_permission("Operator"):
    tabs.append("🚨 Alerts")
    tab_labels.append("alerts")

    tabs.append("📈 Charts")
    tab_labels.append("charts")

if has_permission("Admin") or True:  # 👈 Force show for testing
    tabs.append("📂 Logs")
    tab_labels.append("logs")
    tabs.append("🤖 Copilot")
    tab_labels.append("copilot")

tabs.append("🎬 Replay")
tab_labels.append("replay")

tab_objects = st.tabs(tabs)

# 🔁 Tab loop using zip()
for label, tab in zip(tab_labels, tab_objects):
    with tab:
        if label == "map":
            st.subheader("🗺️ Live Drone Map")
            render_map(drones)

        elif label == "metrics":
            st.subheader(f"📊 Telemetry for {focused['id']}")
            st.metric(label="Speed", value=f"{focused['speed']} km/h")
            st.metric(label="Altitude", value=f"{focused['altitude']} m")
            st.metric(label="Battery", value=f"{focused['battery']:.1f}%")
            st.markdown("#### Battery Level")
            st.progress(int(focused["battery"]))

            st.markdown("#### ⚠️ Anomaly Detection")
            anomalies = detect_anomalies(focused)
            if anomalies:
                for a in anomalies:
                    st.error(a)
            else:
                st.success("✅ No anomalies detected.")

            if "history" in focused and focused["history"]:
                st.markdown("#### 📜 Telemetry History")
                history_df = pd.DataFrame(focused["history"])
                st.dataframe(history_df)
                st.line_chart(history_df.set_index("timestamp")[["speed", "altitude", "battery"]])
            else:
                st.info("No telemetry history available for this drone.")

        elif label == "alerts":
            st.subheader("🚨 Alerts")
            alerts = get_all_alerts(drones)
            if alerts:
                for alert in alerts:
                    st.markdown(f"**{alert['type']}**: {alert['message']} ⚠️")
            else:
                st.success("✅ All drones operating safely.")

        elif label == "charts":
            st.subheader("📈 Telemetry Charts")
            render_telemetry_charts(drones)

        elif label == "logs":
            st.subheader("📂 Mission Logs")
            uploaded_file = st.file_uploader("Upload Flight Plan (.json or .csv)", type=["json", "csv"])
            if uploaded_file:
                st.success("✅ File uploaded successfully!")
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_json(uploaded_file)
                st.dataframe(df)

                st.download_button(
                    label="⬇️ Download Telemetry as CSV",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="telemetry_export.csv",
                    mime="text/csv"
                )

        elif label == "copilot":
            st.subheader("🤖 Ask AeroStream Anything")
            query = st.text_input("🔍 Type your question", placeholder="e.g. Which drone has the lowest battery?")
            if query:
                st.markdown("🧠 Thinking...")
                answer = handle_query(query, drones)
                st.success(answer)

        elif label == "replay":
            st.subheader("🎬 Mission Replay")
            render_replay(focused)