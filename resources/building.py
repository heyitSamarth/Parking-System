from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import BuildingSchema
from models import BuildingModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("buildings","Buildings",__name__,description="Operations on buildings")

@blp.route("/building")
class Building(MethodView):
    @jwt_required()
    @blp.arguments(BuildingSchema)
    def post(Self,building_data):
        if BuildingModel.query.filter(BuildingModel.number==building_data["number"]).first():
            abort(409,message="A building with same building no already exists")
        building=BuildingModel(
            number=building_data["number"]
        )
        db.session.add(building)
        db.session.commit()
        return {"message":"building created Succesfully"},201
    @jwt_required()
    @blp.response(200, BuildingSchema(many=True))
    def get(self):
        building = BuildingModel.query.all()
        return building

@blp.route("/building/<int:building_id>")
class BuildingOperation(MethodView):
    @jwt_required()
    @blp.response(200, BuildingSchema)
    def get(self, building_id):
        building = BuildingModel.query.filter(BuildingModel.id==building_id).first()
        if building :
            return building
        else :
            abort(400,message="Plz enter correct Building id")
    
    @jwt_required()
    def delete(self, building_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(403,message="admin privilege required ")
        building = BuildingModel.query.filter(BuildingModel.id==building_id).first()
        if building :
            db.session.delete(building)
            db.session.commit()
            return {"message": "building deleted."}, 204
        else :
            abort(400,message="Plz enter correct building number")

