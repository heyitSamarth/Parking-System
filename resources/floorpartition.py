from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import FloorPartitionSchema
from models import FloorPartitionModel,FloorModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("floorpartitions","FloorPartitions",__name__,description="Operations on floorpartition")

@blp.route("/floorpartition")
class FloorPartition(MethodView):
    @jwt_required()
    @blp.arguments(FloorPartitionSchema)
    def post(Self,floorpartition_data):
        if FloorModel.query.filter(FloorModel.id==floorpartition_data["floor_id"]).first():
            floorpartitionnumber=FloorPartitionModel.query.filter(FloorPartitionModel.floor_id==floorpartition_data["floor_id"]).count()+1
        
            # <- if user give floor partion number ->
            # if FloorPartitionModel.query.filter(FloorPartitionModel.number==floorpartition_data["number"] , FloorPartitionModel.floor_id==floorpartition_data["floor_id"]).first():
            #     abort(409,message="A floorpartition with same floorpartion number already exists in floor ")

            floorpartition=FloorPartitionModel(
                number=floorpartitionnumber,
                floor_id=floorpartition_data["floor_id"]
            )
            db.session.add(floorpartition)
            db.session.commit()
            return {"message":"floorpartition created Succesfully"},201
        else:
            abort(400,message="Plz enter correct floor id")
    @jwt_required()
    @blp.response(200, FloorPartitionSchema(many=True))
    def get(self):
        floorpartitions = FloorPartitionModel.query.all()
        return floorpartitions
    
@blp.route("/floorpartitions/<int:floor_id>")
class FloorPartitionInFloor(MethodView):
    @jwt_required()
    @blp.response(200, FloorPartitionSchema(many=True))
    def get(self,floor_id):
        floorpartitions=FloorPartitionModel.query.filter(FloorPartitionModel.floor_id==floor_id).all()
        if floorpartitions:
            return floorpartitions
        else:
            abort(400,message="Plz enter correct floor id")
    
@blp.route("/floorpartition/<int:floorpartition_id>")
class FloorPartitionOperations(MethodView):
    @jwt_required()
    @blp.response(200, FloorPartitionSchema)
    def get(self, floorpartition_id):
        floorpartition = FloorPartitionModel.query.filter(FloorPartitionModel.id==floorpartition_id).first()
        if floorpartition :
            return floorpartition
        else :
            abort(400,message="Plz enter correct floorpartition id")
    
    @jwt_required()
    def delete(self, floorpartition_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(403,message="admin privilege required ")
        floorpartition = FloorPartitionModel.query.filter(FloorPartitionModel.id==floorpartition_id).first()
        if floorpartition :
            db.session.delete(floorpartition)
            db.session.commit()
            return {"message": "floorpartition deleted."}, 204
        else :
            abort(400,message="Plz enter correct floorpartition id")