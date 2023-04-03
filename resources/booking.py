from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from Schemas import AddBookingSchema,BookingUpdateSchema,ShowBookingSchema
from models import BookingModel,VehicleModel,SlotModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt


blp =Blueprint("bookings","Bookings",__name__,description="Operations on Bookings")


@blp.route("/booking")
class Booking(MethodView):
    @jwt_required()
    @blp.arguments(AddBookingSchema)
    def post(Self,booking_data):
        # for validation of vehicle and slot
        vehicle=VehicleModel.query.filter(VehicleModel.number==booking_data["vehicle_number"]).first()
        slot=SlotModel.query.filter(SlotModel.id==booking_data["slot_id"]).first()
        if not vehicle:
            abort(401,message="Plz enter correct Vehicle number or Register vehicle ")
        if vehicle.is_parked:
            abort(401,message="Vehicle is already parked ")
        if not slot:
            abort(401,message="Plz Select correct slot ")
        if slot.reserved:
            abort(401,message="Plz Select Empty slot ")
        if vehicle.type!=slot.type:
            abort(401,message="Plz Select Valid slot ")


        logged_in_user_id=get_jwt().get("sub")
        booking=BookingModel(
            vehicle_id = vehicle.id,
            slot_id=booking_data["slot_id"],
            user_id=logged_in_user_id
        )
        db.session.add(booking)
        db.session.commit()
        vehicle.is_parked=True
        slot.reserved=True
        db.session.commit()
        return {"message":"booking created Succesfully"},201

    @blp.response(200, ShowBookingSchema(many=True))
    def get(self):
        bookings = BookingModel.query.all()
        return bookings


@blp.route("/booking/<booking_id>")
class BookingOperation(MethodView):
    @blp.response(200, ShowBookingSchema)
    def get(self, booking_id):
        booking = BookingModel.query.filter(BookingModel.id==booking_id).first()
        if booking :
            return booking
        else :
            abort(401,message="Plz enter correct booking id")
    
    @jwt_required()
    def delete(self, booking_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        booking = BookingModel.query.filter(BookingModel.id==booking_id).first()
        if booking :
            db.session.delete(booking)
            db.session.commit()
            return {"message": "booking deleted."}, 200
        else :
            abort(401,message="Plz enter correct booking id")

    @jwt_required()
    @blp.arguments(BookingUpdateSchema)
    @blp.response(201,ShowBookingSchema)
    def put(self,booking_data,booking_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="admin privilege required ")
        booking = BookingModel.query.filter(BookingModel.id==booking_id).first()
        slot=SlotModel.query.filter(SlotModel.id==booking_data["slot_id"]).first()
        if not slot:
            abort(401,message="Plz Select correct slot ")
        if slot.reserved:
            abort(401,message="Plz Select Empty slot ")        
        if booking:
            booking.slot_id=booking_data["slot_id"]
        else:
            abort(401,message="Enter correct booking id")
        db.session.add(booking)
        db.session.commit()
        return booking
        