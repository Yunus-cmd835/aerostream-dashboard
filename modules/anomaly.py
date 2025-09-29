def detect_anomalies(drone):
    anomalies = []

    # Battery drop check
    history = drone.get("history", [])
    if len(history) >= 2:
        drop = history[-2]["battery"] - history[-1]["battery"]
        if drop > 10:
            anomalies.append(f"🔋 Battery dropped by {drop:.1f}%")

    # Altitude spike check
    if len(history) >= 2:
        spike = history[-1]["altitude"] - history[-2]["altitude"]
        if abs(spike) > 100:
            anomalies.append(f"🛸 Altitude changed by {spike:.1f}m")

    # Speed threshold
    if drone["speed"] > 120:
        anomalies.append(f"⚠️ Speed exceeds safe limit: {drone['speed']:.1f} km/h")

    return anomalies