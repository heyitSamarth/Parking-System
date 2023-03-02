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

class parkingSpace():
    def __init__(self):
        self.parking_space=[[[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]]
    
    def view_buildings(self):
        for i in range(len(self.parking_space)):
            print(f"--------",end=" ")
        print()
        for i in range(len(self.parking_space)):
            print(f"| Bno  |",end=" ")
        print()
        for i in range(len(self.parking_space)):
            print(f"|  {i}   |",end=" ")
        print()
        for i in range(len(self.parking_space)):
            print(f"--------",end=" ")
        print()
        for i in range(len(self.parking_space)):
            print(f"floors {len(self.parking_space[i])}",end=" ")
        print()
    def view_floors(self,building_no):
        print(f"------------")
        for i in reversed(range(len(self.parking_space[building_no]))):
            print(f"|floor no {i}|")
            print(f"------------")
    def view_slots(self,building_no,floor_no,row="@",column="@"):
        print()
        rcount=0
        for rows in self.parking_space[building_no][floor_no]:
            print(f"{rcount}-> | ",end=" ")
            
            count=0
            for slot in rows:
                if(row==rcount and column==count):
                    print(Back.RED+f"[{count}]",end=" ")
                    print(" ",end=" ")
                    count=count+1
                elif(slot==1 ):
                    print(Back.MAGENTA+f"[{count}]",end=" ")
                    print(" ",end=" ")
                    count=count+1
                else:
                    print(f"[{count}]",end=" ")
                    print(" ",end=" ")
                    count=count+1
            print("|")
            rcount=rcount+1
        print()	

    def display_parking(self):
        self.view_buildings()
        print(Back.YELLOW +  '   Please Enter Building no :   ')
        building_no = int(input("-> "))
        self.view_floors(building_no)
        print(Back.YELLOW +  '   Please Enter floor no :   ')
        floor_no = int(input("-> "))
        self.view_slots(building_no,floor_no)
        return(building_no,floor_no)

# class Building():
#     def __init__(self):
#         self.floor=[]

# class floor():
#     def __init__(self):
#         self.slot=[]
    

# class slot():
#     def __init__(self):
#         self.is_empty=True