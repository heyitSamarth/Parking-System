from db import db


class BookingModel(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id=db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    slot_id=db.Column(db.Integer, db.ForeignKey("slots.id"))
    vehicle=db.relationship("VehicleModel", back_populates="bookings")
    slot=db.relationship("SlotModel", back_populates="bookings")
    billing = db.relationship("BillingModel", back_populates="booking", lazy="dynamic", cascade="all, delete")
