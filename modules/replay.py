import folium
from folium.plugins import TimestampedGeoJson
from streamlit_folium import st_folium

def render_replay(drone):
    m = folium.Map(location=[drone["lat"], drone["lon"]], zoom_start=13, tiles="CartoDB dark_matter")

    features = []
    for point in drone.get("path", []):
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point["lon"], point["lat"]],
            },
            "properties": {
                "time": point["time"],
                "popup": f"{drone['id']} @ {point['time']}",
                "icon": "circle",
                "iconstyle": {
                    "fillColor": "#00ffe0",
                    "fillOpacity": 0.8,
                    "stroke": "true",
                    "radius": 6
                }
            }
        })

    TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        period="PT5M",
        add_last_point=True,
        auto_play=True,
        loop=False,
        max_speed=1,
    ).add_to(m)

    st_folium(m, width=800, height=500)