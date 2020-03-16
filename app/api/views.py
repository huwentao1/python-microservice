from flask import Blueprint, jsonify, request, render_template

from app.api.models import User
from app import db

users_blueprint = Blueprint("users", __name__, template_folder="./templates")


@users_blueprint.route("/ping", methods=["GET"])
def ping_ping():
    return jsonify({"message": "pong", "status": "success"})


@users_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        userinfo = request.get_json()
        user = User(userinfo.get("username"), userinfo.get("email"))
        db.session.add(user)
        return (
            {"status": "success", "message": "%s was add."
                                             % userinfo.get("email")},
            200,
        )
    users = User.query.all()
    return render_template("index.html", users=users)


@users_blueprint.route("/users", methods=["POST"])
def add_user():
    """添加用户"""
    userinfo = request.get_json()
    if not userinfo:
        return {"status": "fail", "message": "data is not null."}, 400
    username = userinfo.get("username")
    if not username:
        return {"status": "fail", "message": "Username can not null."}, 400
    email = userinfo.get("email")
    if not email:
        return {"status": "fail", "message": "Email can not null."}, 400
    user = User.query.filter_by(email=email).all()
    if user:
        return {"status": "fail",
                "message": "Sorry. That email already exists."}, 400
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return {"status": "success", "message": "%s was add." % user.email}, 200


@users_blueprint.route("/users/<id>", methods=["GET"])
def get_user(id):
    """查询用户"""
    user = User.query.filter_by(id=id).one_or_none()

    if user:
        return (
            {
                "status": "success",
                "message": {"username": user.username, "email": user.email},
            },
            200,
        )
    return {"status": "fail", "message": "%s id not exists." % id}, 400


@users_blueprint.route("/users", methods=["GET"])
def get_all_users():
    user = User.query.all()
    data = []
    for item in user:
        data.append(
            {
                "username": item.username,
                "id": item.id,
                "email": item.email,
                "created_at": item.created_at,
            }
        )
    return {"status": "success", "user": data}, 200
