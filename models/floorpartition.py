from db import db


class FloorPartitionModel(db.Model):
    __tablename__ = "floor_partitions"
    id = db.Column(db.Integer, primary_key=True)
    floor_partition_no = db.Column(db.Integer, unique=True, nullable=False)
    floor_id=db.Column(db.Integer, db.ForeignKey("floors.id"))
    slots=db.relationship("SlotModel",backref="floor_partitions",lazy="dynamic", cascade="all, delete")