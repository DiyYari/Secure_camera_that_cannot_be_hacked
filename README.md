https://www.realvnc.com/en/connect/download/viewer/?lai_sr=5-9&lai_sl=l

commands for setting up remote access to the system

Sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer

Ifconfig (IP address check)


these commands must be entered in the Rasberry PI environment to install the necessary libraries

sudo apt update

sudo apt upgrade -y

sudo apt install python3-pip -y

sudo apt install -y python3-libcamera python3-kms++

pip3 install Flask picamera2 adafruit-circuitpython-pca9685 adafruit-circuitpython-motor

#if there is a problem with the installation

sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED

#then run it again

pip3 install Flask picamera2 adafruit-circuitpython-pca9685 adafruit-circuitpython-motor

sudo apt install -y i2c-tools python3-smbus

save the camera.py file to a new folder for example "camera"

index.html to the folder camera/templates/index.html, 

then do: python3 camera.py



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Гусеничный вездеход с поворотной камерой</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            touch-action: none;
        }
        #joystick {
            width: 300px;
            height: 300px;
            border: 1px solid #000;
            border-radius: 50%;
            margin: 20px;
        }
        .control-container {
            margin: 20px 0;
            width: 300px;
        }
        input[type="range"] {
            width: 100%;
        }
    </style>
</head>
<body>
    <h1>Управление вездеходом</h1>
    <img src="{{ url_for('video_feed') }}" style="width: 720px; height: 480px;">
    <canvas id="joystick" width="300" height="300"></canvas>
    <div class="control-container">
        <label for="servo">Поворот камеры:</label>
        <input type="range" id="servo" name="servo" min="0" max="180" value="90" oninput="updateServo(this.value)">
        <span id="servoValue">90</span>
    </div>
    <script>
        const joystick = document.getElementById('joystick');
        const ctx = joystick.getContext('2d');
        let joystickPressed = false;
        let centerX = joystick.width / 2;
        let centerY = joystick.height / 2;
        let maxDistance = joystick.width / 2;

        function drawJoystick(x, y) {
            ctx.clearRect(0, 0, joystick.width, joystick.height);
            ctx.beginPath();
            ctx.arc(centerX, centerY, maxDistance, 0, 2 * Math.PI);
            ctx.strokeStyle = '#000';
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(x, y, 20, 0, 2 * Math.PI);
            ctx.fillStyle = '#00F';
            ctx.fill();
        }

        function handleJoystick(e) {
            if (!joystickPressed) return;
            let rect = joystick.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;
            if (e.touches) {
                x = e.touches[0].clientX - rect.left;
                y = e.touches[0].clientY - rect.top;
            }
            let dx = x - centerX;
            let dy = y - centerY;
            let distance = Math.sqrt(dx*dx + dy*dy);
            if (distance > maxDistance) {
                x = centerX + (dx * maxDistance) / distance;
                y = centerY + (dy * maxDistance) / distance;
            }
            drawJoystick(x, y);
            updateMotors(dx / maxDistance, -dy / maxDistance);
        }

        joystick.addEventListener('mousedown', (e) => {
            joystickPressed = true;
            handleJoystick(e);
        });
        joystick.addEventListener('mousemove', handleJoystick);
        joystick.addEventListener('mouseup', () => {
            joystickPressed = false;
            drawJoystick(centerX, centerY);
            updateMotors(0, 0);
        });
        joystick.addEventListener('mouseleave', () => {
            if (joystickPressed) {
                joystickPressed = false;
                drawJoystick(centerX, centerY);
                updateMotors(0, 0);
            }
        });

        joystick.addEventListener('touchstart', (e) => {
            joystickPressed = true;
            handleJoystick(e);
        });
        joystick.addEventListener('touchmove', handleJoystick);
        joystick.addEventListener('touchend', () => {
            joystickPressed = false;
            drawJoystick(centerX, centerY);
            updateMotors(0, 0);
        });

        drawJoystick(centerX, centerY);

        function updateMotors(x, y) {
            let leftMotor = y + x;
            let rightMotor = y - x;
            leftMotor = Math.max(-1, Math.min(1, leftMotor)) * 100;
            rightMotor = Math.max(-1, Math.min(1, rightMotor)) * 100;
            fetch('/set_motors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `left=${leftMotor}&right=${rightMotor}`
            });
        }

        function updateServo(value) {
            document.getElementById('servoValue').innerText = value;
            fetch('/set_servo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'angle=' + value
            });
        }
    </script>
</body>
</html>
