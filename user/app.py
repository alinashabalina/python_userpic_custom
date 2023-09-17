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
migrate = Migrate(app, db, render_as_batch=True)


@app.route("/")
def intro_page():
    return "hello world"


@app.route("/user/<username>")
def private(username):
    return f"This is your private area, {username}"


@app.route("/all", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = [user.all_info() for user in all_users]
    response = {
        "message": "All app users",
        "result": result
    }

    return jsonify(response)


@app.route("/create", methods=["POST"])
def create_user():
    try:
        user = User()
        user.username = json.loads(request.data)["username"]
        user.email = json.loads(request.data)["email"]
        user.is_admin = json.loads(request.data)["is_admin"]
        db.session.add(user)
        db.session.commit()
        response = {"message": "User created", "result": user.created()}
        return jsonify(response), 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        result = db.session.execute(select(User).filter_by(email=json.loads(request.data)["email"]))
        response = {
            "Message": f"This user already exists in the database with username {next(result)[0].username}",

        }
        return jsonify(response), 400
