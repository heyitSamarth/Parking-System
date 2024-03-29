from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import SlotSchema
from models import SlotModel,FloorPartitionModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("slot","Slot",__name__,description="Operations on slots")

@blp.route("/slot")
class SlotPartition(MethodView):
    @jwt_required()
    @blp.arguments(SlotSchema)
    def post(Self,slot_data):
        if FloorPartitionModel.query.filter(FloorPartitionModel.id==slot_data["floor_partition_id"]).first():
            slotnumber=SlotModel.query.filter(SlotModel.floor_partition_id==slot_data["floor_partition_id"]).count()+1
        
            # <- if user give floor partion number ->
            # if SlotModel.query.filter(SlotModel.number==floorpartition_data["number"] , SlotModel.floor_id==floorpartition_data["floor_id"]).first():
            #     abort(409,message="A slot with same floorpartion number already exists in floor ")

            slot=SlotModel(
                number=slotnumber,
                floor_partition_id=slot_data["floor_partition_id"],
                type=slot_data["type"]
            )
            db.session.add(slot)
            db.session.commit()
            return {"message":"slot created Succesfully"},201
        else:
            abort(400,message="Plz enter correct floor partition id")
    @jwt_required()
    @blp.response(200, SlotSchema(many=True))
    def get(self):
        slots = SlotModel.query.all()
        return slots
    
@blp.route("/slots/<int:floor_partition_id>")
class SlotInFloorpartition(MethodView):
    @jwt_required()
    @blp.response(200, SlotSchema(many=True))
    def get(self,floor_partition_id):
        slots=SlotModel.query.filter(SlotModel.floor_partition_id==floor_partition_id).all()
        if slots:
            return slots
        else:
            abort(400,message="Plz enter correct floor partition id")
@blp.route("/slot/<int:slot_id>")
class SlotOperations(MethodView):
    @jwt_required()
    @blp.response(200, SlotSchema)
    def get(self, slot_id):
        slot = SlotModel.query.filter(SlotModel.id==slot_id).first()
        if slot :
            return slot
        else :
            abort(400,message="Plz enter correct slot id")
    
    @jwt_required()
    def delete(self, slot_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(403,message="admin privilege required ")
        slot = SlotModel.query.filter(SlotModel.id==slot_id).first()
        if slot :
            db.session.delete(slot)
            db.session.commit()
            return {"message": "slot deleted."}, 204
        else :
            abort(400,message="Plz enter correct slot id")