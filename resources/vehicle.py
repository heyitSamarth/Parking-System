from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import VehicleSchema,VehicleUpdateSchema
from models import VehicleModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("vehicles","Vehicles",__name__,description="Operations on Vehicles")


@blp.route("/vehicle")
class Vehicle(MethodView):
    @blp.arguments(VehicleSchema)
    def post(Self,vehicle_data):
        if VehicleModel.query.filter(VehicleModel.number==vehicle_data["number"]).first():
            abort(409,message="A vehicle with same vehicle number already exists")
        vehicle=VehicleModel(
            number=vehicle_data["number"],
            type=vehicle_data["type"],
            owner=vehicle_data["owner"],
            colour = vehicle_data["colour"],
            description=vehicle_data["description"]
        )
        db.session.add(vehicle)
        db.session.commit()
        return {"message":"vehicle created Succesfully"},201

    @blp.response(200, VehicleSchema(many=True))
    def get(self):
        vehicle = VehicleModel.query.all()
        return vehicle


@blp.route("/vehicle/<vehicle_number>")
class VehicleOperation(MethodView):
    @blp.response(200, VehicleSchema)
    def get(self, vehicle_number):
        vehicle = VehicleModel.query.filter(VehicleModel.number==vehicle_number).first()
        if vehicle :
            return vehicle
        else :
            abort(401,message="Plz enter correct vehicle number")
    
    @jwt_required()
    def delete(self, vehicle_number):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        vehicle = VehicleModel.query.filter(VehicleModel.number==vehicle_number).first()
        if vehicle :
            db.session.delete(vehicle)
            db.session.commit()
            return {"message": "vehicle deleted."}, 200
        else :
            abort(401,message="Plz enter correct vehicle number")

    @jwt_required()
    @blp.arguments(VehicleUpdateSchema)
    @blp.response(201,VehicleSchema)
    def put(self,vehicle_data,vehicle_number):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        vehicle = VehicleModel.query.filter(VehicleModel.number==vehicle_number).first()
        if vehicle:
            vehicle.owner=vehicle_data["owner"]
            vehicle.colour = vehicle_data["colour"]
            vehicle.description=vehicle_data["description"]
        else:
            abort(401,message="Enter correct vehicle number")
        db.session.add(vehicle)
        db.session.commit()
        return vehicle
        


# <-  FOR SERACHING VEHICLE BY VEHICLE ID ->
# @blp.route("/vehicle/<int:vehicle_id>")
# class vehicle(MethodView):
#     @blp.response(200, VehicleSchema)
#     def get(self, vehicle_id):
#         vehicle = VehicleModel.query.get_or_404(vehicle_id)
#         return vehicle
    
#     @jwt_required()
#     def delete(self, vehicle_id):
#         jwt=get_jwt()
#         if not jwt.get("is_admin"):
#             abort(401,message="admin privilege required ")
#         vehicle = VehicleModel.query.get_or_404(vehicle_id)
#         db.session.delete(vehicle)
#         db.session.commit()
#         return {"message": "vehicle deleted."}, 200

#     @jwt_required()
#     @blp.arguments(VehicleUpdateSchema)
#     @blp.response(201,VehicleSchema)
#     def put(self,vehicle_data,vehicle_id):
#         jwt=get_jwt()
#         if not jwt.get("is_admin"):
#             abort(401,message="admin privilege required ")
#         vehicle = VehicleModel.query.get(vehicle_id)
#         if vehicle:
#             vehicle.vehicle_owner=vehicle_data["vehicle_owner"],
#             vehicle.vehicle_colour = vehicle_data["vehicle_colour"],
#             vehicle.vehicle_description=vehicle_data["vehicle_description"]
#         else:
#             abort(401,message="Enter correct vehicle id")
#         db.session.add(vehicle)
#         db.session.commit()
#         return vehicle

