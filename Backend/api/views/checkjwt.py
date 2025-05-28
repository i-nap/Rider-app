import jwt
import json
from cryptography.fernet import Fernet

# Keys (MUST match your middleware)
JWT_SECRET = "7c345a2c7f9e8a24442d83090e7d327e670c86da3d21c5b16dbf53bd53716fa7"  # Same as in Django
FERNET_KEY = b"N8gyllOd3SlW5pk0AgJ7nE4XYQDC5lniL5G4sfcsyZM=" # 32-byte base64 key

fernet = Fernet(FERNET_KEY)

# --- The actual payload ---
payload = {
  "full_name": "Jane Doe",
  "email": "regmislok@gmail.com",
  "phone_number": "1234567890",
  "password_hash": "Str0ngPassw0rd!"
}


# --- Step 1: Convert to JSON then encrypt ---
json_payload = json.dumps(payload)  # ensures valid JSON string
encrypted = fernet.encrypt(json_payload.encode()).decode()  # encrypt and decode to str

# --- Step 2: Wrap in JWT ---
token = jwt.encode({'secure_data': encrypted}, JWT_SECRET, algorithm='HS256')

print(token)
