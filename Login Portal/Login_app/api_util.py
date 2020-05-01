from datetime import datetime
from Login_app.models import User
from flask import json
from Login_app import db
from Login_app.schema import schema_for_post, schema_for_put
import jsonschema


def check_json_post(data_received):
    try:
        jsonschema.validate(data_received, schema_for_post)
    except jsonschema.exceptions.ValidationError as e:
        return False
    except json.decoder.JSONDecodeError as e:
        return False

    if len(data_received["username"]) == 0 or len(data_received["password"]) == 0 or len(data_received["email"]) == 0 or \
            len(data_received) > 3:
        return False

    return True


def check_json_put(data_received):
    try:
        jsonschema.validate(data_received, schema_for_put)
    except jsonschema.exceptions.ValidationError as e:
        return False
    except json.decoder.JSONDecodeError as e:
        return False

    if len(data_received["username"]) == 0 or len(data_received["password"]) == 0 or len(data_received) > 2:
        return False

    return True


def check_credentials_post(username, password, email):
    try:
        user_obj = User.query.filter_by(username=username).first()
        if user_obj:
            return 208

        user_obj = User(username=username, password=password, email=email)
        db.session.add(user_obj)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return 503

    return 202


def check_credentials_put(username, password):
    try:
        user = User.query.filter_by(username=username).first()

        if not user:
            return "401_user_not_found"

        password_temp = user.password

        if password != password_temp:
            return "401_password_not_matching"

        dt = datetime.now()
        user.last_login_timestamp = dt
        db.session.commit()

    except Exception as e:
        return 503

    return 202
