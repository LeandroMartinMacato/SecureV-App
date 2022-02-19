import os

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
        # self.car_list = ["ABY8512" , "ABY852" , "ABY751"]
        self.car_list = ["NXX8870" , "NXX887" , "tik142"]

    def verify_car(self, plate_num):
        if plate_num in self.car_list:
            print("Vehicle Verified!")
        else:
            print("Vehicle Unverified!")

    def add_car(self , plate_num):
        self.car_list.append(plate_num)
        print("Car Added!")

    def delete_car(self , plate_num):
        self.car_list.remove(plate_num)
        print("Car Deleted!")



# ----------------------------------- main ----------------------------------- #

# jazz = Car("tik142")
# innova = Car("abc123")

# verif_obj = Verificator()


# car_list = []

# car_list.append(jazz) # add car object to list
# car_list.append(innova) # add car object to list

# print(car_list)
# # verif_obj.verify_car(jazz.pnum)
# verif_obj.verify_car(car_list[0].pnum)
# verif_obj.verify_car(car_list[1].pnum)



