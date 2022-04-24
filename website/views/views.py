from flask import Blueprint, Response,render_template
# from camera import VideoCamera

views = Blueprint('views',__name__)

views.route ('/')
def index():
    return render_template('index.html')

def gen (camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

views.route ('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')