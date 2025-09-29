import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

def render_map(drones):
    avg_lat = sum(d["lat"] for d in drones) / len(drones)
    avg_lon = sum(d["lon"] for d in drones) / len(drones)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6, tiles="CartoDB dark_matter")

    # 🧠 Create cluster group
    cluster = MarkerCluster().add_to(m)

    for drone in drones:
        icon = folium.CustomIcon("assets/drone.png", icon_size=(40, 40))

        popup = folium.Popup(
            f"""
            <b>{drone['id']}</b><br>
            Speed: {drone['speed']} km/h<br>
            Altitude: {drone['altitude']} m<br>
            Battery: {drone['battery']:.1f}%
            """, max_width=250
        )

        folium.Marker(
            location=[drone["lat"], drone["lon"]],
            popup=popup,
            icon=icon,
            tooltip=f"{drone['id']} ({drone['battery']:.1f}%)"
        ).add_to(cluster)

    return st_folium(m, width=800, height=500)