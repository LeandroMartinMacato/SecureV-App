import os
from database import  db  ,Vehicle 
import emoji

class Car:
    def __init__(self , pnum):
        self.pnum = pnum
        self.owner = None

    @property
    def pnum(self):
        return self._pnum

    @pnum.setter
    def pnum(self , new_pnum):
        self._pnum = new_pnum

    @pnum.getter
    def pnum(self):
        return self._pnum

    @pnum.deleter
    def pnum(self):
        print("Delete pnum!")
        self.pnum = None


class Verificator:
    '''Temporary store car list'''
    def __init__(self):
        # self.car_list = ["NXX8870" , "NXX887" , "tik142"]
        self.car_list = []
        self.get_plates_db() 
        self.current_plate = ''

    def verify_car(self, plate_num):
        plate_num = plate_num.lower()
        self.current_plate = plate_num
        currenty_plate = plate_num
        # --------------------- DEBUG: print car list and verify --------------------- #
        # print(f"VERIFYING: [ {plate_num} ]")
        # print(f"CAR LIST: {self.car_list}")

        if plate_num in self.car_list:
            # print("Vehicle Verified!")
            print(emoji.emojize("Vehicle Verified! :balloon: "))
        else:
            print(emoji.emojize("Vehicle Unverified! :warning:"))
            # print("Vehicle Unverified!")

    def add_car(self , plate_num):
        self.car_list.append(plate_num)
        print(f"Plate {plate_num} Added!")

    def delete_car(self , plate_num):
        self.car_list.remove(plate_num)
        print("Car Deleted!")

    def in_car_list(self, plate_num):
        if plate_num in self.car_list:
            return True
        else:
            return False

    def get_plates_db(self):
        car_list = []
        db.create_all()
        all_car_db = Vehicle.query.all()
        for car in all_car_db:
            plate = str(car).split("|")
            self.add_car(plate[0])

    def get_current_plate(self):
        return self.current_plate

# ----------------------------------- debug main ---------------------------------- #
if __name__ == "__main__":
    pass
    # test = Vehicle.query.all()
    # print(test)
    # print(type(test))


    # db.create_all()
    # verif = Verificator()


    # print(verif.car_list)



    



