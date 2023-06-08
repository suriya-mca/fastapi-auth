from decouple import config

import time
import jwt
from typing import Dict


JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")


def token_response(token: str, type: str):

    if type == "login":
        return token
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str, type: str) -> Dict[str, str]:

    try:

        # jwt payload
        if type == "password_change":
            payload = {
                "user_id": user_id,
                "expires": time.time() + 300
            }
        elif type == "login":
            payload = {
                "user_id": user_id,
                "expires": time.time() + 3600
            }
        else:
            payload = {
                "user_id": user_id,
                "expires": time.time() + 600
            }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token_response(token, type)
    except Exception as e:
        print(e)

# function used to decode the JWT string
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)