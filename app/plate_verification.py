import os
from database import  db  ,Vehicle , Entry , DB_Manager
import emoji
from datetime import datetime , timedelta

db_man = DB_Manager()

class Verificator:
    '''Temporary store car list'''
    def __init__(self):
        self.car_list = []
        self.get_plates_db() 
        self.current_plate = ''
        self.current_owner = ''

        self.cooldown = '' 
        self.current_time = ''

    def verify_car(self, plate_num):
        plate_num = plate_num.upper()
        self.current_plate = plate_num

        self.clear_local_plates()
        self.get_plates_db()

        # --------------------- DEBUG: print car list and verify --------------------- #
        # print(f"VERIFYING: [ {plate_num} ]")
        # print(f"CAR LIST: {self.car_list}")
        #

        if plate_num in self.car_list:
            print(emoji.emojize("Vehicle Verified! :balloon: "))
            car_obj_verified = Vehicle.query.filter_by(plate_num = plate_num).first() 

            try:
                if db_man.get_car_entries(car_obj_verified.plate_num):
                    print(emoji.emojize(":minibus: Car exist w/ atleast ONE entry :open_book:")) # DEBUG:
                    latest_entry = db_man.get_latest_entry(car_obj_verified.plate_num) # get latest entry
                    self.cooldown = latest_entry + timedelta(minutes  = 1) # get cooldown from latest entry
                    self.curr_time = datetime.now().isoformat(' ', 'seconds')  # get current time
                    self.curr_time = datetime.strptime(self.curr_time, "%Y-%m-%d %H:%M:%S") # format current time
                    
                    # ------------------------- DEBUG: Check time values ------------------------- #
                    # print("........................................")
                    # print(f"LATEST_ENTRY: {latest_entry}")
                    # print(f"COOLDOWN: {self.cooldown}")
                    # print(f"CURRENT TIME: {self.curr_time}")
                    # print("........................................")
                    #

                    if self.curr_time >= self.cooldown:
                        print(emoji.emojize("✅⏰ Not at Cooldown "))

                        # create new entry
                        curr_time_new_entry = datetime.now().isoformat(' ', 'seconds')
                        new_entry = Entry(plate = car_obj_verified.plate_num , entry_dtime = curr_time_new_entry) 
                        db.session.add(new_entry) 
                        db.session.commit() 
                        db_man.get_db_data()
                        
                        # for console log
                        latest_entry = db_man.get_latest_entry(car_obj_verified.plate_num)
                        self.cooldown = latest_entry + timedelta(minutes  = 1)
                        print(emoji.emojize(f"✍ CREATE NEW ENTRY: {car_obj_verified.plate_num} at {latest_entry}"))
                    else:
                        print(emoji.emojize(f":alarm_clock: at cooldown till {self.cooldown}"))
                else:
                    print(emoji.emojize(":bus: :anger: Car exist but NO entry :warning: | Create entry"))

                    # create new entry
                    curr_time_new_entry = datetime.now().isoformat(' ', 'seconds')
                    new_entry = Entry(plate = car_obj_verified.plate_num , entry_dtime = curr_time_new_entry) 
                    db.session.add(new_entry) 
                    db.session.commit() 
                    db_man.get_db_data()
                    print(f"New Entry From: {car_obj_verified.plate_num}")
            except Exception as e:
                print("ERROR!!!")
                print(f"EXCEPTION: {e}")
            print(".........................End Verify Instance........................")
        else:
            print(emoji.emojize("Vehicle Unverified! :warning:"))

    def add_car(self , plate_num):
        self.car_list.append(plate_num)

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

    def clear_local_plates(self):
        self.car_list = []

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



    



