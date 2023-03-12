
from tqdm.auto import tqdm
import colorama
from colorama import Back, Style
from pickle import load,dump

colorama.init(autoreset=True)

# from ParkingSpace import parkingSpace
class user():
    def __init__(self):
        pass

class employee(user):
    def __init__(self,E_name,E_contact,E_id,E_password):
        self.E_name=E_name
        self.E_contact=E_contact
        self.E_id=E_id
        self.E_password=E_password

    def employee_detail(self):
        print("Employee Name       = "+ self.E_name)
        print("Employee Contact    = "+ self.E_contact)
        print("Employee ID         = "+ self.E_id)
        print("Employee Password   = "+ self.E_password)
    
    def unpark_vehicle(self,parking_spaces,vehicles,bookings,do_billing):
        print(Back.YELLOW + "Enter Vehicle no of Vehicle u want to Unpark")
        V_no=input("-> ")
        V_no=V_no.upper()
        booking_object=""
        for booking in bookings:
            if(booking.vehicle_no==V_no):
                booking_object=booking

        if(booking_object==""):
            print(Back.RED + "Enter Correct Vehicle no  ")
            return
        building_no=booking_object.building
        floor_no=booking_object.floor
        row=booking_object.row
        column=booking_object.column
        print(Back.GREEN + f"Your vehicle is Located at Floor no {floor_no} of Buildin no {building_no} at Red location ( row {row} and column {column})")
        parking_spaces[0].view_slots(building_no,floor_no,row,column)
        print(Back.YELLOW +"Calculating Vechile Charges ")

        charges=do_billing(V_no)

        print(Back.GREEN +f"Charges for vehicle no {V_no} are {charges}$")
        input("Press Enter if payment Recived")
        parking_spaces[0].parking_space[building_no][floor_no][row][column]=0
        for vehicle_object in vehicles:
            if(vehicle_object.vehicle_no==V_no):
                vehicle_object.unpark_vehicle()
        i=0
        for booking in bookings:
            i=i+1
            if(booking.vehicle_no==V_no):
                break
            
        bookings.pop(i-1)
        print(Back.GREEN +"Vechile unparked ")
        print(Back.BLUE +"Thankyou for Visiting")


    def check_empty_space(self,parking_spaces):
        building_no=""
        floor_no=""
        row_no=""
        column_no=""
        for  building in range(len(parking_spaces[0].parking_space)):
            for floor in range(len(parking_spaces[0].parking_space[building])):
                for row in range(len(parking_spaces[0].parking_space[building][floor])):
                    for column in range(len(parking_spaces[0].parking_space[building][floor][row])):
                        if(parking_spaces[0].parking_space[building][floor][row][column]==0):
                            return(building,floor,row,column)
    
    def random_park_vehicle(self,parking_spaces,vehicles,do_booking,add_vehicle):

        (building_no,floor_no,row_no,column_no)=self.check_empty_space(parking_spaces)
        print(Back.GREEN +f"Vechile parked at floor {floor_no} of Building {building_no} ")                  
        parking_spaces[0].view_slots(building_no,floor_no,row_no,column_no)
        V_no=  input("Please Enter Vehicle no            -> ")
        V_no=V_no.upper()
        vehicle_data_present=False
        vehicle_object=""
        for vehicle in vehicles:
            if(vehicle.vehicle_no==V_no):
                vehicle_data_present=True
                vehicle_object=vehicle

        if(vehicle_data_present==False):
            print(Back.CYAN + "+------------------------+")
            print(Back.CYAN + "|  1- Car (LMV)          |")
            print(Back.CYAN + "|  2- Truck (HMV)        |")
            print(Back.CYAN + "|  3- Bike (MC)          |")
            print(Back.CYAN + "+------------------------+")
            V_type_option=0
            while (V_type_option!='1' and  V_type_option!='2' and V_type_option!='3'):
                V_type_option=input("Please Select Vehicle type         -> ")
            if(V_type_option=='1'):
                V_type="LMV"
            if(V_type_option=='2'):
                V_type="HMV"
            if(V_type_option=='3'):
                V_type="MC"
            V_owner=str(input("Please Enter Vehicle owner         -> "))
            V_colour=   input("Please enter Vehicle colour        -> ")
            V_brand=    input("Please enter Vehicle brand         -> ")
            print(Back.YELLOW + "Please Verify the Information")
            print("Vehicle no       = "+ V_no)
            print("Vehicle type     = "+ V_type)
            print("Vehicle owner    = "+ V_owner)
            print("Vehicle colour   = "+ V_colour)
            print("Vehicle brand    = "+ V_brand)
            input("Press Enter to continue or CTRL+C to Break Operation")
            vehicle_object=add_vehicle(V_no,V_type,V_owner,V_colour,V_brand)
            print(Back.GREEN + "Vehicle information stored")
        
        if(vehicle_data_present==True):
            if(vehicle_object.vehicle_parked=="P"):
                print(Back.RED + "Vehicle Already Parked ")
                return
            print(Back.GREEN + "Vehicle information already stored")
            V_no=vehicle_object.vehicle_no
            V_type=vehicle_object.vehicle_type
        booking=do_booking(V_no,V_type,building_no,floor_no,row_no,column_no)
        booking.show_booking()
        parking_spaces[0].parking_space[building_no][floor_no][row_no][column_no]=1	     
        vehicle_object.park_vehicle()

    def park_vehicle(self,parking_spaces,vehicles,do_booking,add_vehicle):
        (building_no,floor_no)=parking_spaces[0].display_parking()
        print(Back.YELLOW +  '   Please Enter row you want to select    : ')
        row = int(input("-> "))
        print(Back.YELLOW +  '   Please Enter column you want to select : ')
        column = int(input("-> "))
        if(parking_spaces[0].parking_space[building_no][floor_no][row][column]==1):
            print(Back.RED + "Slot already booked ")
            return
        parking_spaces[0].view_slots(building_no,floor_no,row,column)
        V_no=  input("Please Enter Vehicle no            -> ")
        V_no=V_no.upper()
        vehicle_data_present=False
        vehicle_object=""
        for vehicle in vehicles:
            if(vehicle.vehicle_no==V_no):
                vehicle_data_present=True
                vehicle_object=vehicle

        if(vehicle_data_present==False):
            print(Back.CYAN + "+------------------------+")
            print(Back.CYAN + "|  1- Car (LMV)          |")
            print(Back.CYAN + "|  2- Truck (HMV)        |")
            print(Back.CYAN + "|  3- Bike (MC)          |")
            print(Back.CYAN + "+------------------------+")
            V_type_option=0
            while (V_type_option!='1' and  V_type_option!='2' and V_type_option!='3'):
                V_type_option=input("Please Select Vehicle type         -> ")
            if(V_type_option=='1'):
                V_type="LMV"
            if(V_type_option=='2'):
                V_type="HMV"
            if(V_type_option=='3'):
                V_type="MC"
            V_owner=str(input("Please Enter Vehicle owner         -> "))
            V_colour=   input("Please enter Vehicle colour        -> ")
            V_brand=    input("Please enter Vehicle brand         -> ")
            print(Back.YELLOW + "Please Verify the Information")
            print("Vehicle no       = "+ V_no)
            print("Vehicle type     = "+ V_type)
            print("Vehicle owner    = "+ V_owner)
            print("Vehicle colour   = "+ V_colour)
            print("Vehicle brand    = "+ V_brand)
            input("Press Enter to continue or CTRL+C to Break Operation")
            vehicle_object=add_vehicle(V_no,V_type,V_owner,V_colour,V_brand)
            print(Back.GREEN + "Vehicle information stored")
        
        if(vehicle_data_present==True):
            if(vehicle_object.vehicle_parked=="P"):
                print(Back.RED + "Vehicle Already Parked ")
                return
            print(Back.GREEN + "Vehicle information already stored")
            V_no=vehicle_object.vehicle_no
            V_type=vehicle_object.vehicle_type
        booking=do_booking(V_no,V_type,building_no,floor_no,row,column)
        booking.show_booking()
        parking_spaces[0].parking_space[building_no][floor_no][row][column]=1	     
        vehicle_object.park_vehicle()


class admin(user):
    def __init__(self):
        self.employees=[]
        self.password="aka"

    def create_employee(self):
        E_name=str(input("Please Enter Employee Name         -> "))
        E_contact= input("Please enter Employee Contact No   -> ")
        E_id=str(input  ("Please Enter Employee Id           -> "))
        E_password=input("Please enter Employee password     -> ")
        print(Back.YELLOW + "Please Verify the Information")
        employee_object=employee(E_name,E_contact,E_id,E_password)
        employee_object.employee_detail()
        input("Press Enter to continue or CTRL+C to Break Operation")
        self.employees.append(employee_object)
        print(Back.GREEN + "Employee information stored")

    def change_parking_space(self,parking_object):
        # parking_object=ParkingSpace()
        print(Back.CYAN + "+------------------------------+")
        print(Back.CYAN + "|  1- Change Parking Space     |")
        print(Back.CYAN + "+------------------------------+")
        user_input = input("-> ")
        if user_input == '1':
            print(Back.CYAN + "+------------------------------+")
            print(Back.CYAN + "|  1- Add Building             |")
            print(Back.CYAN + "|  2- Add floor in building    |")
            print(Back.CYAN + "|  3- Add Slot in building     |")
            print(Back.CYAN + "|  4- Previous Menu            |")
            print(Back.CYAN + "+------------------------------+")
            user_input2 = input("-> ")
            if user_input2 == '1':
                parking_object.parking_space.append([[]])
                parking_object.view_buildings()
            elif user_input2 == '2':
                parking_object.view_buildings()
                print(Back.YELLOW +  '   Please Enter Building no :   ')
                user_input3 = int(input("-> "))
                parking_object.parking_space[user_input3].append([])
                parking_object.view_floors(user_input3)
            elif user_input2 == '3':
                (building_no,floor_no)=parking_object.display_parking()	
                print(Back.YELLOW +  '   Please Enter no of rows :    ')
                no_of_rows = int(input("-> "))
                print(Back.YELLOW +  '   Please Enter no of columns : ')
                no_of_columns = int(input("-> "))
                existing_slot=len(parking_object.parking_space[building_no][floor_no])
                for i in range( no_of_rows):
                    parking_object.parking_space[building_no][floor_no].append([])
                    for j in range(no_of_columns):
                        parking_object.parking_space[building_no][floor_no][i+existing_slot].append(0)
                parking_object.view_slots(building_no,floor_no)
            elif user_input2 == '4':
                self.change_parking_space(parking_object)
            else :
                print(Back.RED+"    Please enter valid input    ")
                self.change_parking_space(parking_object)