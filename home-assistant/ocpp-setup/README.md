# OCPP Integration Setup Guide for Home Assistant

Complete guide to setting up OCPP (Open Charge Point Protocol) integration with Home Assistant for your EV charger.

## What is OCPP?

OCPP is an open protocol that allows EV chargers to communicate with a central management system. With Home Assistant acting as the central system, you get:

- Real-time charging status and statistics
- Remote start/stop charging
- Adjustable charging current
- Energy consumption tracking
- Full automation capabilities

## Compatibility

### Confirmed Working Chargers
- Grizzl-E chargers with OCPP firmware
- Wallbox Pulsar Plus
- OpenEVSE
- Many other OCPP 1.6J compatible chargers

### Requirements
- Charger must support OCPP 1.6J (JSON over WebSocket)
- Charger must be on the same network as Home Assistant (or have proper port forwarding)

## Step 1: Install HACS

HACS (Home Assistant Community Store) is required to install the OCPP integration.

### If HACS is not installed:

1. Open your Home Assistant terminal or SSH
2. Run this command:
   ```bash
   wget -O - https://get.hacs.xyz | bash -
   ```
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "HACS" and complete the setup
6. Link your GitHub account when prompted

**HACS Documentation:** https://hacs.xyz/docs/setup/download

## Step 2: Install OCPP Integration

1. Open Home Assistant
2. Go to **HACS** → **Integrations**
3. Click **+ Explore & Download Repositories** (bottom right)
4. Search for **"OCPP"**
5. Click on **OCPP** by lbbrhzn
6. Click **Download**
7. **Restart Home Assistant**

**OCPP Integration Repository:** https://github.com/lbbrhzn/ocpp

## Step 3: Configure OCPP in Home Assistant

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"OCPP"**
4. Configure the Central System:

| Setting | Recommended Value | Description |
|---------|------------------|-------------|
| Host | 0.0.0.0 | Listen on all interfaces |
| Port | 9000 | Default OCPP WebSocket port |
| Path | / | WebSocket path |
| Measurands | Select all | What data to collect |
| Skip Schema Validation | Off | Keep on for strict compliance |

5. Click **Submit**

Home Assistant is now running as an OCPP Central System on port 9000.

## Step 4: Configure Your Charger

Your charger needs to connect to Home Assistant. The exact steps vary by charger brand.

### General Settings

Configure these in your charger's web interface or app:

| Setting | Value |
|---------|-------|
| OCPP Server URL | `ws://YOUR_HA_IP:9000/` |
| Charge Point ID | `charger` (or any name you choose) |
| OCPP Version | 1.6J |
| Connection Type | WebSocket (WS) |

**Replace `YOUR_HA_IP` with your Home Assistant IP address** (e.g., `ws://192.168.1.100:9000/`)

### Charger-Specific Guides

#### Grizzl-E
1. Access charger web interface (usually `http://CHARGER_IP`)
2. Go to **Settings** → **OCPP**
3. Enable OCPP
4. Enter server URL: `ws://YOUR_HA_IP:9000/`
5. Set Charge Point ID
6. Save and reboot charger

#### Wallbox
1. Open Wallbox app
2. Go to charger settings
3. Enable OCPP
4. Enter Central System URL
5. Configure authentication if required

#### OpenEVSE
1. Access OpenEVSE web interface
2. Go to **Services** → **OCPP**
3. Enable OCPP
4. Enter server URL
5. Save

**More charger guides:** https://github.com/lbbrhzn/ocpp/wiki

## Step 5: Verify Connection

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Find **OCPP** integration
3. You should see your charger listed as a device
4. Check that entities are populating:
   - `sensor.charger_status_connector`
   - `sensor.charger_power_active_import`
   - `sensor.charger_current_import`
   - `sensor.charger_voltage`
   - `switch.charger_charge_control`
   - `switch.charger_availability`

## Common Entity Names

After setup, you'll have these entities (names may vary based on your Charge Point ID):

### Sensors
| Entity | Description |
|--------|-------------|
| `sensor.charger_status_connector` | Current status (Available, Charging, etc.) |
| `sensor.charger_power_active_import` | Current power draw (kW) |
| `sensor.charger_current_import` | Current amperage (A) |
| `sensor.charger_voltage` | Line voltage (V) |
| `sensor.charger_energy_session` | Energy this session (kWh) |
| `sensor.charger_energy_active_import_register` | Lifetime energy (kWh) |

### Controls
| Entity | Description |
|--------|-------------|
| `switch.charger_charge_control` | Start/stop charging |
| `switch.charger_availability` | Enable/disable charger |
| `number.charger_maximum_current` | Set max charging amps |

## Troubleshooting

### Charger won't connect

1. **Check network connectivity**
   - Charger and HA must be on same network (or port forwarded)
   - Try pinging HA from charger network

2. **Verify URL format**
   - Must start with `ws://` (not `http://`)
   - Include port: `ws://192.168.1.100:9000/`
   - Trailing slash may be required

3. **Check firewall**
   - Ensure port 9000 is open on HA host
   - Check router firewall rules

4. **Check HA logs**
   - Go to **Settings** → **System** → **Logs**
   - Filter for "ocpp"

### Entities show "unavailable"

1. Restart the OCPP integration
2. Reboot your charger
3. Check that charger is still connected to WiFi
4. Verify OCPP settings haven't reset

### Wrong entity names

Entity names are based on your Charge Point ID. If you used "mycharger" as the ID, entities will be:
- `sensor.mycharger_status_connector`
- `sensor.mycharger_power_active_import`
- etc.

Update the dashboard and automation files to match your entity names.

## Network Diagram

```
┌─────────────────┐         ┌─────────────────┐
│   EV Charger    │         │ Home Assistant  │
│                 │         │                 │
│  OCPP Client    │◄───────►│  OCPP Server    │
│                 │   WS    │  (Port 9000)    │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
        │                           │
        │                           │
        ▼                           ▼
   ┌─────────┐               ┌─────────────┐
   │   EV    │               │  Dashboard  │
   │         │               │  Automations│
   └─────────┘               │  Tracking   │
                             └─────────────┘
```

## Next Steps

Once OCPP is working, proceed to install the VinFast dashboard and sensors:
- [Main Installation Guide](../README.md)

## Resources

- **OCPP Integration:** https://github.com/lbbrhzn/ocpp
- **OCPP Wiki:** https://github.com/lbbrhzn/ocpp/wiki
- **HACS:** https://hacs.xyz
- **OCPP Protocol Spec:** https://www.openchargealliance.org/protocols/ocpp-16/
