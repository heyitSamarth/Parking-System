from db import db


class VehicleModel(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(80), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(3), nullable=False)
    vehicle_owner = db.Column(db.String(80), nullable=False)
    vehicle_colour = db.Column(db.String(80),  nullable=False)
    vehicle_description = db.Column(db.String(80), nullable=False)
    vehicle_status=db.Column(db.Boolean,nullable=False)
    bookings = db.relationship("BookingModel", back_populates="vehicle", lazy="dynamic", cascade="all, delete")
    