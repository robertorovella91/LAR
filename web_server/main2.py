#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response
from camera import VideoCamera



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('provahtml.html')

def gen(camera):
    while True:
        #obj  = VideoCamera(0)
        frame = camera.get_frame()
        #frame1 = camera1.get_frame()
        
		#frame1 = frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #yield (b'--frame1\r\n'
         #      b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    obj  = VideoCamera(0)
    
    return Response(gen(obj),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    obj1  = VideoCamera("http://192.168.1.46:7777/video")
    
    return Response(gen(obj1),mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    
    app.run(host='192.168.1.131',port=9999,threaded=True, debug=False)
