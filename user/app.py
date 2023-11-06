import json
import random
import string
from datetime import datetime
from functools import wraps

import jsonschema
import requests
import sqlalchemy
from flask import Flask, jsonify, request, redirect
from flask_migrate import Migrate
from sqlalchemy import select

from models import init_app, db, User
from schemas import ValidationSchemas

app = Flask(__name__)

GROUPS_URL = "http://127.0.0.1:5001"

app.config['SECRET_KEY'] = "opop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/user.db'
init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index_page():
    response = {"message": "This page is empty"}
    return jsonify(response), 200


@app.route("/unlogged")
def unlogged():
    response = {"message": "You should log in before you make this request"}
    return jsonify(response), 400


@app.route("/login", methods=['POST'])
def user_login():
    if 'password' in json.loads(request.data).keys() or 'email' in json.loads(request.data).keys():
        password = json.loads(request.data)['password']
        email = json.loads(request.data)['email']
        try:
            user_select = db.session.execute(select(User).filter_by(email=email))
            user = next(user_select)[0]
            if user.all_info()['password'] == password:
                message = {"message": "Successful authentication"}
                status_code = 200
                user.token = ''.join(random.choice(string.ascii_letters) for i in range(15))
                user.token_issue_time = datetime.now().time()
                db.session.commit()
            else:
                message = {"message": "A valid password or email is missing!"}
                status_code = 401
        except KeyError:
            db.session.rollback()
            response = {"message": "Make sure you are registered"}
            return jsonify(response), 400

        return jsonify(message), status_code
    else:
        return jsonify({"message": "A valid password or email is missing!"}), 401


@app.route("/admin/login", methods=['POST'])
def admin_login():
    if 'password' in json.loads(request.data).keys() or 'email' in json.loads(request.data).keys():
        password = json.loads(request.data)['password']
        email = json.loads(request.data)['email']
        user_select = db.session.execute(select(User).filter_by(email=email))
        user = next(user_select)[0]
        if user.all_info()['is_admin'] is True and user.all_info()['password'] == password:
            try:
                message = {"message": "Successful authentication"}
                status_code = 200
                user.token = ''.join(random.choice(string.ascii_letters) for i in range(15))
                user.token_issue_time = datetime.now().time()
                db.session.commit()
                return jsonify(message), status_code
            except KeyError:
                return redirect("/unlogged")
        else:
            return redirect("/unlogged")
    else:
        return jsonify({"message": "A valid password or email is missing!"}), 401


def login_check(f):
    @wraps(f)
    def decorator(**kwargs):
        kwargs.pop('user_id')
        try:
            if 'x-auth-token' in request.headers or 'email' in request.headers:
                token = request.headers['x-auth-token']
                email = request.headers['email']
                user_select = db.session.execute(select(User).filter_by(email=email))
                user = next(user_select)[0]
                if 'token' in user.login_info().keys() and user.login_info()['token'] == token:
                    kwargs['user_id'] = user.id
                    kwargs['result'] = user.login_info()
                else:
                    return redirect("/unlogged")
            else:
                return redirect("/unlogged")
        except (KeyError, StopIteration):
            return redirect("/unlogged")
        return kwargs
    return decorator


@app.route("/all", methods=["GET"])
def get_all_users():
    try:
        if "offset" in request.args.to_dict().keys() and "limit" in request.args.to_dict().keys():
            offset = request.args.get("offset")
            limit = request.args.get("limit")
        elif "offset" in request.args.to_dict().keys() and "limit" not in request.args.to_dict().keys():
            offset = request.args.get("offset")
            limit = 100
        elif "limit" in request.args.to_dict().keys() and "offset" not in request.args.to_dict().keys():
            offset = 0
            limit = request.args.get("limit")
        else:
            offset = 0
            limit = 1000
        if int(limit) >= 0 and int(offset) >= 0:
            all_users = User.query.limit(int(limit)).offset(int(offset)).all()
            result = [user.all_info() for user in all_users]
            response = {"message": "All app users", "result": result}
            return jsonify(response), 200
        else:
            response = {"message": "Enter the correct limit/offset number"}
            return jsonify(response), 400
    except ValueError:
        response = {"message": "Limit/offset can only be a number"}
        return jsonify(response), 400


@app.route("/user/info/<user_id>", methods=["GET"])
@login_check
def get_user(**kwargs):
    try:
        user_select = db.session.execute(select(User).filter_by(id=user_id))
        user = next(user_select)[0]
        response = {
            "message": "Info successfully acquired",
            "result": kwargs["result"]
        }

        return jsonify(response), 200
    except StopIteration:
        response = {
            "message": "Oops something went wrong",
        }

        return jsonify(response), 400


@app.route("/create", methods=["POST"])
def create_user():
    try:
        user = User()
        jsonschema.validate(instance=json.loads(request.data), schema=ValidationSchemas.UserCreateSchema)
        user.is_admin = json.loads(request.data)["is_admin"]
        user.email = json.loads(request.data)["email"]
        user.password = json.loads(request.data)["password"]
        if "username" not in json.loads(request.data).keys():
            user.username = ""
        else:
            user.username = json.loads(request.data)["username"]
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
    except KeyError as e:
        db.session.rollback()
        if len(e.args) != 0:
            response = {
                "message": f"Make sure you have filled the {e.args[0]} field",

            }
        else:
            response = {
                "message": "Oops something went wrong. Check that all the fields are filled",

            }
        return jsonify(response), 400
    except jsonschema.exceptions.SchemaError as e:
        db.session.rollback()
        response = {
            "message": f"Check that all the fields are filled {e.json_path}",

        }
        return jsonify(response), 400
    except jsonschema.exceptions.ValidationError as e:
        db.session.rollback()
        response = {
            "message": f"Validation error: {e.message}",

        }
        return jsonify(response), 400


@app.route("/update/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user_select = db.session.execute(select(User).filter_by(id=user_id))
        user = next(user_select)[0]
        jsonschema.validate(instance=json.loads(request.data), schema=ValidationSchemas.UserCreateSchema)
        user.email = json.loads(request.data)["email"]
        user.is_admin = json.loads(request.data)["is_admin"]
        if "username" not in json.loads(request.data).keys():
            user.username = ""
        else:
            user.username = json.loads(request.data)["username"]
        db.session.commit()
        response = {"message": f"User successfully updated", "result": user.user_info()}
        return jsonify(response), 200
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        response = {
            "message": "User with such data probably already exists in the database",

        }
        return jsonify(response), 400
    except jsonschema.exceptions.ValidationError as e:
        db.session.rollback()
        response = {
            "message": f"Validation error: {e.message}",

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
            "message": "User successfully deleted"
        }
        return jsonify(response), 200
    except StopIteration:
        db.session.rollback()
        response = {
            "message": "User does not exist in the database"
        }
        return jsonify(response), 400


@app.route("/user/create/group", methods=["POST"])
def create_group():
    r = requests.post(GROUPS_URL + "/group/create", json=json.loads(request.data))
    if r.status_code == 201:
        response = {
            "message": "Group successfully added",
            "result": r.json()["result"]
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Group is not added"
        }
        return jsonify(response), 400
