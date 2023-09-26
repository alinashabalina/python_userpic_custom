import json

import jsonschema
from flask import Flask, jsonify, request
from flask_migrate import Migrate

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
