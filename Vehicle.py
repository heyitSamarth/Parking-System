class vehicle():
    def __init__(self,vehicle_no,vehicle_type,vehicle_owner,vehicle_colour,vehicle_brand):
        self.vehicle_no=vehicle_no
        self.vehicle_type=vehicle_type
        self.vehicle_owner=vehicle_owner
        self.vehicle_colour=vehicle_colour
        self.vehicle_brand=vehicle_brand
        self.vehicle_parked="UP"
    def park_vehicle(self):
        self.vehicle_parked="P"
    def unpark_vehicle(self):
        self.vehicle_parked="UP"
