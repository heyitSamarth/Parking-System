from db import db


class BuildingModel(db.Model):
    __tablename__ = "buildings"
    id = db.Column(db.Integer, primary_key=True)
    building_no = db.Column(db.Integer, unique=True, nullable=False)
    floors = db.relationship("FloorModel", back_populates="building", lazy="dynamic", cascade="all, delete")
