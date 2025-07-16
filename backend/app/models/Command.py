from app import db

class Command(db.Model):
    __tablename__ = "commands"

    id = db.Column(db.Integer, primary_key=True)
    command_text = db.Column(db.String(255), nullable=False)
    action_taken = db.Column(db.String(255), nullable=True)
