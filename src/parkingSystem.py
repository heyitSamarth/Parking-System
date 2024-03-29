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

from billing import Billing
from parkingspace import ParkingSpace
from vehicle import Vehicle
from user import Admin
from booking import Booking

class ParkingSystem:
    def __init__(self):
        self.parking_spaces = []
        self.vehicles = []
        self.bookings=[]
        self.billings=[]
        self.add_parking_space()
        self.admin_object=Admin()

    def add_parking_space(self):
        parking_space = ParkingSpace()
        self.parking_spaces.append(parking_space)
    
    def add_vechile(self,vehicle_no):
        if(True):
            print(Back.CYAN + "+------------------------+")
            print(Back.CYAN + "|  1- Car (LMV)          |")
            print(Back.CYAN + "|  2- Truck (HMV)        |")
            print(Back.CYAN + "|  3- Bike (MC)          |")
            print(Back.CYAN + "+------------------------+")
            vehicle_type_option=0
            while (vehicle_type_option!='1' and  vehicle_type_option!='2' and vehicle_type_option!='3'):
                vehicle_type_option=input("Please Select Vehicle type         -> ")
            if(vehicle_type_option=='1'):
                vehicle_type="LMV"
            if(vehicle_type_option=='2'):
                vehicle_type="HMV"
            if(vehicle_type_option=='3'):
                vehicle_type="MC"
            vehicle_owner=str(input("Please Enter Vehicle owner         -> "))
            vehicle_colour=   input("Please enter Vehicle colour        -> ")
            vehicle_brand=    input("Please enter Vehicle brand         -> ")
            print(Back.YELLOW + "Please Verify the Information")
            print("Vehicle no       = "+ vehicle_no)
            print("Vehicle type     = "+ vehicle_type)
            print("Vehicle owner    = "+ vehicle_owner)
            print("Vehicle colour   = "+ vehicle_colour)
            print("Vehicle brand    = "+ vehicle_brand)
            input("Press Enter to continue or CTRL+C to Break Operation")
            print(Back.GREEN + "Vehicle information stored")
        vehicle_object=Vehicle(vehicle_no,vehicle_type,vehicle_owner,vehicle_colour,vehicle_brand)
        self.vehicles.append(vehicle_object)
        return vehicle_object

    def do_booking(self,vehicle_no,vehicle_type , building , floor ,row ,column):
        booking_object=Booking(vehicle_no,vehicle_type , building , floor ,row ,column ,datetime.datetime.now())
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
        vehicle_type=vehicle_object.vehicle_type
        park_in_time=vehicle_object.park_in_time
        duration=datetime.datetime.now()-datetime.datetime.strptime(str(park_in_time),'%Y-%m-%d %H:%M:%S.%f')
        duration=divmod(duration.total_seconds(),3600)[0]
        parking_charges=0
        if(vehicle_type=="LMV"):
            if(duration<2):
                parking_charges = 30
            elif(duration<12):
                parking_charges = 80
            else:
                parking_charges = 150
        elif(vehicle_type=="HMV"):
            if(duration<2):
                parking_charges = 60
            elif(duration<12):
                parking_charges = 140
            else:
                parking_charges = 300
        elif(vehicle_type=="MC"):
            if(duration<2):
                parking_charges = 10
            elif(duration<12):
                parking_charges = 30
            else:
                parking_charges = 70
        parking_bill=Billing(vehicle_no,vehicle_type,park_in_time,datetime.datetime.now(),parking_charges)
        self.billings.append(parking_bill)
        return parking_charges

    def find_vehicle(self):
        print(Back.YELLOW + "Enter Vehicle no of Vehicle u want location to Unpark")
        vehicle_no=input("-> ")
        vehicle_no=vehicle_no.upper()
        vehicle_object=""
        for booking in self.bookings:
            if(booking.vehicle_no==vehicle_no):
                vehicle_object=booking

        if(vehicle_object==""):
            print(Back.RED + "Enter Correct Vehicle no  ")
            return
        building_no=vehicle_object.building
        floor_no=vehicle_object.floor
        row=vehicle_object.row
        column=vehicle_object.column
        print(Back.GREEN + f"Your Vechile is Located at Floor no {floor_no} of Buildin no {building_no} at Red location")
        self.parking_spaces[0].view_slots(building_no,floor_no,"vehicle_object.vehicle_type",row,column)
        return (vehicle_no,building_no,floor_no,row,column)




    def employee_functionality(self,employee_object):
        print(Back.CYAN + "+------------------------------+")
        print(Back.CYAN + "|  1- Park a Vehicle (specific)|")
        print(Back.CYAN + "|  2- Park a Vehicle (random)  |")
        print(Back.CYAN + "|  3- Unpark a Vehicle         |")
        print(Back.CYAN + "|  4- Display Parking space    |")
        print(Back.CYAN + "|  5- Logout                   |")
        print(Back.CYAN + "+------------------------------+")
        user_input = input("-> ")
        if user_input == '1':
            employee_object.park_vehicle(self.parking_spaces,self.vehicles,self.do_booking,self.add_vechile)
            self.employee_functionality(employee_object)
        elif user_input == '2':
            employee_object.random_park_vehicle(self.parking_spaces,self.vehicles,self.do_booking,self.add_vechile)
            self.employee_functionality(employee_object)
        elif user_input == '3':
            employee_object.unpark_vehicle(self.parking_spaces,self.vehicles,self.bookings,self.do_billing)
            self.employee_functionality(employee_object)
        elif user_input == '4':
            self.parking_spaces[0].display_parking()
            self.employee_functionality(employee_object)
        elif user_input == '5':
            self.main_page()
        else:
            print(Back.RED+"    Please enter valid input    ")
            self.employee_functionality(employee_object)

    def employee_login(self,admin_object):
        employees=admin_object.employees
        print(Back.YELLOW +'   Please Enter Employee id :   ')
        employee_id=input("-> ")
        employee_object=False
        employee_password=""
        for employee in employees:
            if(employee.E_id==employee_id):
                employee_password=employee.E_password
                employee_object=employee
        password=""
        if(employee_password==""):
            print(Back.RED +'Invalid Credentials')
            return self.employee_login(admin_object)
        else:
            print(Back.YELLOW +'   Please Enter Password :      ')
            password = getpass.getpass()
        if(password==employee_password):
            return employee_object
        else:
            print(Back.RED+"      Invalid Password          ")

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
            else:
                print(Back.RED+"      Invalid Password          ")
                self.login()
        elif user_input2 == '2':
            employee_object=self.employee_login(self.admin_object)
            if(employee_object):
                self.employee_functionality(employee_object)
            self.login()
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
            vehicle_no=input("-> ").upper()
            current_cost= self.do_billing(vehicle_no)
            print(Back.GREEN + f"Your Current Vechile charges are {current_cost} ")
            self.main_page()
        elif user_input == '4':
            exit()
        else:
            print(Back.RED+"    Please enter valid input    ")
            self.main_page()