from flask import Flask, render_template, request, Response, redirect, url_for
from flask_bootstrap import Bootstrap

from object_detection import *

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

if __name__ == '__main__':
    application.run(debug = True)
