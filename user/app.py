import json

import sqlalchemy
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from sqlalchemy import select

from models import init_app, db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "opop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/user.db'
init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def intro_page():
    return ""


@app.route("/all", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = [user.all_info() for user in all_users]
    response = {
        "message": "All app users",
        "result": result
    }

    return jsonify(response)


@app.route("/user/info/<user_id>", methods=["GET"])
def get_user(user_id):
    user_select = db.session.execute(select(User).filter_by(id=user_id))
    user = next(user_select)[0]
    response = {
        "message": "Info successfully acquired",
        "result": user.user_info()
    }

    return jsonify(response), 200


@app.route("/create", methods=["POST"])
def create_user():
    try:
        user = User()
        user.username = json.loads(request.data)["username"]
        user.email = json.loads(request.data)["email"]
        user.is_admin = json.loads(request.data)["is_admin"]
        db.session.add(user)
        db.session.commit()
        response = {"message": "User created", "result": user.user_info()}
        return jsonify(response), 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        result = db.session.execute(select(User).filter_by(email=json.loads(request.data)["email"]))
        response = {
            "message": f"This user already exists in the database with username {next(result)[0].username}",

        }
        return jsonify(response), 400


@app.route("/update/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user_select = db.session.execute(select(User).filter_by(id=user_id))
        user = next(user_select)[0]
        user.username = json.loads(request.data)["username"]
        user.email = json.loads(request.data)["email"]
        user.is_admin = json.loads(request.data)["is_admin"]
        db.session.commit()
        response = {"message": f"User successfully updated", "result": user.user_info()}
        return jsonify(response), 200
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        response = {
            "message": "User with such data probably already exists in the database",

        }
        return jsonify(response), 400


@app.route("/delete/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user_select = db.session.execute(select(User).filter_by(id=user_id))
        user = next(user_select)[0]
        db.session.delete(user)
        db.session.commit()
        response = {
            "message": f"User successfully deleted"
        }
        return jsonify(response), 200
    except:
        db.session.rollback()
        response = {
            "message": "User cannot be deleted from the database",

        }
        return jsonify(response), 400
