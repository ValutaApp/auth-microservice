from datetime import timedelta
from flask import Blueprint, request
from flask.wrappers import Response
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from api.models import db, User
from api.core import create_response, serialize_list, logger
from sqlalchemy import inspect

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "<p style=\"font-size: 30px;\">Why are <span style=\"font-size: 40px; color: red;\">you</span> here?</p>"


@main.route("/currentUser", methods=["GET"])
@jwt_required
def get_persons():
    current_user = get_jwt_identity()
    currnet_claims = get_jwt_claims()
    return create_response(status=200, message={"email": current_user, "claims": currnet_claims})


@main.route("/register", methods=["POST"])
def create_person():
    data = request.get_json()

    logger.info("Data received: %s", data)
    if "name" not in data:
        msg = "No name provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "email" not in data:
        msg = "No email provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "password" not in data:
        msg = "No password provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)


    if db.session.query(User.id).filter_by(email=data["email"]).scalar() is not None:
        msg = "!!!!"
        logger.info(msg)
        return create_response(status=422, message=msg)
    new_user = User(name=data["name"], email=data["email"], password=generate_password_hash(data["password"]), isAdmin=False)

    db.session.add(new_user)
    db.session.commit()
    return create_response(
        message=f"Successfully created person {new_user.name} with id: {new_user.id}"
    )

@main.route('/login', methods=["POST"])
def login_person():
    data = request.get_json()


    logger.info("Data received: %s", data)
    if "email" not in data:
        msg = "No email provided for person/"
        logger.info(msg)
        return create_response(status=422, message=msg)
    if "password" not in data:
        msg = "No password provided for person."
        logger.info(msg)
        return create_response(status=422, message=msg)

    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(
            identity=data["email"],
            expires_delta=timedelta(minutes=30),
            user_claims={
            "user": user.name, 
            "admin": user.isAdmin 
            })
        return create_response(status=200, message={"token": access_token})

    return create_response(status=401, message="Sorry :(")