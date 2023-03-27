
from tqdm.auto import tqdm
import colorama
from colorama import Back, Style
from pickle import load,dump
colorama.init(autoreset=True)
from parking_slot import ParkingSlot

class User():
    def __init__(self):
        pass

class Employee(User):
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
        vehicle_no=input("-> ")
        vehicle_no=vehicle_no.upper()
        booking_object=""
        for booking in bookings:
            if(booking.vehicle_no==vehicle_no):
                booking_object=booking

        if(booking_object==""):
            print(Back.RED + "Enter Correct Vehicle no  ")
            return
        building_no=booking_object.building
        floor_no=booking_object.floor
        row=booking_object.row
        column=booking_object.column
        print(Back.GREEN + f"Your vehicle is Located at Floor no {floor_no} of Buildin no {building_no} at Red location ( row {row} and column {column})")
        parking_spaces[0].view_slots(building_no,floor_no,"booking_object.vehicle_type",row,column)
        print(Back.YELLOW +"Calculating Vechile Charges ")

        charges=do_billing(vehicle_no)

        print(Back.GREEN +f"Charges for vehicle no {vehicle_no} are {charges}$")
        input("Press Enter if payment Recived")
        parking_spaces[0].parking_space[building_no][floor_no][row][column].reserved=False
        for vehicle_object in vehicles:
            if(vehicle_object.vehicle_no==vehicle_no):
                vehicle_object.unpark_vehicle()
        i=0
        for booking in bookings:
            i=i+1
            if(booking.vehicle_no==vehicle_no):
                break
            
        bookings.pop(i-1)
        print(Back.GREEN +"Vechile unparked ")
        print(Back.BLUE +"Thankyou for Visiting")

    def check_empty_space(self,parking_spaces,vehicle_type):
        building_no=""
        floor_no=""
        row_no=""
        column_no=""
        for  building in range(len(parking_spaces[0].parking_space)):
            for floor in range(len(parking_spaces[0].parking_space[building])):
                for row in range(len(parking_spaces[0].parking_space[building][floor])):
                    for column in range(len(parking_spaces[0].parking_space[building][floor][row])):
                        if(parking_spaces[0].parking_space[building][floor][row][column].reserved==False and parking_spaces[0].parking_space[building][floor][row][column].slot_type==vehicle_type ):
                            return(building,floor,row,column)
    
    def random_park_vehicle(self,parking_spaces,vehicles,do_booking,add_vehicle):
        vehicle_no=  input("Please Enter Vehicle no            -> ")
        vehicle_no=vehicle_no.upper()
        vehicle_object=""
        vehicle_data_present=False
        for vehicle in vehicles:
            if(vehicle.vehicle_no==vehicle_no):
                vehicle_data_present=True
                vehicle_object=vehicle

        if(vehicle_data_present==True):
            if(vehicle_object.vehicle_parked=="P"):
                print(Back.RED + "Vehicle Already Parked ")
                return
            print(Back.GREEN + "Vehicle information already stored")
        else:
            vehicle_object=add_vehicle(vehicle_no)
        
        vehicle_no=vehicle_object.vehicle_no
        vehicle_type=vehicle_object.vehicle_type

        # (building_no,floor_no)=parking_spaces[0].display_parking(vehicle_type)
        (building_no,floor_no,row,column)=self.check_empty_space(parking_spaces,vehicle_type)
        print(Back.GREEN +f"Vechile parked at floor {floor_no} of Building {building_no} ")
        if(parking_spaces[0].parking_space[building_no][floor_no][row][column].reserved==True):
            print(Back.RED + "Slot already booked ")
            return
        parking_spaces[0].view_slots(building_no,floor_no,vehicle_type,row,column)
        input("Press Enter to continue Booking")
        booking=do_booking(vehicle_no,vehicle_type,building_no,floor_no,row,column)
        booking.show_booking()
        parking_spaces[0].parking_space[building_no][floor_no][row][column].reserved=True
        vehicle_object.park_vehicle()

    def park_vehicle(self,parking_spaces,vehicles,do_booking,add_vehicle):
        vehicle_no=  input("Please Enter Vehicle no            -> ")
        vehicle_no=vehicle_no.upper()
        vehicle_object=""
        vehicle_data_present=False
        for vehicle in vehicles:
            if(vehicle.vehicle_no==vehicle_no):
                vehicle_data_present=True
                vehicle_object=vehicle

        if(vehicle_data_present==True):
            if(vehicle_object.vehicle_parked=="P"):
                print(Back.RED + "Vehicle Already Parked ")
                return
            print(Back.GREEN + "Vehicle information already stored")
        else:
            vehicle_object=add_vehicle(vehicle_no)
        
        vehicle_no=vehicle_object.vehicle_no
        vehicle_type=vehicle_object.vehicle_type
        
        (building_no,floor_no)=parking_spaces[0].display_parking(vehicle_type)
        print(Back.YELLOW +  '   Please Enter Slot id you want to select    : ')
        selected_slot_id=input("-> ").lower()
        row=ord(selected_slot_id[0])-ord('a')
        column=int(selected_slot_id[1:])
        if(parking_spaces[0].parking_space[building_no][floor_no][row][column].reserved==True):
            print(Back.RED + "Slot already booked ")
            return
        parking_spaces[0].view_slots(building_no,floor_no,vehicle_type,row,column)
        input("Press Enter to continue Booking")
        booking=do_booking(vehicle_no,vehicle_type,building_no,floor_no,row,column)
        booking.show_booking()
        parking_spaces[0].parking_space[building_no][floor_no][row][column].reserved=True
        vehicle_object.park_vehicle()


class Admin(User):
    def __init__(self):
        self.employees=[]
        self.password="aka"
        employee=Employee('sam','sam','sam','sam')
        self.employees.append(employee)

    def create_employee(self):
        E_name=str(input("Please Enter Employee Name         -> "))
        E_contact= input("Please enter Employee Contact No   -> ")
        E_id=str(input  ("Please Enter Employee Id           -> "))
        E_password=input("Please enter Employee password     -> ")
        print(Back.YELLOW + "Please Verify the Information")
        employee_object=Employee(E_name,E_contact,E_id,E_password)
        employee_object.employee_detail()
        input("Press Enter to continue or CTRL+C to Break Operation")
        self.employees.append(employee_object)
        print(Back.GREEN + "Employee information stored")

    def change_parking_space(self,parking_object):
        # parking_object=ParkingSpace()
        # print(Back.CYAN + "+------------------------------+")
        # print(Back.CYAN + "|  1- Add Parking Space        |")
        # print(Back.CYAN + "+------------------------------+")
        user_input = '1'
        if user_input == '1':
            print(Back.CYAN + "+------------------------------+")
            print(Back.CYAN + "|  1- Add Building             |")
            print(Back.CYAN + "|  2- Add floor in building    |")
            print(Back.CYAN + "|  3- Add Slot in building     |")
            print(Back.CYAN + "|  4- Previous Menu            |")
            print(Back.CYAN + "+------------------------------+")
            user_input2 = input("-> ")
            if user_input2 == '1':
                parking_object.parking_space.append([])
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
                print(Back.YELLOW + "Enter Vehicle slot Type   ")
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
                for i in range( no_of_rows):
                    parking_object.parking_space[building_no][floor_no].append([])
                    for j in range(no_of_columns):
                        slot_id=chr(ord('a')+(i+existing_slot))+str(j)
                        slot=ParkingSlot(slot_id,vehicle_type)
                        parking_object.parking_space[building_no][floor_no][i+existing_slot].append(slot)
                parking_object.view_slots(building_no,floor_no)
            elif user_input2 == '4':
                return
            else :
                print(Back.RED+"    Please enter valid input    ")
        self.change_parking_space(parking_object)