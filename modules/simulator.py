import json
import random
from datetime import datetime, timedelta

def load_drones():
    with open("data/drones.json") as f:
        return json.load(f)

def simulate_drones(drones):
    for drone in drones:
        # 🔄 Simulate live values
        drone["lat"] += random.uniform(-0.001, 0.001)
        drone["lon"] += random.uniform(-0.001, 0.001)
        drone["battery"] = max(0, drone["battery"] - random.uniform(0.1, 0.5))
        drone["speed"] += random.uniform(-1, 1)
        drone["altitude"] += random.uniform(-10, 10)

        # ✅ Inject telemetry history
        now = datetime.now()
        drone["history"] = [
            {
                "timestamp": (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M"),
                "speed": round(drone["speed"] - 2, 1),
                "altitude": round(drone["altitude"] + 20, 1),
                "battery": round(drone["battery"] + 5, 1)
            },
            {
                "timestamp": (now - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M"),
                "speed": round(drone["speed"] - 1, 1),
                "altitude": round(drone["altitude"] + 10, 1),
                "battery": round(drone["battery"] + 2, 1)
            },
            {
                "timestamp": now.strftime("%Y-%m-%d %H:%M"),
                "speed": round(drone["speed"], 1),
                "altitude": round(drone["altitude"], 1),
                "battery": round(drone["battery"], 1)
            }
        ]

        # 🎬 Inject mission replay path
        drone["path"] = [
            {
                "time": (now - timedelta(minutes=10)).isoformat(),
                "lat": drone["lat"] - 0.002,
                "lon": drone["lon"] - 0.002
            },
            {
                "time": (now - timedelta(minutes=5)).isoformat(),
                "lat": drone["lat"] - 0.001,
                "lon": drone["lon"] - 0.001
            },
            {
                "time": now.isoformat(),
                "lat": drone["lat"],
                "lon": drone["lon"]
            }
        ]

    return drones