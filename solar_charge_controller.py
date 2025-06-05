import os
import time
import requests
from datetime import datetime, timedelta


def fetch_solar_production(start_time: datetime, api_key: str, user_id: str, system_id: str):
    """Fetch 15 minute solar production data from Enphase Enlighten API.

    This is a simplified example using the 'stats' endpoint.
    Documentation: https://developer.enphase.com/docs
    """
    url = f"https://api.enphaseenergy.com/api/v2/systems/{system_id}/stats"
    params = {
        "key": api_key,
        "user_id": user_id,
        "start_at": int(start_time.timestamp()),
        "end_at": int((start_time + timedelta(minutes=15)).timestamp()),
        "granularity": "15min",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # The API returns a list of intervals with energy_wh
    intervals = data.get("intervals", [])
    if not intervals:
        return 0
    return intervals[0].get("enwh", 0) / 1000  # convert Wh to kWh


def get_vehicle_charge_state(access_token: str, vehicle_id: str):
    """Retrieve the current charging state of the Tesla vehicle."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://owner-api.teslamotors.com/api/1/vehicles/{vehicle_id}/vehicle_data"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json().get("response", {}).get("charge_state", {})


def set_charge_limit(access_token: str, vehicle_id: str, amperage: int):
    """Set the charge current request for the Tesla."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://owner-api.teslamotors.com/api/1/vehicles/{vehicle_id}/command/set_charging_amps"
    resp = requests.post(url, headers=headers, json={"charging_amps": amperage}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    # Load credentials from environment variables
    enphase_key = os.getenv("ENPHASE_KEY")
    enphase_user_id = os.getenv("ENPHASE_USER_ID")
    enphase_system_id = os.getenv("ENPHASE_SYSTEM_ID")

    tesla_token = os.getenv("TESLA_ACCESS_TOKEN")
    tesla_vehicle_id = os.getenv("TESLA_VEHICLE_ID")

    if not all([enphase_key, enphase_user_id, enphase_system_id, tesla_token, tesla_vehicle_id]):
        raise RuntimeError("Missing required API credentials")

    now = datetime.utcnow().replace(minute=(datetime.utcnow().minute // 15) * 15, second=0, microsecond=0)
    solar_kwh = fetch_solar_production(now - timedelta(minutes=15), enphase_key, enphase_user_id, enphase_system_id)

    charge_state = get_vehicle_charge_state(tesla_token, tesla_vehicle_id)
    current_amp = charge_state.get("charge_amps", 0)
    charging = charge_state.get("charging_state") == "Charging"

    # Assume 240V to convert kW to amps
    solar_available_amp = int((solar_kwh * 1000) / 240 * 60 / 15)

    if solar_available_amp <= 0:
        if charging:
            set_charge_limit(tesla_token, tesla_vehicle_id, 0)
        return

    if solar_available_amp != current_amp:
        set_charge_limit(tesla_token, tesla_vehicle_id, solar_available_amp)


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as exc:
            print(f"Error: {exc}")
        time.sleep(900)  # wait 15 minutes
