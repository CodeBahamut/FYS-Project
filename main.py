from flask import Flask, render_template, redirect
from time import sleep
from gpiozero import Motor
from pyPS4Controller.controller import Controller # sudo pip install pyPS4Controller
import socket

app = Flask(__name__)

motor1 = Motor(forward=(7), backward=(8))
motor2 = Motor(forward=(9), backward=(10))

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60) # https://pes.mundayweb.com/html/Using%20PS4%20Control%20Pads%20via%20Bluetooth.html#pairing-using-bluetoothctl

@app.route("/")
def index():
    return render_template('index.html')

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_R3_up(self):
        motor1.forward()

    def on_L3_up(self):
        motor2.forward()

    def on_R3_down(self):
        motor1.backward()

    def on_L3_down(self):
        motor2.backward()

    def on_x_press(self):
        motor1.stop()
        motor2.stop()

    def on_L3_y_at_rest(self):
        motor2.stop()

    def on_R3_y_at_rest(self):
        motor1.stop()



def forward():
    motor1.forward()
    motor2.forward()


def backward():
    motor1.backward()
    motor2.backward()


def left():
    motor1.forward()
    motor2.backward()


def right():
    motor1.backward()
    motor2.forward()


def stop():
    motor1.stop()
    motor2.stop()

def rfid_response(serverMACAddress, port, value):
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress, port))
    s.send(bytes(value, 'UTF-8'))
    s.close()


@app.route('/json')
def json():
    return render_template('json.html')


@app.route('/background_process_test')
def background_process_test():
    print "Hello"
    return "nothing"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
