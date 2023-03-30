from db import db


class VehicleModel(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(3), nullable=False)
    owner = db.Column(db.String(80), nullable=False)
    colour = db.Column(db.String(80),  nullable=False)
    description = db.Column(db.String(80), nullable=False)
    is_parked=db.Column(db.Boolean,nullable=False,default=False)
    bookings = db.relationship("BookingModel", back_populates="vehicle", lazy="dynamic", cascade="all, delete")
    