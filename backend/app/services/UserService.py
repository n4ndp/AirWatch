from flask import abort
from app import db
from app.models.User import User
from app.models.Account import Account
from app.models.enums.UserRole import UserRole
from app.models.enums.AccountStatus import AccountStatus
from app.utils.PasswordUtils import hash_password


def to_user_profile(user):
    account = user.account
    return {
        "username": user.username,
        "full_name": account.full_name,
        "email": account.email,
        "role": account.role.value,
        "status": account.status.value,
        "registered_at": account.created_at.isoformat() if account.created_at else None
    }


class UserService:

    @staticmethod
    def get_user_profile(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, description="User not found")
        return to_user_profile(user)

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [to_user_profile(user) for user in users]

    @staticmethod
    def update_profile(username, data):
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, description="User not found")

        account = user.account

        email = data.get("email")
        full_name = data.get("full_name")

        if not email or not full_name:
            abort(400, description="Missing full_name or email")

        if email != account.email and Account.query.filter_by(email=email).first():
            abort(409, description="Email already in use")

        account.email = email
        account.full_name = full_name
        db.session.commit()

        return to_user_profile(user)

    @staticmethod
    def delete_user(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, description="User not found")

        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def create_user(data):
        username = data.get("username")
        password = data.get("password")
        full_name = data.get("full_name")
        email = data.get("email")
        role = data.get("role", "USER")

        if not all([username, password, full_name, email]):
            abort(400, description="Missing required fields")

        if User.query.filter_by(username=username).first():
            abort(409, description="Username already exists")

        if Account.query.filter_by(email=email).first():
            abort(409, description="Email already exists")

        try:
            role_enum = UserRole(role.upper())
        except ValueError:
            abort(400, description="Invalid role")

        user = User(
            username=username,
            password=hash_password(password)
        )

        account = Account(
            full_name=full_name,
            email=email,
            role=role_enum,
            status=AccountStatus.ACTIVE
        )

        user.account = account
        db.session.add(user)
        db.session.commit()

        return to_user_profile(user)

    @staticmethod
    def update_user_by_admin(username, data):
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, description="User not found")

        account = user.account

        email = data.get("email")
        full_name = data.get("full_name")
        role = data.get("role")

        if not all([email, full_name, role]):
            abort(400, description="Missing fields: email, full_name or role")

        if email != account.email and Account.query.filter_by(email=email).first():
            abort(409, description="Email already in use")

        try:
            role_enum = UserRole(role.upper())
        except ValueError:
            abort(400, description="Invalid role")

        account.email = email
        account.full_name = full_name
        account.role = role_enum

        db.session.commit()
        return to_user_profile(user)
