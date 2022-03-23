from flask import Flask, render_template, request, Response, redirect, url_for , session , jsonify
from flask_bootstrap import Bootstrap

from object_detection import *
import object_detection

from flask_sqlalchemy import SQLAlchemy # import sqlalchemy
from database import db , Vehicle , DB_Manager

import webbrowser

from threading import Timer #Debug Autostart

from plate_verification import Verificator

application = Flask(__name__)
application.config.update(
    TESTING = True,
    SECRET_KEY = "password"
)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/vehicle_db.sqlite3' # Config to use sqlalchemy
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
db_manager = DB_Manager()

VIDEO = VideoStreaming()

random_decimal = np.random.rand()

@application.route('/update_plate' , methods=['POST'])
def updateplate():
    current_plate = object_detection.current_plate 
    try:
        current_owner = db_manager.search_owner(current_plate)
    except:
        current_owner = "No owner found"

    return jsonify('' , render_template('dynamic_plate.html', PLATE = current_plate , OWNER = current_owner))

@application.route('/')
def home():
    page_title = 'SecureV | Home'
    current_plate = ""
    current_owner = ""
    return render_template('index.html', TITLE=page_title , PLATE = current_plate, OWNER = current_owner)

@application.route('/video_feed')
def video_feed():
    '''
    Video streaming route.
    '''
    return Response(
        VIDEO.show(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@application.route('/request_model_switch')
def request_model_switch():
    VIDEO.detect = not VIDEO.detect
    print('*'*10, VIDEO.detect)
    try:
        print("This is a return function from VideoStreaming class " + str(VIDEO.lblret))
    except:
        pass
    return "nothing"

@application.route("/database")
def data_mode():
    page_title = 'SecureV | Database Mode'
    db_man = DB_Manager()
    return render_template("data_mode.html" , db_data = db_man.db_data, TITLE=page_title) 

@application.route("/register", methods=["POST","GET"])
def register_mode():
    page_title = 'SecureV | Register Mode'
    if request.method =="POST":
        session.permanent = True
        plate_input = request.form["plate_input"]
        owner_input = request.form["owner_input"]
        current_registering = Vehicle(plate_num = plate_input , owner_name = owner_input)
        db.session.add(current_registering)
        db.session.commit()

    return render_template("register_mode.html", TITLE=page_title) 

@application.route("/logs")
def log_mode():
    page_title = 'SecureV | Log Mode'
    return render_template("log_mode.html", TITLE=page_title) 

def open_browser():
    ''' Debug autostartt'''
    webbrowser.open_new('http://127.0.0.1:2000/')


if __name__ == '__main__':
    # Timer(3, open_browser).start() # Auto open browser
    # db.create_all() # Create db when it doesnt exist

    application.run(port = 2000 , debug = True)