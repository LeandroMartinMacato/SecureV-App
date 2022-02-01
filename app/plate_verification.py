import os


class Car:
    def __init__(self , pnum):
        self.pnum = pnum
        self.owner = None



class Verificator():
    '''Temporary store car list'''
    def __init__(self):
        self.car_list = ["ABY8512" , "ABY852" , "ABY751"]

    def verify_car(plate_num):
        print("Trying Verificator.verify_car()")
        if plate_num in self.car_list:
            print("Vehicle Verified!")
        else:
            print("Vehicle Unverified!")

    def add_car():
        pass

    def delete_car():
        pass