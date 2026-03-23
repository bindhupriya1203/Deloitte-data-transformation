import json
import datetime


# ✅ Convert Format 1
def convertFromFormat1(data):
    # Timestamp
    timestamp = data.get("timestamp")

    # Device
    device_id = data.get("deviceID") or data.get("deviceId") or data.get("device", {}).get("id")
    device_type = data.get("deviceType") or data.get("device", {}).get("type")

    # Location
    location_value = data.get("location")

    if isinstance(location_value, str):
        parts = location_value.split("/")
        location = {
            "country": parts[0],
            "city": parts[1],
            "area": parts[2],
            "factory": parts[3],
            "section": parts[4]
        }
    else:
        location = location_value

    # ✅ Auto-detect status & temperature
    status = None
    temperature = None

    for key, value in data.items():
        if isinstance(value, dict):
            if "status" in value and "temperature" in value:
                status = value["status"]
                temperature = value["temperature"]
                break

    # fallback
    if status is None:
        status = data.get("status")

    if temperature is None:
        temperature = data.get("temperature")

    return {
        "deviceId": device_id,
        "deviceType": device_type,
        "timestamp": timestamp,
        "location": location,
        "status": status,
        "temperature": temperature
    }


# ✅ Convert Format 2
def convertFromFormat2(data):
    # Timestamp → milliseconds
    timestamp_value = data.get("timestamp")

    if isinstance(timestamp_value, int):
        timestamp = timestamp_value
    else:
        dt = datetime.datetime.strptime(timestamp_value, "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = int((dt - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

    # Device
    device_id = data.get("deviceId") or data.get("device", {}).get("id")
    device_type = data.get("deviceType") or data.get("device", {}).get("type")

    # Location
    if "location" in data:
        location = data["location"]
    else:
        location = {
            "country": data.get("country"),
            "city": data.get("city"),
            "area": data.get("area"),
            "factory": data.get("factory"),
            "section": data.get("section")
        }

    # Status & Temperature
    status = data.get("status") or data.get("data", {}).get("status")
    temperature = data.get("temperature") or data.get("data", {}).get("temperature")

    return {
        "deviceId": device_id,
        "deviceType": device_type,
        "timestamp": timestamp,
        "location": location,
        "status": status,
        "temperature": temperature
    }


# ✅ Main function
def main():
    with open("data-1.json", encoding="utf-8") as f1:
        data1 = json.load(f1)

    with open("data-2.json", encoding="utf-8") as f2:
        data2 = json.load(f2)

    result1 = convertFromFormat1(data1)
    result2 = convertFromFormat2(data2)

    print(result1)
    print(result2)


# ✅ Run
if __name__ == "__main__":
    main()