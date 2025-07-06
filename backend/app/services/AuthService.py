from app import db
from app.models.User import User
from app.models.Account import Account
from app.models.enums.UserRole import UserRole
from app.models.enums.AccountStatus import AccountStatus
from app.utils.PasswordUtils import hash_password, check_password
from app.utils.JWTHelper import JWTHelper
from flask import abort
from sqlalchemy.exc import SQLAlchemyError

class AuthService:
    
    @staticmethod
    def register(request_data):
        username = request_data.get("username", "").strip()
        password = request_data.get("password", "").strip()
        full_name = request_data.get("full_name", "").strip()
        email = request_data.get("email", "").strip()

        if not all([username, password, full_name, email]):
            abort(400, description="All fields (username, password, full_name, email) are required")

        if User.query.filter_by(username=username).first():
            abort(409, description="Username already exists")

        if Account.query.filter_by(email=email).first():
            abort(409, description="Email already exists")

        try:
            hashed = hash_password(password)
            user = User(username=username, password=hashed)

            account = Account(
                full_name=full_name,
                email=email,
                role=UserRole.USER,
                status=AccountStatus.ACTIVE
            )

            user.account = account

            db.session.add(user)
            db.session.commit()

            token = JWTHelper.generate_token(username, account.role.value)

            return {
                "username": username,
                "role": account.role.value,
                "token": token
            }

        except SQLAlchemyError as e:
            db.session.rollback()
            print("DB Error:", e)
            abort(500, description="Database error")
        except Exception as e:
            print("Unexpected Error:", e)
            abort(500, description="Internal server error")

    @staticmethod
    def login(request_data):
        username = request_data.get("username", "").strip()
        password = request_data.get("password", "").strip()

        if not username or not password:
            abort(400, description="Username and password are required")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password(password, user.password):
            abort(401, description="Invalid username or password")

        token = JWTHelper.generate_token(username, user.account.role.value)

        return {
            "username": username,
            "role": user.account.role.value,
            "token": token
        }
