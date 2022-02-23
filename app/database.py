




class Vehicle(db.Model):
    id = db.Column("id" , db.Integer , primary_key=True)
    plate_num = db.Column("plate_num" , db.String(6) , unique=True , nullable=False)
    owner_name = db.Column("owner_name" , db.String(20) ,  unique=True , nullable=False)

    def __init__(self, plate_num , owner_name):
        self.plate_num = plate_num
        self.owner_name = owner_name
        

    def __repr__(self):
        return f'Plate Num: {self.plate_num} | Owner Name: {self.owner_name}'