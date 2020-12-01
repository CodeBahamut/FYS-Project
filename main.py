from flask import Flask, render_template, redirect
from time import sleep
from gpiozero import Motor

app = Flask(__name__)

motor1 = Motor(forward=(7), backward=(8))
motor2 = Motor(forward=(9), backward=(10))


@app.route("/")
def index():
    return render_template('index.html')


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

@app.route('/json')
def json():
    return render_template('json.html')


@app.route('/background_process_test')
def background_process_test():
    print "Hello"
    return "nothing"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
