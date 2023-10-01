import json

import jsonschema
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from sqlalchemy import select

from models import init_app, db, Group
from schemas import ValidationSchemas

app = Flask(__name__)

app.config['SECRET_KEY'] = "opop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/groups.db'
init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def intro_page():
    return ""


@app.route("/group/create", methods=["POST"])
def create_group():
    try:
        group = Group()
        jsonschema.validate(instance=json.loads(request.data), schema=ValidationSchemas.GroupCreateSchema)
        group.user_id = json.loads(request.data)["user_id"]
        group.group_name = json.loads(request.data)["group_name"]
        group.userpic_link = json.loads(request.data)["userpic_link"]
        group.is_default = json.loads(request.data)["is_default"]
        group.is_private = json.loads(request.data)["is_private"]
        db.session.add(group)
        db.session.commit()
        response = {"message": "Group created", "result": group.group_info()}
        return jsonify(response), 201
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


@app.route("/group/update/<group_id>", methods=["PUT"])
def update_group(group_id):
    try:
        group_select = db.session.execute(select(Group).filter_by(id=group_id))
        group = next(group_select)[0]
        jsonschema.validate(instance=json.loads(request.data), schema=ValidationSchemas.GroupCreateSchema)
        group.user_id = json.loads(request.data)["user_id"]
        group.group_name = json.loads(request.data)["group_name"]
        group.userpic_link = json.loads(request.data)["userpic_link"]
        group.is_default = json.loads(request.data)["is_default"]
        group.is_private = json.loads(request.data)["is_private"]
        db.session.add(group)
        db.session.commit()
        response = {"message": "Group updated", "result": group.group_info()}
        return jsonify(response), 200
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


@app.route("/group/delete/<group_id>", methods=["DELETE"])
def delete_user(group_id):
    try:
        group_select = db.session.execute(select(Group).filter_by(id=group_id))
        group = next(group_select)[0]
        db.session.delete(group)
        db.session.commit()
        response = {
            "message": "Group successfully deleted"
        }
        return jsonify(response), 200
    except StopIteration:
        db.session.rollback()
        response = {
            "message": "Group does not exist in the database"
        }
        return jsonify(response), 400

