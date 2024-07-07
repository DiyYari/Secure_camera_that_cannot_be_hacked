from flask import Flask, Response, render_template, request
from picamera2 import Picamera2
import io
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import threading
import time

app = Flask(__name__)

# Camera setup
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (720, 576)}))
camera.start()

# PCA9685 and servo setup
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard frequency for most servos

# Servo configuration
servo1 = servo.Servo(pca.channels[0], min_pulse=600, max_pulse=2400)

# Set initial angle
servo1.angle = 90

# Global variable for target angle
servo1_target = 90

servo_lock = threading.Lock()

def servo_control():
    global servo1_target
    while True:
        with servo_lock:
            if servo1.angle is not None and abs(servo1.angle - servo1_target) > 0.5:
                servo1.angle = servo1_target
            
            print(f"Servo1 angle: {servo1.angle}, target: {servo1_target}")
        
        time.sleep(0.02)  # 50Hz update rate

# Start servo control thread
threading.Thread(target=servo_control, daemon=True).start()

def generate():
    while True:
        stream = io.BytesIO()
        camera.capture_file(stream, format='jpeg')
        stream.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_servo', methods=['POST'])
def set_servo():
    global servo1_target
    angle = int(request.form['angle'])
    with servo_lock:
        servo1_target = max(0, min(180, angle))
        servo1.angle = servo1_target  # Set angle immediately
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
