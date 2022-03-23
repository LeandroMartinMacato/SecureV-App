from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime as dt

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
    id = db.Column(db.Integer, primary_key=True)
    date_of_entry = db.Column("date_of_entry" , db.String(30) ,nullable = False , default=dt.datetime.now)
    # entry_vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id") , nullable = False)
    entry_vehicle_plate = db.Column(db.String(6), db.ForeignKey("vehicle.plate_num") , nullable = False) # Test
    # vehicle relation here

    # def __init__(self , ):
    #     self.date_of_entry = self.date_of_entry
    #     self.vehicle_id = ""

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

    def get_owner_data(self,plate):
        return Vehicle.query.filter_by(plate_num = plate).first()

    def search_owner(self,plate):
        searched_owner = [element for element in self.db_data if element['plate_num'] == plate]
        return searched_owner[0]["owner_name"] 


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

    # ------------------------------- search debug ------------------------------- #
    # print(db_man.search_owner("tk142"))
    # test = Vehicle.query.filter_by(plate_num = "plate_num").first()
    # test = Vehicle.query.all()

    # -------------------------------- LOGS DEBUG -------------------------------- #

    # Create Vehicle
    # car_1 = Vehicle("luh143" , "pinut")
    # db.session.add(car_1)
    # db.session.commit()

    # Create Entry
    # car_1 = Vehicle.query.filter_by(plate_num = "luh143").first()
    # entry_1 = Entry(entry_vehicle_plate = car_1.plate_num)
    # db.session.add(entry_1)
    # db.session.commit()

    # show car entries
    # car_1 = Vehicle.query.filter_by(plate_num = "luh143").first()
    # print(f"Car_1 Entries : {car_1.entries}")

    # Show db_man data content
    # print(db_man.db_data)
    # print(db_man.db_data_entries)
