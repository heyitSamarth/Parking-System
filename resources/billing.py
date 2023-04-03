from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import BillingSchema
from models import BillingModel,BookingModel,VehicleModel,SlotModel
from db import db
from datetime import datetime
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("billings","Billings",__name__,description="Operations on Billings")


@blp.route("/billing")
class Billing(MethodView):
    @jwt_required()
    @blp.arguments(BillingSchema)
    def post(Self,billing_data):
        logged_in_user_id=get_jwt().get("sub")
        booking = BookingModel.query.filter(BookingModel.id==billing_data["booking_id"]).first()
        if booking:
            billing=BillingModel(
                booking_id=billing_data["booking_id"],
                parking_amount=billing_data["parking_amount"],
                user_id=logged_in_user_id
            )
            db.session.add(billing)
            vehicle_id=booking.vehicle_id
            slot_id=booking.slot_id
            vehicle=VehicleModel.query.filter(VehicleModel.id==vehicle_id).first()
            slot=SlotModel.query.filter(SlotModel.id==slot_id).first()
            vehicle.is_parked=False
            slot.reserved=False
            booking.park_out_time=datetime.now()
            db.session.commit()

            return {"message":"billing created Succesfully"},201
        else:
            abort(401,message="Plz enter correct booking id")

    @blp.response(200, BillingSchema(many=True))
    def get(self):
        billings = BillingModel.query.all()
        return billings


@blp.route("/billing/<billing_id>")
class BillingOperation(MethodView):
    @blp.response(200, BillingSchema)
    def get(self, billing_id):
        billing = BillingModel.query.filter(BillingModel.id==billing_id).first()
        if billing :
            return billing
        else :
            abort(401,message="Plz enter correct billing id")
    
    @jwt_required()
    def delete(self, billing_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        billing = BillingModel.query.filter(BillingModel.id==billing_id).first()
        if billing :
            db.session.delete(billing)
            db.session.commit()
            return {"message": "billing deleted."}, 200
        else :
            abort(401,message="Plz enter correct billing id")

    # <- Update Billing ->
    # @jwt_required()
    # @blp.arguments(BillingUpdateSchema)
    # @blp.response(201,BillingSchema)
    # def put(self,billing_data,billing_id):
    #     jwt=get_jwt()
    #     if not jwt.get("is_admin"):
    #         abort(401,message="admin privilege required ")
    #     billing = BillingModel.query.filter(BillingModel.id==billing_id).first()
    #     if billing:
    #         billing.slot_id=billing_data["slot_id"]
    #     else:
    #         abort(401,message="Enter correct billing id")
    #     db.session.add(billing)
    #     db.session.commit()
    #     return billing
        