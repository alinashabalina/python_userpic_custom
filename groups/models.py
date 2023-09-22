from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    group_name = db.Column(db.String(255))
    userpic_link = db.Column(db.String)

    def group_info(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "group_name": self.group_name,
            "userpic_link": self.userpic_link
        }


class GroupUsers(db.Model):
    group_id = db.Column(db.Integer, ForeignKey("group.id"), primary_key=True)
    user_id = db.Column(db.Integer)

    def group_user_info(self):
        return {
            "group_id": self.group_id,
            "user_id": self.user_id
        }