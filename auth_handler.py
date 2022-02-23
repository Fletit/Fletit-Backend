import jwt
from decouple import config
import time
from typing import Dict

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_response(token: str, user: dict):
    return {
        "access_token": token,
        "user": user
    }

def signJWT(user_id: str, user: dict) -> dict:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token, user)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}