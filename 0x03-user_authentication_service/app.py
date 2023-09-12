#!/usr/bin/env python3
"""
Flask App
"""
from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """ welcome function
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """ register a user
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """ Change the password
        args:
            email: Expected
        return
            200 if it exist otherwise 403
    """
    try:
        email = request.form['email']
        reset_tok = request.form["reset_token"]
        new_pwd = request.form['new_password']
    except KeyError:
        abort(403)

    try:
        AUTH.update_password(reset_tok, new_pwd)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    """ Get profile with session id
        args:
            email: Expected
        return
            200 if it exist otherwise 403
    """
    try:
        email = request.form['email']
    except KeyError:
        abort(403)

    token: str = ''
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token}), 200


@ app.route('/profile', methods=['GET'])
def profile() -> str:
    """ Get profile with session id
        args:
            session_id: Session identificator
        return
            Email 200 otherwise 403 status
    """
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@ app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ Logout session
        args:
            session_id
        return
            redirect main or 403 error
    """
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/', code=302)


@ app.route('/sessions', methods=['POST'])
def login() -> str:
    """ Sessions Login User """
    try:
        email = request.form['email']
        pwd = request.form['password']
    except KeyError:
        abort(401)

    if (AUTH.valid_login(email, pwd)):
        session_id = AUTH.create_session(email)
        if session_id is not None:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response

    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
