from gpiozero import Motor, DistanceSensor
from sh import sudo
from pyPS4Controller.controller import Controller
import bluetooth
import config
import time


motor1 = Motor(forward=8, backward=7)
motor2 = Motor(forward=10, backward=9)
sensor = DistanceSensor(echo=29, trigger=28)


def check_distance():

    while True:
        distance = sensor.distance * 100
        print('Distance: ', distance)
        if distance > 5:
            config.controls_inactive = True
            break
        time.sleep(1)


def find_controller():
    loop = True
    while loop:
        result = bluetooth.lookup_name(config.controller_mac, timeout=20)
        if result is None:
            print("not detected")
        else:
            print("Controller found")
            try:
                sudo.bluetoothctl("trust", config.controller_mac)
                sudo.bluetoothctl("connect", config.controller_mac)
            except:
                print("Couldn't connect to controller")
            finally:
                break


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        if config.controls_inactive:
            self.stop()

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
        config.turn_speed = turn_value
        config.direction = "right"
        print(turn_value)
        motor1.backward(turn_value)

    def on_L3_left(self, value):
        turn_value = 1 - ((32767 + value) / 32767)
        config.turn_speed = turn_value
        config.direction = "left"
        print(turn_value)
        motor1.forward(turn_value)

    def on_L3_x_at_rest(self):
        if config.direction == "right":
            motor1.forward(config.turn_speed)
            time.sleep(0.15)

        if config.direction == "left":
            motor1.backward(config.turn_speed)
            time.sleep(0.15)

        motor1.stop()

    def disconnect(self):
        motor1.stop()
        motor2.stop()
