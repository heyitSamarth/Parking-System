from db import db


class SlotsModel(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    slot_no = db.Column(db.Integer, unique=True, nullable=False)
    slot_reserved=db.Column(db.Boolean,unique=False,nullable=False)
    slot_type=db.Column(db.String(3),nullable=False)
    bookings = db.relationship("BookingModel", back_populates="slot", lazy="dynamic", cascade="all, delete")