import os

from fastapi import Header, HTTPException
from dotenv import load_dotenv


load_dotenv()


def validate_token(authorization: str = Header(...)):
    token = os.getenv("TOKEN")
    if authorization != f"Bearer {token}":
        raise HTTPException(status_code=401, detail="Token no válido")
    return True
