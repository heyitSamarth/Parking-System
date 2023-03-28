from db import db


class FloorModel(db.Model):
    __tablename__ = "floors"
    floor_id = db.Column(db.Integer, primary_key=True)
    floor_no = db.Column(db.Integer, unique=False, nullable=False)
    building_id=db.Column(db.Integer, db.ForeignKey("buildings.id"))
    floor_partitions=db.relationship("FloorPartitionModel",backref="floors",lazy="dynamic", cascade="all, delete")