# VinFast Home Assistant Integration

Home Assistant configurations for VinFast EV owners, including vehicle telemetry, OCPP charger monitoring, cost tracking, and gas savings calculations.

## Features

### VinFast Connected Car Integration
- **Battery & Range** - Real-time SOC and estimated range
- **Odometer** - Track miles driven for accurate cost calculations
- **Doors & Windows** - Individual door status (FL, FR, RL, RR)
- **Trunk & Hood** - Opening status
- **Tire Pressure** - All four tires
- **Climate** - Inside and outside temperatures
- **Location** - GPS tracking with map display
- **Charging Status** - Charging state, time to full, charge limit
- **Lock Status** - Vehicle lock state

### OCPP Charger Dashboard
- **Real-Time Monitoring** - Power, current, voltage gauges
- **Cost Tracking** - Session, daily, weekly, monthly costs
- **Odometer-Based Calculations** - Actual $/mile from real driving data
- **Efficiency Tracking** - Wh/mi for battery degradation analysis
- **Gas Savings Calculator** - Compare EV vs gas costs

## Requirements

- Home Assistant (2024.1 or newer recommended)
- VinFast account (for vehicle integration)
- OCPP Integration (for charger features)
- Mushroom Cards (optional, for enhanced UI)

## VinFast Connected Car Setup

### Quick Install

1. Copy `custom_components/vinfast/` to your Home Assistant `custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings** → **Devices & Services** → **Add Integration**
4. Search for "VinFast" and enter your account credentials

### Available Sensors

| Sensor | Description |
|--------|-------------|
| Battery | State of charge (%) |
| Range | Estimated range (miles) |
| Odometer | Current mileage |
| Charging | Charging state |
| Time to Full | Minutes until charged |
| Charge Limit | Target SOC (%) |
| Doors (FL/FR/RL/RR) | Individual door open/closed |
| Trunk | Trunk open/closed |
| Hood | Hood open/closed |
| Windows | Window status |
| Tire Pressure (FL/FR/RL/RR) | PSI for each tire |
| Outside Temp | Ambient temperature |
| Inside Temp | Cabin temperature |
| Lock Status | Vehicle locked/unlocked |
| Plug Status | Charger plugged in |
| Speed | Current speed |
| Location | GPS coordinates |

## OCPP Integration Setup

Before using the cost tracking configurations, install the OCPP integration:

**[Complete OCPP Setup Guide](ocpp-setup/README.md)**

**Quick Links:**
- [OCPP Integration Repository](https://github.com/lbbrhzn/ocpp)
- [OCPP Wiki (charger-specific guides)](https://github.com/lbbrhzn/ocpp/wiki)
- [HACS Installation](https://hacs.xyz/docs/setup/download)

## Installation

### 1. Add Configuration

Copy the contents of `configuration/ocpp_sensors.yaml` to your `configuration.yaml`, or use include:

```yaml
# In configuration.yaml
template: !include configuration/ocpp_sensors.yaml
```

**Important:** Update entity names to match your setup:
- `sensor.your_vehicle_name_odometer` → `sensor.YOUR_VEHICLE_NAME_odometer`
- `sensor.charger_*` → your OCPP charger entity names

### 2. Add Automations

Copy files from `automations/` to your Home Assistant automations folder.

### 3. Import Dashboard

1. Go to **Settings** → **Dashboards**
2. Click **Add Dashboard** → **New dashboard from scratch**
3. Click the three dots → **Edit Dashboard** → **Raw configuration editor**
4. Paste contents of `dashboards/vinfast_dashboard.yaml`
5. Save

### 4. Customize Settings

Edit these values in `configuration/ocpp_sensors.yaml`:

| Setting | Default | Description |
|---------|---------|-------------|
| `electricity_rate` | 0.14601 | Your $/kWh rate |
| `gas_price_per_gallon` | 3.25 | Current gas price |
| `comparable_vehicle_mpg` | 25 | Gas car comparison MPG |
| `ev_efficiency_mi_per_kwh` | 3.5 | Your VF8/VF9 efficiency |

## File Structure

```
├── README.md
├── custom_components/
│   └── vinfast/               # VinFast Connected Car integration
│       ├── __init__.py
│       ├── api.py             # VinFast API client
│       ├── config_flow.py     # Setup wizard
│       ├── coordinator.py     # Data coordinator
│       ├── sensor.py          # Sensor entities
│       ├── binary_sensor.py   # Binary sensors (doors, etc.)
│       ├── device_tracker.py  # Location tracking
│       └── manifest.json
├── ocpp-setup/
│   └── README.md              # OCPP setup guide
├── configuration/
│   └── ocpp_sensors.yaml      # Cost tracking & gas savings
├── automations/
│   ├── ocpp_auto_start.yaml   # Auto-start charging
│   └── ocpp_tts.yaml          # Voice announcements
└── dashboards/
    └── vinfast_dashboard.yaml # Lovelace dashboard
```

## Dashboard Features

### Vehicle View
- Battery gauge with range and odometer
- Status row: Lock, Charging, Plug, Power
- Individual door status (FL, FR, RL, RR)
- Trunk, Hood, Windows status
- Tire pressure for all four corners
- Climate (inside/outside temp, speed)
- Live map with vehicle location
- Vehicle info (Model, Year, Color)

### Charging View
- Battery status with charging indicators
- OCPP charger controls (start/stop, availability, max current)
- Power, current, voltage gauges
- Session energy and cost
- Period tracking (Today/7 Days/31 Days)
- Historical graphs
- Cost metrics ($/kWh, $/mile, $/100 miles)
- Gas savings comparison

## Adjustable Settings

After installation, adjust these from the dashboard:

| Setting | Entity | Description |
|---------|--------|-------------|
| Gas Price | `input_number.gas_price_per_gallon` | Current gas price |
| Vehicle MPG | `input_number.comparable_vehicle_mpg` | Gas car comparison |
| EV Efficiency | `input_number.ev_efficiency_mi_per_kwh` | Your VinFast mi/kWh |

## Cost Calculations

The integration provides both **estimated** and **actual** cost calculations:

- **Estimated**: Based on energy charged × efficiency
- **Actual**: Based on real odometer data when available

Actual calculations become available after driving and will show:
- Real $/mile from your driving
- Actual Wh/mile for battery degradation tracking
- True efficiency compared to estimated

## Troubleshooting

### Sensors show "unavailable"
- Ensure VinFast integration is configured with valid credentials
- Check that entity IDs match your setup
- Verify OCPP integration is connected

### Cost calculations show 0 or wrong values
- Wait for statistics to accumulate (24-48 hours)
- Verify `sensor.charger_energy_active_import_register` is reporting
- Check that odometer entity name matches your vehicle

### Dashboard not updating
- Clear browser cache (Cmd+Shift+R)
- Restart Home Assistant
- Check logs for errors

## Contributing

Pull requests welcome! Please test your changes before submitting.

## License

GPL-3.0 License

## Credits

Created by the VinFast Owners community.
