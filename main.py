from flask import Flask, render_template
from gpiozero import Motor
import bluetooth
from sh import sudo
from pyPS4Controller.controller import Controller
import socket

app = Flask(__name__)


motor1 = Motor(forward=8, backward=7)
motor2 = Motor(forward=10, backward=9)

controller_mac = "DC:0C:2D:72:E6:EE"


@app.route("/")
def index():
    return render_template('index.html')


def find_controller():
    loop = True
    while loop:
        result = bluetooth.lookup_name(controller_mac, timeout=20)
        if result is None:
            print("not detected")
        else:
            print("Controller found")
            try:
                sudo.bluetoothctl("trust", controller_mac)
                sudo.bluetoothctl("connect", controller_mac)
            except:
                print("Couldn't connect to controller")
            finally:
                break


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_R2_press(self, value):
        speed_value = (32767 + value) / 65534
        print(speed_value)
        motor2.forward(speed_value)

    def on_R2_release(self):
        motor2.stop()

    def on_L2_press(self, value):
        speed_value = (32767 + value) / 65534
        print("on_L2_press: {}".format(speed_value))
        motor2.backward(speed_value)

    def on_L2_release(self):
        motor2.stop()

    def on_square_press(self):
        motor2.stop()

    def on_L3_right(self, value):
        turn_value = value / 32767
        print(turn_value)
        motor1.backward(turn_value)

    def on_L3_left(self, value):
        turn_value = 1 - ((32767 + value) / 32767)
        print(turn_value)
        motor1.forward(turn_value)

    def on_L3_x_at_rest(self):
        motor1.stop()


find_controller()

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()


def rfid_response(server_mac_address, port, value):
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((server_mac_address, port))
    s.send(bytes(value, 'UTF-8'))
    s.close()


@app.route('/json')
def json():
    return render_template('json.html')


@app.route('/background_process_test')
def background_process_test():
    return "nothing"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
