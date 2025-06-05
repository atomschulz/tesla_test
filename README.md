# Tesla Solar Charge Controller

This repository contains a simple Python script that replicates Tesla's "charge on solar" feature using Enphase solar data.

## Requirements
- Python 3.8+
- `requests` library
- Enphase Enlighten API credentials (`ENPHASE_KEY`, `ENPHASE_USER_ID`, `ENPHASE_SYSTEM_ID`)
- Tesla API access token (`TESLA_ACCESS_TOKEN`) and vehicle ID (`TESLA_VEHICLE_ID`)

## Usage
1. Install dependencies:
   ```bash
   pip install requests
   ```
2. Export the required credentials as environment variables:
   ```bash
   export ENPHASE_KEY=your_enphase_key
   export ENPHASE_USER_ID=your_user_id
   export ENPHASE_SYSTEM_ID=your_system_id
   export TESLA_ACCESS_TOKEN=your_tesla_token
   export TESLA_VEHICLE_ID=your_vehicle_id
   ```
3. Run the controller:
   ```bash
   python solar_charge_controller.py
   ```

The script polls the Enphase API every 15 minutes and adjusts the Tesla charging current so it does not exceed your solar production.
