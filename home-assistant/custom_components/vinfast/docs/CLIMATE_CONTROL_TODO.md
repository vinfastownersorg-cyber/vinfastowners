# VinFast Climate Control - Future Implementation

## Current Status
Climate control requires cryptographic signing that needs device-paired keys.
This is not yet implemented in the integration.

## How to Extract Keys (Option A - iOS Backup)

1. Create an **unencrypted** iTunes backup of your iPhone
2. Use a tool like `iBackup Viewer` or `iMazing` to browse the backup
3. Find the VinFast app container (look for `com.vinfast.companion`)
4. Locate the SQLite database with remote control data
5. Extract:
   - `privateKey` - RSA private key in PEM format
   - `sharedKey` - Base64 encoded HMAC key

## Command Signing Algorithm

```python
import hashlib
import hmac
import base64
import time
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sign_command(private_key_pem, shared_key_b64, user_id, message_content, session_id):
    timestamp = str(int(time.time() * 1000))
    message_b64 = base64.b64encode(json.dumps(message_content).encode()).decode()

    # signature = SHA256withRSA(privateKey, timestamp_bytes + message_b64_bytes)
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
    data_to_sign = timestamp.encode() + message_b64.encode()
    signature = private_key.sign(data_to_sign, padding.PKCS1v15(), hashes.SHA256())
    signature_b64 = base64.b64encode(signature).decode()

    # signature2 = base64(HMAC-SHA256(sharedKey, timestamp_bytes + message_b64_bytes))
    shared_key = base64.b64decode(shared_key_b64)
    hmac_data = timestamp.encode() + message_b64.encode()
    signature2 = base64.b64encode(hmac.new(shared_key, hmac_data, hashlib.sha256).digest()).decode()

    # user_id = base64(SHA256(userid_bytes))
    user_id_hash = base64.b64encode(hashlib.sha256(user_id.encode()).digest()).decode()

    return {
        "message_name": "CLIMATE_CONTROL_AIR_CONDITION_ENABLE",
        "message_content": message_b64,
        "sess_id": session_id,
        "timestamp": timestamp,
        "signature": signature_b64,
        "tag": None,
        "user_id": user_id_hash,
        "isMasterProfile": True,
        "signature2": signature2,
        "wakeUpTimeOut": 60000
    }
```

## Message Content Format

```json
{
  "deviceKey": "3416_0_5850",
  "value": 1
}
```

Where `deviceKey` format is `objectId_instanceId_resourceId` from LwM2M.

## API Endpoint

```
POST https://ccarapi.vinfast.com/ccaraccessmgmt/api/v2/remote/app/command
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Known Climate Control Aliases

| Control | Alias | Resource Path |
|---------|-------|---------------|
| AC Enable | CLIMATE_CONTROL_AIR_CONDITION_ENABLE | 3416/0/5850 |
| Target Temp | CLIMATE_CONTROL_TARGET_TEMPERATURE | TBD |

## Pairing Flow (If Re-pairing Needed)

VinFast requires QR code + OTP two-factor verification:

1. Car displays QR code containing: `K=<key>&ssid=<session>&vin=<VIN>&timeout=<sec>&profileId=<b64_userid>`
2. App validates VIN matches user's vehicle
3. App generates RSA 2048-bit keypair and CSR
4. `POST /verify-session` with session ID - triggers OTP to phone/email
5. `POST /send-pair-data` with OTP + encrypted CSR
6. Server returns encrypted certificate + shared key
7. Keys stored locally for future command signing
