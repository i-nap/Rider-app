import jwt
import json
from cryptography.fernet import Fernet

# Keys (MUST match your middleware)
JWT_SECRET = '0123456789abcdef0123456789abcdef'  # Same as in Django
FERNET_KEY = b'bxZ7E9QAm4GbKvJDD1yMX8rhZCT0uRBAqff_U7jKb1I='  # 32-byte base64 key

fernet = Fernet(FERNET_KEY)

# --- The actual payload ---
payload = {
    "user_id": 5,
    "group_id": 12
}

# --- Step 1: Convert to JSON then encrypt ---
json_payload = json.dumps(payload)  # ensures valid JSON string
encrypted = fernet.encrypt(json_payload.encode()).decode()  # encrypt and decode to str

# --- Step 2: Wrap in JWT ---
token = jwt.encode({'secure_data': encrypted}, JWT_SECRET, algorithm='HS256')

print(token)
