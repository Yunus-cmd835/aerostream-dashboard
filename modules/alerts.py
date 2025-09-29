from geopy.distance import geodesic

def detect_collisions(drones, threshold_meters=100):
    alerts = []
    for i in range(len(drones)):
        for j in range(i + 1, len(drones)):
            d1 = drones[i]
            d2 = drones[j]
            dist = geodesic((d1["lat"], d1["lon"]), (d2["lat"], d2["lon"])).meters
            if dist < threshold_meters:
                alerts.append({
                    "type": "Collision Risk",
                    "message": f"{d1['id']} and {d2['id']} are {int(dist)}m apart!",
                    "severity": "High"
                })
    return alerts

def detect_battery_issues(drones, threshold_percent=20):
    alerts = []
    for drone in drones:
        if drone["battery"] < threshold_percent:
            alerts.append({
                "type": "Low Battery",
                "message": f"{drone['id']} battery is at {drone['battery']:.1f}%",
                "severity": "Medium"
            })
    return alerts

def get_all_alerts(drones):
    return detect_collisions(drones) + detect_battery_issues(drones)