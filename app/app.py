from flask import Flask, render_template, request, Response, redirect, url_for , session
from flask_bootstrap import Bootstrap

from object_detection import *

from flask_sqlalchemy import SQLAlchemy # import sqlalchemy
from database import db , Vehicle , DB_Manager

import webbrowser
from threading import Timer #Debug Autostart

application = Flask(__name__)
application.config.update(
    TESTING = True,
    SECRET_KEY = "password"
)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/vehicle_db.sqlite3' # Config to use sqlalchemy
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

VIDEO = VideoStreaming()


@application.route('/')
def home():
    TITLE = 'SecureV'
    return render_template('index.html', TITLE=TITLE)

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
    db_man = DB_Manager()
    return render_template("data_mode.html" , db_data = db_man.db_data) 

@application.route("/register", methods=["POST","GET"])
def register_mode():
    if request.method =="POST":
        session.permanent = True
        plate_input = request.form["plate_input"]
        owner_input = request.form["owner_input"]
        current_registering = Vehicle(plate_num = plate_input , owner_name = owner_input)
        db.session.add(current_registering)
        db.session.commit()

    return render_template("register_mode.html") 

@application.route("/logs")
def log_mode():
    return render_template("log_mode.html") 

def open_browser():
    ''' Debug autostartt'''
    webbrowser.open_new('http://127.0.0.1:2000/')


if __name__ == '__main__':
    # Timer(3, open_browser).start() # Auto open browser
    # db.create_all() # Create db when it doesnt exist

    application.run(port = 2000 , debug = True)