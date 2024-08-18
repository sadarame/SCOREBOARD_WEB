#!/usr/local/bin/python3.7
from flask_login import UserMixin

from .db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic,select_team):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.select_team = select_team

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3],select_team=user[4]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic,select_team):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic,select_team)"
            " VALUES (?, ?, ?, ?, ?)",
            (id_, name, email, profile_pic,select_team),
        )
        db.commit()
