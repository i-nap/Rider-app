import json
import jwt
from django.http import JsonResponse, HttpRequest
from cryptography.fernet import Fernet, InvalidToken
import os
from dotenv import load_dotenv



load_dotenv()

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

FERNET_KEY = os.environ.get('FERNET_SECRET') 
fernet = Fernet(FERNET_KEY)


class JWTEncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # === STEP 1: Decrypt incoming token ===
        if request.method == 'POST':
            try:
                raw_data = json.loads(request.body)
                token = raw_data.get('token')
                if not token:
                    return JsonResponse({'error': 'Missing JWT token in request body'}, status=400)

                # Decode JWT to get encrypted payload
                jwt_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                encrypted_data = jwt_payload.get('secure_data')

                # Decrypt the payload using Fernet
                decrypted_json = fernet.decrypt(encrypted_data.encode()).decode()
                request.decrypted_data = json.loads(decrypted_json)
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, InvalidToken) as e:
                return JsonResponse({'error': 'Invalid token', 'details': str(e)}, status=401)
            except Exception as e:
                return JsonResponse({'error': 'Decryption failed', 'details': str(e)}, status=400)
        else:
            request.decrypted_data = {}

        # === Call the view ===
        response = self.get_response(request)

        # === STEP 2: Encrypt outgoing response ===
        try:
            if hasattr(response, 'data'):
                # Serialize and encrypt the response data
                json_data = json.dumps(response.data)
                encrypted_data = fernet.encrypt(json_data.encode()).decode()

                # Wrap encrypted data inside JWT
                jwt_token = jwt.encode({'secure_data': encrypted_data}, JWT_SECRET, algorithm=JWT_ALGORITHM)
                return JsonResponse({'token': jwt_token})
        except Exception as e:
            return JsonResponse({'error': 'Response encryption failed', 'details': str(e)}, status=500)

        return response
