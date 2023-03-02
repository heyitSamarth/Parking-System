
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