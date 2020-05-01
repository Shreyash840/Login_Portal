from Login_app import app, db
from flask import request, jsonify
from Login_app import api_util
import http


################################################################################
@app.route('/register/', methods=['POST'])
def post():
    db.create_all()
    data_received = request.get_json()
    if api_util.check_json_post(data_received) is False:
        return jsonify(status="Bad Entries"), http.HTTPStatus.BAD_REQUEST
    else:
        username = (data_received["username"])
        password = (data_received["password"])
        email = (data_received["email"])
        result = api_util.check_credentials_post(username, password, email)
        if result == 208:
            return jsonify(status="Already Exists"), http.HTTPStatus.ALREADY_REPORTED
        elif result == 503:
            return jsonify(status="Database Error"), http.HTTPStatus.SERVICE_UNAVAILABLE
        elif result == 202:
            return jsonify(status="Added New User"), http.HTTPStatus.ACCEPTED
################################################################################


@app.route('/login/', methods=['PUT'])
def valid():
    data_received = request.get_json()
    if api_util.check_json_put(data_received) is False:
        return jsonify(status="Bad Entries"), http.HTTPStatus.BAD_REQUEST
    else:
        username = (data_received["username"])
        password = (data_received["password"])
        result = api_util.check_credentials_put(username, password)
        if result == "401_user_not_found":
            return jsonify(status="User does not exist"), http.HTTPStatus.UNAUTHORIZED
        elif result == "401_password_not_matching":
            return jsonify(status="Password does not match"), http.HTTPStatus.UNAUTHORIZED
        elif result == 503:
            return jsonify(status="Database Error"), http.HTTPStatus.SERVICE_UNAVAILABLE
        elif result == 202:
            return jsonify(status="Login successful"), http.HTTPStatus.ACCEPTED
    ################################################################################

