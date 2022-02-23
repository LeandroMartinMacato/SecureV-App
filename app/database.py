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
        return f'Plate Num: {self.plate_num} | Owner Name: {self.owner_name} | Date Registered: {self.date_registered} '

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_entry = db.Column("date_of_entry" , db.Date() , default=datetime.datetime.now)
    # vehicle relation here

    def __init__(self):
        self.date_of_entry = self.date_of_entry

    def __repr__(self):
        return f"Date of Entry: {self.date_of_entry}"
