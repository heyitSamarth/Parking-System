from db import db
from sqlalchemy.sql import func


class BillingModel(db.Model):
    __tablename__ = "billings"
    id = db.Column(db.Integer, primary_key=True)
    booking_id=db.Column(db.Integer, db.ForeignKey("bookings.id"))
    park_in_time= db.Column(db.DateTime(timezone=True), server_default=func.now(),nullable=False)
    park_out_time= db.Column(db.DateTime(timezone=True),nullable=True)
    booking = db.relationship("BookingModel", back_populates="billing")