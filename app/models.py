from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))
    access_token = db.Column(db.String(200))
    refresh_token = db.Column(db.String(200))
