from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)


class Banana(db.Model):
    __tablename__ = "bananas"
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String, nullable=False)
    origins = db.Column(db.String, nullable=True)


class Palm(db.Model):
    __tablename__ = "palms"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    max_banana_in_bundle = db.Column(db.Integer, nullable=False)
