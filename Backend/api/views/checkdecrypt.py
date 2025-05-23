import jwt
from cryptography.fernet import Fernet
import json

# === Keys used ===
JWT_SECRET = '0123456789abcdef0123456789abcdef'  # Same as in Django middleware
FERNET_KEY = b'bxZ7E9QAm4GbKvJDD1yMX8rhZCT0uRBAqff_U7jKb1I='  # Same base64 key used in Django

fernet = Fernet(FERNET_KEY)

# === Simulated response token from Django ===
response = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZWN1cmVfZGF0YSI6ImdBQUFBQUJvTHBmaWd5SUlOaFJUc04tWjJfdjZmWGtTVjNHaTVRU1l1SDdYWTM1aGQ5dC1pMVRKT2dmRE1BSVNOaktHM2UwWlJ4WjJyNVVhc19kZkUwbXlxQ0tGaXBPNHdVN0pJTDVIUHp1VkZLQjBzS1RTRmVKd1lLeE9yZ1NENDZUV0VMaklCY0dxIn0.3AFggT1uEzPeVehD74G7gkSOKYgNWHnCgIJ0XcNQTAo"
}

# === Step 1: Decode JWT and extract encrypted payload ===
try:
    jwt_payload = jwt.decode(response["token"], JWT_SECRET, algorithms=["HS256"])
    encrypted_data = jwt_payload.get("secure_data")

    if not encrypted_data:
        raise ValueError("secure_data not found in token payload")

    # === Step 2: Decrypt the payload using Fernet ===
    decrypted_json = fernet.decrypt(encrypted_data.encode()).decode()
    final_data = json.loads(decrypted_json)

    print("✅ Decrypted response data:")
    print(json.dumps(final_data, indent=2))

except Exception as e:
    print("❌ Error while decoding/decrypting:", str(e))
