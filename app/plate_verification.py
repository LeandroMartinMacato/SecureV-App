import os
from database import  db  ,Vehicle , Entry , DB_Manager
import emoji

class Verificator:
    '''Temporary store car list'''
    def __init__(self):
        # self.car_list = ["NXX8870" , "NXX887" , "tik142"]
        self.car_list = []
        self.get_plates_db() 
        self.current_plate = ''
        self.current_owner = ''

    def verify_car(self, plate_num):
        plate_num = plate_num.lower()
        self.current_plate = plate_num
        # self.current_owner = db
        # --------------------- DEBUG: print car list and verify --------------------- #
        # print(f"VERIFYING: [ {plate_num} ]")
        # print(f"CAR LIST: {self.car_list}")

        if plate_num in self.car_list:
            # print("Vehicle Verified!")
            print(emoji.emojize("Vehicle Verified! :balloon: "))

            #TODO Create condition to not create entry after a entry is created
            car_obj_verified = Vehicle.query.filter_by(plate_num = plate_num).first() 
            new_entry = Entry(plate = car_obj_verified.plate_num) 
            db.session.add(new_entry) 
            db.session.commit() 
            print(f"New Entry From: {car_obj_verified.plate_num}")

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



    



