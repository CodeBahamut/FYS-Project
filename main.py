import RPi.GPIO as GPIO
from flask import Flask, render_template, redirect
from time import sleep
from gpiozero import Motor

app = Flask(__name__)

motor1 = Motor(forward=(7), backward=(8))
motor2 = Motor(forward=(9), backward=(10))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/Vooruit")
def vooruit():
    motor1.forward()
    motor2.forward()
    return redirect("/StatusVooruit")

@app.route("/Achteruit")
def achteruit():
    motor1.backward()
    motor2.backward()
    return redirect("/StatusAchteruit")

@app.route("/Links")
def links():
    motor1.forward()
    motor2.backward()
    return redirect("/StatusLinks")

@app.route("/Rechts")
def rechts():
    motor1.backward()
    motor2.forward()
    return redirect("/StatusRechts")

@app.route("/stop")
def stop():
    motor1.stop()
    motor2.stop()
     return redirect("/")

@app.route("/StatusVooruit")
def statusvrt():
    return render_template("statusvrt.html")

@app.route("/StatusAchteruit")
def statusact():
    return render_template("statusact.html")

@app.route("/StatusLinks")
def statuslnk():
    return render_template("statuslnk.html")

@app.route("/StatusRechts")
def statusrct():
    return render_template("statusrct.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
