from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from passlib.hash import pbkdf2_sha256
from Schemas import UserSchema,PlainUserSchema,UserUpdateSchema
from models import UserModel
from db import db
from flask_jwt_extended import create_access_token,jwt_required,get_jwt
from blocklist import BLOCKLSIT

blp =Blueprint("users","Users",__name__,description="Operations on users")



@blp.route("/register")
class UserRegister(MethodView):
    @jwt_required()
    @blp.arguments(UserSchema)
    def post(Self,user_data):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(409,message="A user with that user name already exists")
        user=UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            role=user_data["role"],
            name=user_data["name"],
            address=user_data["address"]
            ,contact=user_data["contact"]
        )
        db.session.add(user)
        db.session.commit()
        return {"message":"user created Succesfully"},201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @jwt_required()
    def delete(self, user_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
    
    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(201,UserSchema)
    def put(self,user_data,user_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        user = UserModel.query.get(user_id)
        if user:
            user.name=user_data["name"]
            user.address=user_data["address"]
            user.contact=user_data["contact"]
        else:
            abort(401,message="Enter correct user id")
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/user")
class AllUser(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        user = UserModel.query.all()
        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password) and user.role==user_data["role"]:
            access_token = create_access_token(identity=user.id,additional_claims={"is_admin":user.role=="ADMIN"})
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLSIT.add(jti)
        return {"message":"USer LOgged out"}