from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), nullable=False)
    contact=db.Column(db.Integer, nullable=False)
    address=db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role=db.Column(db.String(10),nullable=False)

    bookings = db.relationship("BookingModel", back_populates="user",)
    billings = db.relationship("BillingModel", back_populates="user",)
    