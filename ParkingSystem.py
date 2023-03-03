import datetime
import getpass
import warnings
import sqlite3
from tqdm.auto import tqdm
import colorama
from colorama import Back, Style
from pickle import load,dump
warnings.filterwarnings("ignore")
colorama.init(autoreset=True)

from ParkingSpace import parkingSpace
from Vehicle import vehicle
from User import admin
from Booking import booking

class parkingSystem:
    def __init__(self):
        self.parking_spaces = []
        self.vehicles = []
        self.bookings=[]
        self.billings=[]
        self.add_parking_space()
        self.admin_object=admin()

    def add_parking_space(self):
        parking_space = parkingSpace()
        self.parking_spaces.append(parking_space)
    
    def add_vehicle(self,vehicle_no,vehicle_type,vehicle_owner,vehicle_colour,vehicle_brand):
        vehicle_object=vehicle(vehicle_no,vehicle_type,vehicle_owner,vehicle_colour,vehicle_brand)
        self.vehicles.append(vehicle_object)
        return vehicle_object

    def do_booking(self,vehicle_no,vehicle_type , building , floor ,row ,column):
        booking_object=booking(vehicle_no,vehicle_type , building , floor ,row ,column ,datetime.datetime.now())
        self.bookings.append(booking_object)
        return booking_object

    def do_billing(self,vehicle_no):
        vehicle_object=" "
        for booking in self.bookings:
            if(booking.vehicle_no==vehicle_no):
                vehicle_object=booking
        if(vehicle_object==" "):
            print(Back.RED + "Enter Correct Vehicle no  ")
            self.main_page()

        v_type=vehicle_object.vehicle_type
        park_in_time=vehicle_object.park_in_time
        duration=datetime.datetime.now()-datetime.datetime.strptime(str(park_in_time),'%Y-%m-%d %H:%M:%S.%f')
        duration=divmod(duration.total_seconds(),3600)[0]
        if(v_type=="LMV"):
            if(duration<2):
                return 30
            elif(duration<12):
                return 80
            else:
                return 150
        elif(v_type=="HMV"):
            if(duration<2):
                return 60
            elif(duration<12):
                return 140
            else:
                return 300
        elif(v_type=="MC"):
            if(duration<2):
                return 10
            elif(duration<12):
                return 30
            else:
                return 70

    def find_vehicle(self):
        print(Back.YELLOW + "Enter Vehicle no of Vehicle u want to get location of ")
        V_no=input("-> ")
        V_no=V_no.upper()
        vehicle_object=""
        for booking in self.bookings:
            if(booking.vehicle_no==V_no):
                vehicle_object=booking

        if(vehicle_object==""):
            print(Back.RED + "Enter Correct Vehicle no  ")
            return
        building_no=vehicle_object.building
        floor_no=vehicle_object.floor
        row=vehicle_object.row
        column=vehicle_object.column
        print(Back.GREEN + f"Your vehicle is Located at Floor no {floor_no} of Buildin no {building_no} at Red location ( row {row} and column {column})")
        self.parking_spaces[0].view_slots(building_no,floor_no,row,column)



    def unpark_vehicle(self):
        print(Back.YELLOW + "Enter Vehicle no of Vehicle u want to Unpark")
        V_no=input("-> ")
        V_no=V_no.upper()
        booking_object=""
        for booking in self.bookings:
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
        self.parking_spaces[0].view_slots(building_no,floor_no,row,column)
        print(Back.YELLOW +"Calculating vehicle Charges ")

        charges=self.do_billing(V_no)

        print(Back.GREEN +f"Charges for vehicle no {V_no} are {charges}$")
        input("Press Enter if payment Recived")
        self.parking_spaces[0].parking_space[building_no][floor_no][row][column]=0
        for vehicle_object in self.vehicles:
            if(vehicle_object.vehicle_no==V_no):
                vehicle_object.unpark_vehicle()
        i=0
        for booking in self.bookings:
            i=i+1
            if(booking.vehicle_no==V_no):
                break
            
        self.bookings.pop(i-1)
        

        print(Back.GREEN +"vehicle unparked ")
        print(Back.BLUE +"Thankyou for Visiting")

    def park_vehicle(self):
        (building_no,floor_no)=self.parking_spaces[0].display_parking()
        print(Back.YELLOW +  '   Please Enter row you want to select    : ')
        row = int(input("-> "))
        print(Back.YELLOW +  '   Please Enter column you want to select : ')
        column = int(input("-> "))
        if(self.parking_spaces[0].parking_space[building_no][floor_no][row][column]==1):
            print(Back.RED + "Slot already booked ")
            self.park_vehicle()
        self.parking_spaces[0].view_slots(building_no,floor_no,row,column)
        V_no=  input("Please Enter Vehicle no            -> ")
        V_no=V_no.upper()
        vehicle_data_present=False
        vehicle_object=""
        for vehicle in self.vehicles:
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
            vehicle_object=self.add_vehicle(V_no,V_type,V_owner,V_colour,V_brand)
            print(Back.GREEN + "Vehicle information stored")
        
        if(vehicle_data_present==True):
            if(vehicle_object.vehicle_parked=="P"):
                print(Back.RED + "Vehicle Already Parked ")
                self.employee_functionality()
            print(Back.GREEN + "Vehicle information already stored")
            V_no=vehicle_object.vehicle_no
            V_type=vehicle_object.vehicle_type
        booking=self.do_booking(V_no,V_type,building_no,floor_no,row,column)
        booking.show_booking()
        self.parking_spaces[0].parking_space[building_no][floor_no][row][column]=1	     
        vehicle_object.park_vehicle()

    def employee_functionality(self):
        print(Back.CYAN + "+------------------------------+")
        print(Back.CYAN + "|  1- Park a Vehicle           |")
        print(Back.CYAN + "|  2- Unpark a Vehicle         |")
        print(Back.CYAN + "|  3- Display Parking space    |")
        print(Back.CYAN + "|  4- Logout                   |")
        print(Back.CYAN + "+------------------------------+")
        user_input = input("-> ")
        if user_input == '1':
            self.park_vehicle()
            self.employee_functionality()
        elif user_input == '2':
            self.unpark_vehicle()
            self.employee_functionality()
        elif user_input == '3':
            self.parking_spaces[0].display_parking()
            self.employee_functionality()
        elif user_input == '4':
            self.main_page()
        else:
            print(Back.RED+"    Please enter valid input    ")
            self.employee_functionality()

    def employee_login(self,admin_object):
        employees=admin_object.employees
        print(Back.YELLOW +'   Please Enter Employee id :   ')
        employee_id=input("-> ")
        employee_password=""
        for employee in employees:
            if(employee.E_id==employee_id):
                employee_password=employee.E_password
        password=""
        if(employee_password==""):
            print(Back.RED +'Invalid Credentials')
            self.employee_login(admin_object)
        else:
            
            print(Back.YELLOW +'   Please Enter Password :      ')
            password = getpass.getpass()
        if(password==employee_password):
            return True
        else:
            print(Back.RED+"      Invalid Password          ")
            self.login()

    def admin_functionality(self,admin_object):
        print(Back.CYAN + "+------------------------------+")
        print(Back.CYAN + "|  1- Create Employee          |")
        print(Back.CYAN + "|  2- Change Parking space     |")
        print(Back.CYAN + "|  3- Display Parking space    |")
        print(Back.CYAN + "|  4- Logout                   |")
        print(Back.CYAN + "+------------------------------+")
        user_input = input("-> ")
        if user_input == '1':
            admin_object.create_employee()
            self.admin_functionality(admin_object)
        elif user_input == '2':
            admin_object.change_parking_space(self.parking_spaces[0])
            self.admin_functionality(admin_object)
        elif user_input == '3':
            self.parking_spaces[0].display_parking()
            self.admin_functionality(admin_object)
        elif user_input == '4':
            self.main_page()
        else:
            print(Back.RED+"    Please enter valid input    ")
            self.admin_functionality(admin_object)

    def login(self):
        print(Back.CYAN + "+------------------------------+")
        print(Back.CYAN + "|  1- Admin                    |")
        print(Back.CYAN + "|  2- Employee                 |")
        print(Back.CYAN + "|  3- Main Menu                |")
        print(Back.CYAN + "+------------------------------+")
        user_input2 = input("-> ")
        
        if user_input2 == '1':
            print(Back.YELLOW +  'Please Enter Password : ')
            password = getpass.getpass()
            if password ==self.admin_object.password:
                for i in tqdm(range(4000)):
                    print("",end='\r')
                print("------------------------------------------------------------------------------------------------------------------------")
                print(Back.BLUE+"Hello Admin")
                self.admin_functionality(self.admin_object)
            if password != self.admin_object.password:
                print(Back.RED+"      Invalid Password          ")
                self.login()
        elif user_input2 == '2':
            if(self.employee_login(self.admin_object)):
                self.employee_functionality()
        elif user_input2=='3':
            self.main_page()
        else:
            print(Back.RED+"    Please enter valid input    ")
            self.login()

    def main_page(self):
        print(Back.CYAN + "+------------------------------+")
        print(Back.CYAN + "|  1- Login                    |")
        print(Back.CYAN + "|  2- Find a Vehicle           |")
        print(Back.CYAN + "|  3- Display Vehicle Charges  |")
        print(Back.CYAN + "|  4- Exit                     |")
        print(Back.CYAN + "+------------------------------+")
        user_input = input("-> ")
        if user_input == '1':
            self.login()
        elif user_input == '2':
            self.find_vehicle()
            self.main_page()
        elif user_input == '3':
            print(Back.YELLOW + "Enter Vehicle no of Vehicle u want to get location of ")
            V_no=input("-> ")
            current_cost=self.do_billing(V_no.upper())
            print(Back.GREEN + f"Your Current vehicle charges are {current_cost} ")
            self.main_page()
        elif user_input == '4':
            exit()
        else:
            print(Back.RED+"    Please enter valid input    ")
            self.main_page()