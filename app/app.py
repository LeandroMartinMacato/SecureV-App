import webbrowser
from flask import Flask, render_template, request, Response, redirect, url_for
from flask_bootstrap import Bootstrap

from object_detection import *

from threading import Timer #Debug Autostart

application = Flask(__name__)
Bootstrap(application)

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
    return render_template("data_mode.html") 

@application.route("/register", methods=["POST","GET"])
def register_mode():
    # if request.method =="POST":
    #     session.permanent = True
    #     plate_input = request.form["plate_input"]
    #     owner_input = request.form["owner_input"]
    #     current_registering = Vehicle(plate_num = plate_input , owner_name = owner_input)
    #     db.session.add(current_registering)
    #     db.session.commit()

    return render_template("register_mode.html") 

@application.route("/logs")
def log_mode():
    return render_template("log_mode.html") 

def open_browser():
    ''' Debug autostartt'''
    webbrowser.open_new('http://127.0.0.1:2000/')

if __name__ == '__main__':
    Timer(2, open_browser).start() # Auto open browser
    application.run(port = 2000 , debug = True)
    
