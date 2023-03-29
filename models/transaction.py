from db import db


class TransactionModel(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    billing_id=db.Column(db.Integer, db.ForeignKey("billings.id"))
    billing = db.relationship("BillingModel", back_populates="transaction")

    amount_paid=db.Column(db.Integer, nullable=False)
    payment_status=db.Column(db.String(10), nullable=False)
