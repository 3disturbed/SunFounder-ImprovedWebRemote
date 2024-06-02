import cv2
from flask import Flask, render_template, Response
from picarx import Picarx
from time import sleep
from robot_hat import ADC, TTS
import socket
from threading import Thread
import logging

# Initialize Flask app
app = Flask(__name__)
batt = ADC('A4')
HOST = "192.168.1.102"  # Listen on all network interfaces

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask video streaming
def gen_frames():
    camera = cv2.VideoCapture(0)  # Use 0 for web camera
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            logger.error("Failed to read frame from camera")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                logger.error("Failed to encode frame")
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Concatenate frame one by one and show result

@app.route('/')
def index():
    voltage = batt.read()
    voltage = voltage / 4095 * 3.3 * 3
    return render_template('index.html', voltage=voltage)

# Thread function for TTS
def tts_thread(ts, message):
    
    ts.say(message)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Robot control
def robot_control():
    px = Picarx()
    ts = TTS(amplitude=100, pitch=100, speed=100, voice='en-GB', engine='pico2wave')
    PORT = 5000  # Port to listen on (non-privileged ports are > 1023)
    speed = 0
    turn = 0
    headPan = 0
    headTilt = 0
    offset = -2

    # Configure TTS language
    #ts.lang("en-GB")
    ts.say("Hello, I am Jakey Bot. I am a robot designed to assist you.")
    ts.say("Jakey Bot online, awaiting instructions.")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            logger.info("Listening for connections...")
            conn, addr = s.accept()
            with conn:
                logger.info(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024).decode('ascii')
                    if not data:
                        break
                    # Convert the received data into a list of integers
                    data = data.strip().split(',')
                    if len(data) != 19:
                        break
                    
                    data = [int(x) for x in data]

                    wPressed = data[0]
                    aPressed = data[1]
                    sPressed = data[2]
                    dPressed = data[3]
                    upPressed = data[4]
                    downPressed = data[5]
                    leftPressed = data[6]
                    rightPressed = data[7]
                    ePressed = data[8]
                    qPressed = data[9]
                    onePressed = data[10]
                    twoPressed = data[11]
                    threePressed = data[12]
                    fourPressed = data[13]
                    fivePressed = data[14]
                    sixPressed = data[15]
                    sevenPressed = data[16]
                    eightPressed = data[17]
                    ninePressed = data[18]

                    if wPressed == 1:
                        speed = 100
                    elif sPressed == 1:
                        speed = -100
                    else:
                        speed = 0

                    if aPressed == 1:
                        turn = -30
                    elif dPressed == 1:
                        turn = 30
                    else:
                        turn = 0

                    # Head pan and tilt using up, down, left, right to add 1 degree
                    if upPressed == 1:
                        headTilt += 10
                    elif downPressed == 1:
                        headTilt -= 10
                    if leftPressed == 1:
                        headPan += 10
                    elif rightPressed == 1:
                        headPan -= 10
                    # Q reset head pan and tilt
                    if qPressed == 1:
                        headPan = 0
                        headTilt = 0

                    if onePressed == 1:
                        Thread(target=tts_thread, args=(ts, "Move please", 50)).start()
                    elif twoPressed == 1:
                        Thread(target=tts_thread, args=(ts, "Coming through!", 70)).start()
                    elif threePressed == 1:
                        Thread(target=tts_thread, args=(ts, "Im stuck, Help me please", 30)).start()
                    elif fourPressed == 1:
                        Thread(target=tts_thread, args=(ts, "Could you open the door. I can not reach the handle", 80)).start()
                    elif fivePressed == 1:
                        Thread(target=tts_thread, args=(ts, "Dont mind me im just passing through!", 90)).start()
                    elif sixPressed == 1:
                        Thread(target=tts_thread, args=(ts, "My battery is low. Could you take me back to my owner?", 60)).start()
                    elif sevenPressed == 1:
                        Thread(target=tts_thread, args=(ts, "Lower intelligence life form detected.", 40)).start()
                    elif eightPressed == 1:
                        Thread(target=tts_thread, args=(ts, "Take me home I am low on battery!", 50)).start()
                    elif ninePressed == 1:
                        Thread(target=tts_thread, args=(ts, "Dark Firebeard made some cool firmware you should become a patron", 100)).start()
            
                    px.set_cam_pan_angle(headPan)
                    px.set_cam_tilt_angle(headTilt)
                    px.set_dir_servo_angle(turn - offset)
                    px.forward(speed)
                    
                    sleep(0.1)

if __name__ == '__main__':
# Start the robot control thread
robot_thread = Thread(target=robot_control)
robot_thread.start()

# Start the Flask web server
app.run(host=HOST, port=5001)
