class booking():
    def __init__(self,vehicle_no,vehicle_type , building , floor ,row ,column ,park_in_time):
        self.vehicle_no =vehicle_no
        self.vehicle_type =vehicle_type
        self.building =building
        self.floor =floor
        self.row =row
        self.column =column
        self.park_in_time=park_in_time
    def show_booking(self):
        print("Vehicle No          = "+ self.vehicle_no)
        print("Vehicle Type        = "+ self.vehicle_type)
        print("Building No         = "+ str(self.building))
        print("Floor No            = "+ str(self.floor))
        print("Row No              = "+ str(self.row))
        print("Column No           = "+ str(self.column))
        print("Park in time        = "+ str(self.park_in_time))
    