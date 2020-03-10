from flask import Blueprint, jsonify, request

from app.api.models import User
from app import db

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/ping", methods=["GET"])
def ping_ping():
    return jsonify({"message": "pong", "status": "success"})


@users_blueprint.route("/users", methods=["POST"])
def add_user():
    """添加用户"""
    userinfo = request.get_json()
    user = User(username=userinfo.get("username"), email=userinfo.get("email"))
    db.session.add(user)
    db.session.commit()
    return {"status": "success", "message": "%s was add." % user.email}, 200
