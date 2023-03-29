from db import db


class FloorModel(db.Model):
    __tablename__ = "floors"
    id = db.Column(db.Integer, primary_key=True)
    floor_no = db.Column(db.Integer, unique=False, nullable=False)
    building_id=db.Column(db.Integer, db.ForeignKey("buildings.id"))
    building=db.relationship("BuildingModel",back_populates="floors")
    floor_partitions=db.relationship("FloorPartitionModel",back_populates="floor",lazy="dynamic", cascade="all, delete")