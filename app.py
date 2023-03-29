import os
from datetime import timedelta
from flask import Flask,jsonify
from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLSIT
import models


# from resources.item import blp as ItemBlueprint
# from resources.store import blp as StoreBlueprint
from resources.vehicle import blp as VehicleBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Parking System"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parkingsystemdata.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = '82362600056799238578762281734654593836'#<- signing key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload['jti'] in BLOCKLSIT

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message":"LOGIN AGAIN","description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message":"LOGIN AGAIN","description": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message":"LOGIN AGAIN","description": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(VehicleBlueprint)
    return app

# api.register_blueprint(ItemBlueprint)
# api.register_blueprint(StoreBlueprint)
# api.register_blueprint(TagBlueprint)
# api.register_blueprint(UserBlueprint)
