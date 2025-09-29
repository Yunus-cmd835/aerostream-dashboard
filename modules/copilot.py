def handle_query(query, drones):
    query = query.lower()

    if "lowest battery" in query:
        lowest = min(drones, key=lambda d: d["battery"])
        return f"🔋 Drone {lowest['id']} has the lowest battery: {lowest['battery']:.1f}%"

    elif "highest altitude" in query or "above" in query:
        threshold = 1000
        high_drones = [d for d in drones if d["altitude"] > threshold]
        if high_drones:
            ids = ", ".join(d["id"] for d in high_drones)
            return f"🛸 Drones above {threshold}m: {ids}"
        else:
            return f"✅ No drones above {threshold}m altitude."

    elif "alerts" in query:
        from modules.alerts import get_all_alerts
        alerts = get_all_alerts(drones)
        if alerts:
            return "\n".join([f"{a['type']}: {a['message']}" for a in alerts])
        else:
            return "✅ No alerts in the last 10 minutes."

    elif "export" in query and "telemetry" in query:
        return "💾 You can export telemetry from the Logs tab using the download button."

    else:
        return "🤷 Sorry, I couldn't understand that. Try asking about battery, altitude, alerts, or telemetry."