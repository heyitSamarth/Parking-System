from db import db


class FloorPartitionModel(db.Model):
    __tablename__ = "floor_partitions"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    floor_id=db.Column(db.Integer, db.ForeignKey("floors.id"))
    floor=db.relationship("FloorModel",back_populates="floor_partitions")
    slots=db.relationship("SlotModel",back_populates="floor_partition",lazy="dynamic", cascade="all, delete")