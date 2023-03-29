from db import db

from sqlalchemy.sql import func

class BookingModel(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id=db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    slot_id=db.Column(db.Integer, db.ForeignKey("slots.id"))
    vehicle=db.relationship("VehicleModel", back_populates="bookings")
    slot=db.relationship("SlotModel", back_populates="bookings")

    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    user=db.relationship("UserModel", back_populates="bookings")

    park_in_time= db.Column(db.DateTime(timezone=True), server_default=func.now(),nullable=False)
    park_out_time= db.Column(db.DateTime(timezone=True),nullable=True)

    billing = db.relationship("BillingModel", back_populates="booking", lazy="dynamic", cascade="all, delete")
