from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/vehicle_db.sqlite3' # Config to use sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Vehicle(db.Model):
    id = db.Column("id" , db.Integer , primary_key=True)
    plate_num = db.Column("plate_num" , db.String(6), unique=True , nullable=False )
    owner_name = db.Column("owner_name" , db.String(20) , unique=True , nullable=False)
    date_registered = db.Column("date_registered" , db.Date(),nullable = False, default=datetime.utcnow )
    entries = db.relationship('Entry', backref = 'entry_plate' , lazy = True)

    def __init__(self, plate_num , owner_name):
        self.plate_num = plate_num
        self.owner_name = owner_name
        

    def __repr__(self):
        return f'{self.plate_num}|{self.owner_name}|{self.date_registered}'

class Entry(db.Model):
    curr_entry_time = datetime.now().isoformat(' ', 'seconds') 

    id = db.Column(db.Integer, primary_key=True)
    date_of_entry = db.Column("date_of_entry" , db.String(30) ,nullable = False , default= curr_entry_time)
    entry_vehicle_plate = db.Column(db.String(6), db.ForeignKey("vehicle.plate_num") , nullable = False) # Test

    def __init__(self , plate):
        # self.date_of_entry = self.date_of_entry
        self.entry_vehicle_plate = plate 

    def __repr__(self):
        return f"{self.date_of_entry}|{self.entry_vehicle_plate}"

class DB_Manager():
    def __init__(self):
        self.db_connected = False
        self.db_data = []
        self.db_data_entries = []
        self.get_db_data()
        self.count = 0
        count = 0

    def get_db_data(self):
        self.db_data = [] # Clear current db_data to get fresh fetch
        self.db_data_entries = [] # for LOGS

        # Vehicle
        all_db_data = Vehicle.query.all() 
        self.count = 0
        for data in all_db_data:
            data = str(data).split("|")
            self.count = self.count + 1 
            data_breakdown = {
                "id" : self.count,
                "plate_num": data[0],
                "owner_name": data[1],
                "date_registered": data[2]
            }
            self.db_data.append(data_breakdown)
        
        # Entries
        all_db_entries = Entry.query.all()
        self.count = 0
        for data in all_db_entries:
            data = str(data).split("|")
            self.count = self.count + 1 
            data_breakdown = {
                "id" : self.count,
                "date": data[0],
                "plate" : data[1]
            }
            self.db_data_entries.append(data_breakdown)

    def search_owner(self,plate):
        searched_owner = [element for element in self.db_data if element['plate_num'] == plate]
        return searched_owner[0]["owner_name"] 

    def get_car_entries(self , plate):
        ''' return all car entries from the db '''
        car_entry_list = []
        car_to_get_entries = Vehicle.query.filter_by(plate_num = plate).first()
        for entry in car_to_get_entries.entries:
            data_list = str(entry).split("|")
            car_entry_dt = data_list[0]
            car_entry_list.append(car_entry_dt)
        return car_entry_list

    def get_latest_entry(self , plate):
        ''' returns latest entry in datetime format'''
        car_entry_list = []
        car_to_get_entries = Vehicle.query.filter_by(plate_num = plate).first()
        for entry in car_to_get_entries.entries:
            data_list = str(entry).split("|")
            car_entry_dt = data_list[0]
            car_entry_list.append(car_entry_dt)

        if car_entry_list:
            latest_entry = car_entry_list[-1] # STRING
            latest_entry = datetime.strptime(latest_entry, "%Y-%m-%d %H:%M:%S")
            return latest_entry
        else:
            return "No atleast one entry found..."


if __name__ == '__main__':
    pass

    # ------------------------------ create db debug ----------------------------- #
    # db.create_all()
    # db_man = DB_Manager()
    # db_man.get_db_data()
    # print(db_man.db_data)
    
    # print data debug
    # print(db_man.get_owner_data("tk142"))
    # print(type(db_man.get_owner_data("tk142")))
    # print(type(db_man.db_data))

    # ------------------------------- search vehicle in db ------------------------------- #
    # test = Vehicle.query.filter_by(plate_num = "dab398").first()
    # print(test.plate_num)

    # -------------------------------- LOGS DEBUG -------------------------------- #

    # Create Vehicle
    # car_1 = Vehicle("dab398" , "billy")
    # db.session.add(car_1)
    # db.session.commit()

    # Create Entry
    # car_1 = Vehicle.query.filter_by(plate_num = "luh143").first()
    # entry_1 = Entry(entry_vehicle_plate = car_1.plate_num)
    # db.session.add(entry_1)
    # db.session.commit()

    # show car entries
    # car_1 = Vehicle.query.filter_by(plate_num = "dab398").first()
    # print(f"Car_1 Entries : {car_1.entries}")
    # print(type(car_1.entries))

    # get car entries
    # car_entries = db_man.get_car_entries("dab398")
    # print(type(car_entries))
    # print(car_entries)

    # get car latest entry
    # latest_entry = db_man.get_latest_entry("tk142")
    # print(latest_entry)

    # TEST
    # cooldown = latest_entry + timedelta(minutes=1)
    # curr_time = datetime.now().isoformat(' ', 'seconds') 
    # curr_time = datetime.strptime(curr_time, "%Y-%m-%d %H:%M:%S")
    # print(latest_entry)
    # print(type(latest_entry))

    # print(cooldown)
    # print(type(cooldown))

    # print(curr_time)
    # print(type(curr_time))

    # if curr_time >= cooldown:
    #     print("TRUE CREATE LOG")
    # else:
    #     print("FALSE ON COOLDOWN")

    # check if car has an entry
    # car_1 = Vehicle.query.filter_by(plate_num = "tk142").first()
    # try:
    #     if db_man.get_car_entries("dab398"):
    #         print("Car has atleast one entry")
    #         print("True")
    #     else:
    #         print("EMPTY")
    # except Exception as e:
    #     print(e)
    #     print("EXCEPTION: Car has no entry")


    # Show db_man data content
    # print(db_man.db_data)
    # print(db_man.db_data_entries)
