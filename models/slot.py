from db import db

class SlotModel(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    reserved=db.Column(db.Boolean,unique=False,nullable=False,default=False)
    type=db.Column(db.String(3),nullable=False)
    floor_partition_id=db.Column(db.Integer, db.ForeignKey("floor_partitions.id"))
    floor_partition=db.relationship("FloorPartitionModel",back_populates="slots")
    bookings = db.relationship("BookingModel", back_populates="slot", lazy="dynamic", cascade="all, delete")