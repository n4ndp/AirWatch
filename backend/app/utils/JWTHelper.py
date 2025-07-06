from flask_jwt_extended import create_access_token
from datetime import timedelta
import os

class JWTHelper:
    @staticmethod
    def generate_token(username, role) -> str:
        expiration = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
        return create_access_token(identity=username, additional_claims={"role": role}, expires_delta=timedelta(hours=expiration))
