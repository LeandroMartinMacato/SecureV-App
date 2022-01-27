from flask import Flask , render_template , Response , session , request
from camera import Video
from flask_sqlalchemy import SQLAlchemy # import sqlalchemy


app = Flask(__name__)

app.secret_key = "password" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_db.sqlite3' # Config to use sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable warning on modification

db = SQLAlchemy(app)

class Vehicle(db.Model):
    id = db.Column("id" , db.Integer , primary_key=True)
    plate_num = db.Column("plate_num" , db.String(6) )
    owner_name = db.Column("owner_name" , db.String(20))

    def __init__(self, plate_num , owner_name):
        self.plate_num = plate_num
        self.owner_name = owner_name
        

    def __repr__(self):
        return '<User: %s>' % self.plate_num



@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/database")
def data_mode():
    return render_template("data_mode.html") 

@app.route("/register", methods=["POST","GET"])
def register_mode():
    if request.method =="POST":
        session.permanent = True
        plate_input = request.form["plate_input"]
        owner_input = request.form["owner_input"]
        current_registering = Vehicle(plate_num = plate_input , owner_name = owner_input)
        db.session.add(current_registering)
        db.session.commit()

    return render_template("register_mode.html") 

@app.route("/logs")
def log_mode():
    return render_template("log_mode.html") 

def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route("/video")
def video():
    return Response(gen(Video()),
    mimetype = 'multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    db.create_all() # Create db when it doesn't exist
    app.run(debug=True )


# https://www.youtube.com/watch?v=i_-m1kBTdBI