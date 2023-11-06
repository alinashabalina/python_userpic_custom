from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=False)
    email = db.Column(db.String(255), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(256))
    token = db.Column(db.String(256))
    token_issue_time = db.Column(db.Time)

    def user_info(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def all_info(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "password": self.password
        }

    def login_info(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "password": self.password,
            "token": self.token,
            "token_issue_time": self.token_issue_time.strftime("%H:%M:%S")
        }
