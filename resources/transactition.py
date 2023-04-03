from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import TransactitionSchema
from models import TransactitionModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("transactitions","Transactitions",__name__,description="Operations on Transactitions")


@blp.route("/transactition")
class Transactition(MethodView):
    @jwt_required()
    @blp.arguments(TransactitionSchema)
    def post(Self,transactition_data):
        # for validation of vehicle and slot 
        logged_in_user_id=get_jwt().get("sub")
        transactition=TransactitionModel(
            billing_id=transactition_data["billing_id"],
            amount_paid=transactition_data["parking_amount"],
            payment_status=transactition_data["payment_status"]
        )
        db.session.add(transactition)
        db.session.commit()
        return {"message":"transactition created Succesfully"},201

    @blp.response(200, TransactitionSchema(many=True))
    def get(self):
        transactitions = TransactitionModel.query.all()
        return transactitions


@blp.route("/transactition/<transactition_id>")
class TransactitionOperation(MethodView):
    @blp.response(200, TransactitionSchema)
    def get(self, transactition_id):
        transactition = TransactitionModel.query.filter(TransactitionModel.id==transactition_id).first()
        if transactition :
            return transactition
        else :
            abort(401,message="Plz enter correct transactition id")
    
    @jwt_required()
    def delete(self, transactition_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        transactition = TransactitionModel.query.filter(TransactitionModel.id==transactition_id).first()
        if transactition :
            db.session.delete(transactition)
            db.session.commit()
            return {"message": "transactition deleted."}, 200
        else :
            abort(401,message="Plz enter correct transactition id")

    # <- Update Transactition ->
    # @jwt_required()
    # @blp.arguments(TransactitionUpdateSchema)
    # @blp.response(201,TransactitionSchema)
    # def put(self,transactition_data,transactition_id):
    #     jwt=get_jwt()
    #     if not jwt.get("is_admin"):
    #         abort(401,message="admin privilege required ")
    #     transactition = TransactitionModel.query.filter(TransactitionModel.id==transactition_id).first()
    #     if transactition:
    #         transactition.slot_id=transactition_data["slot_id"]
    #     else:
    #         abort(401,message="Enter correct transactition id")
    #     db.session.add(transactition)
    #     db.session.commit()
    #     return transactition
        