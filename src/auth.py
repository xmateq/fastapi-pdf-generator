from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from passlib.context import CryptContext
import jwt

from datetime import datetime, timedelta

from src.config import Settings

SETTINGS = Settings()

class AuthHandler:
    SECURITY = HTTPBearer()
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = SETTINGS.SECRET_KEY

    def verify_password(self, plain, hashed):
        return self.PWD_CONTEXT.verify(plain, hashed)
    
    def encode_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=15),
            "iat": datetime.utcnow(),
            "sub": username
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(SECURITY)):
        return self.decode_token(auth.credentials)
