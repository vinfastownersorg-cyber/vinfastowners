"""Constants for the VinFast integration."""

DOMAIN = "vinfast"

# API Configuration
AUTH0_DOMAIN = "vinfast-us-prod.us.auth0.com"
AUTH0_CLIENT_ID = "xhGY7XKDFSk1Q22rxidvwujfz0EPAbUP"
AUTH0_AUDIENCE = "https://vinfast-us-prod.us.auth0.com/api/v2/"
API_BASE = "https://mobile.connected-car.vinfastauto.us"

# Config keys
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

# Options keys
CONF_OCPP_ENTITY = "ocpp_entity"
CONF_OCPP_CHARGING_STATE = "ocpp_charging_state"

# Update intervals (seconds)
UPDATE_INTERVAL_NORMAL = 14400  # 4 hours when idle
UPDATE_INTERVAL_CHARGING = 300  # 5 minutes when charging via OCPP

# Legacy - for backward compatibility
UPDATE_INTERVAL = UPDATE_INTERVAL_NORMAL

# Default OCPP charger entity to monitor for charging state
DEFAULT_OCPP_CHARGER_ENTITY = "sensor.charger_status_connector"
DEFAULT_OCPP_CHARGING_STATE = "Charging"

# Legacy - for backward compatibility
OCPP_CHARGER_STATUS_ENTITY = DEFAULT_OCPP_CHARGER_ENTITY
OCPP_CHARGING_STATE = DEFAULT_OCPP_CHARGING_STATE

# Sensor types
SENSOR_ODOMETER = "odometer"
SENSOR_BATTERY = "battery"
SENSOR_CHARGING = "charging"
SENSOR_RANGE = "range"
