from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import FloorSchema
from models import FloorModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("floors","Floors",__name__,description="Operations on floors")

@blp.route("/floor")
class Floor(MethodView):
    @blp.arguments(FloorSchema)
    def post(Self,floor_data):
        floornumber=FloorModel.query.filter(FloorModel.building_id==floor_data["building_id"]).count()
            
        # <- if user gives floor number ->
        # if FloorModel.query.filter(FloorModel.number==floor_data["number"] , FloorModel.building_id==floor_data["building_id"]).first():
        #     abort(409,message="A floor with same floor no already exists in Building ")
        
        floor=FloorModel(
            number=floornumber,
            building_id=floor_data["building_id"]
        )
        db.session.add(floor)
        db.session.commit()
        return {"message":"floor created Succesfully"},201

    @blp.response(200, FloorSchema(many=True))
    def get(self):
        floors = FloorModel.query.all()
        return floors
    
@blp.route("/floors/<int:building_id>")
class FloorInBuilding(MethodView):
    @blp.response(200, FloorSchema(many=True))
    def get(self,building_id):
        floors=FloorModel.query.filter(FloorModel.building_id==building_id)
        return floors
    
@blp.route("/floor/<int:floor_id>")
class FloorOperation(MethodView):
    @jwt_required()
    @blp.response(200, FloorSchema)
    def get(self, floor_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        floor = FloorModel.query.filter(FloorModel.id==floor_id).first()
        if floor :
            return floor
        else :
            abort(401,message="Plz enter correct floor id")
    
    @jwt_required()
    def delete(self, floor_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        floor = FloorModel.query.filter(FloorModel.id==floor_id).first()
        if floor :
            db.session.delete(floor)
            db.session.commit()
            return {"message": "floor deleted."}, 200
        else :
            abort(401,message="Plz enter correct floor id")