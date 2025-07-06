from app import db

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.UniqueConstraint("username", name="uk_users_username"),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    account = db.relationship("Account", back_populates="user", uselist=False, cascade="all, delete-orphan")
