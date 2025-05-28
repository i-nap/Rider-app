import jwt
from cryptography.fernet import Fernet
import json
# Keys (MUST match your middleware)
JWT_SECRET = "7c345a2c7f9e8a24442d83090e7d327e670c86da3d21c5b16dbf53bd53716fa7"  # Same as in Django
FERNET_KEY = b"N8gyllOd3SlW5pk0AgJ7nE4XYQDC5lniL5G4sfcsyZM=" # 32-byte base64 key

fernet = Fernet(FERNET_KEY)

# === Simulated response token from Django ===
response = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZWN1cmVfZGF0YSI6ImdBQUFBQUJvTm1fU1lySVJDMmNERW1Qd1N0WmZ6TEZ5Mk1DRThBVjRzMTI0LWh5ZVBjeUVERlZ1VUZFeXdJLS1NemZ5cno5eEhsYjBycFVEcWVzTmVkdG1CM2tyVkJjc29ocXBYUDJZTlk3ZVQyenRaN0cxQ3FaNjh2b0VIR2lDTVp5dkd0OVhiUHBjIn0.k300Ne3TDeUsUj6L_az0VeXSarHS4d9A8ZX96X6eJGg"
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
