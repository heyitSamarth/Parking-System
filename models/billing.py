from db import db



class BillingModel(db.Model):
    __tablename__ = "billings"
    id = db.Column(db.Integer, primary_key=True)
    booking_id=db.Column(db.Integer, db.ForeignKey("bookings.id"))
    booking = db.relationship("BookingModel", back_populates="billing")
    parking_amount= db.Column(db.Integer, nullable=True)
    
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
    user=db.relationship("UserModel", back_populates="billings")

    transactions = db.relationship("TransactionModel", back_populates="billing", lazy="dynamic", cascade="all, delete")