from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import BuildingSchema
from models import BuildingModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("buildings","Buildings",__name__,description="Operations on users")

@blp.route("/building")
class building(MethodView):
    @blp.arguments(BuildingSchema)
    def post(Self,vehicle_data):
        if BuildingModel.query.filter(BuildingModel.vehicle_number==vehicle_data["vehicle_number"]).first():
            abort(409,message="A vehicle with same vehicle number already exists")
        vehicle=VehicleModel(
            vehicle_number=vehicle_data["vehicle_number"],
            vehicle_type=vehicle_data["vehicle_type"],
            vehicle_owner=vehicle_data["vehicle_owner"],
            vehicle_colour = vehicle_data["vehicle_colour"],
            vehicle_description=vehicle_data["vehicle_description"]
        )
        db.session.add(vehicle)
        db.session.commit()
        return {"message":"vehicle created Succesfully"},201

    @blp.response(200, VehicleSchema(many=True))
    def get(self):
        vehicle = VehicleModel.query.all()
        return vehicle