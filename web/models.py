from flask_login import UserMixin
from sqlalchemy import func

from exts import db


# orm模型
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    power = db.Column(db.Integer, nullable=False)

    create_time = db.Column(db.DateTime, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Capture(db.Model):
    __tablename__ = "capture"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(255), nullable=False)
    pic_type = db.Column(db.String(50), nullable=False)

    create_time = db.Column(db.DateTime, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


# TODO ================================= 口罩 ==========================================================
class Mask(db.Model):
    __tablename__ = "mask"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mask = db.Column(db.Integer, nullable=False)
    no_mask = db.Column(db.Integer, nullable=False)

    create_time = db.Column(db.DateTime, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


# TODO ================================= 人流量 ==========================================================
class PassersBy (db.Model):
    __tablename__ = "passers_by"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    down_count = db.Column(db.Integer, nullable=False)
    up_count = db.Column(db.Integer, nullable=False)

    create_time = db.Column(db.DateTime, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
