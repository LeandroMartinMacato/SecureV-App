from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/vehicle_db.sqlite3' # Config to use sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Vehicle(db.Model):
    id = db.Column("id" , db.Integer , primary_key=True)
    plate_num = db.Column("plate_num" , db.String(6) )
    owner_name = db.Column("owner_name" , db.String(20) )
    date_registered = db.Column("date_registered" , db.Date(), default=datetime.utcnow )

    def __init__(self, plate_num , owner_name):
        self.plate_num = plate_num
        self.owner_name = owner_name
        

    def __repr__(self):
        return f'{self.plate_num}|{self.owner_name}|{self.date_registered}'

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_entry = db.Column("date_of_entry" , db.Date() , default=datetime.utcnow)
    # vehicle relation here

    def __init__(self):
        self.date_of_entry = self.date_of_entry

    def __repr__(self):
        return f"Date of Entry: {self.date_of_entry}"

class DB_Manager():
    def __init__(self):
        self.db_connected = False
        self.db_data = []
        self.get_db_data()
        self.count = 0
        count = 0

    def get_db_data(self):
        self.db_data = [] # Clear current db_data to get fresh fetch
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






if __name__ == '__main__':
    pass
    # db.create_all()
    # db_man = DB_Manager()
    # db_man.get_db_data()
    # print(db_man.db_data)
    # test = Vehicle.query.filter_by(plate_num = "plate_num").first()
    # test = Vehicle.query.all()