from db import db

class SlotModel(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    slot_no = db.Column(db.Integer, unique=True, nullable=False)
    slot_reserved=db.Column(db.Boolean,unique=False,nullable=False)
    slot_type=db.Column(db.String(3),nullable=False)
    floor_partition_id=db.Column(db.Integer, db.ForeignKey("floor_partitions.id"))
    floor_partition=db.relationship("FloorPartitionModel",back_populates="slots")
    bookings = db.relationship("BookingModel", back_populates="slot", lazy="dynamic", cascade="all, delete")