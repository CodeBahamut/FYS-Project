import RPi.GPIO as GPIO
from flask import Flask, render_template, redirect
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/Vooruit")
def vooruit():
    #Hierin komt dus de GPIO, HIGH voor wanneer de knop 'vooruit' wordt ingedrukt
    return redirect("/")

@app.route("/Achteruit")
def achteruit():
    #Hierin komt de GPIO, HIGH voor wanneer de knop 'achteruit' wordt ingedrukt
    return redirect("/")

@app.route("/Links")
def links():
    #Hierin komt de GPIO, HIGH voor wanneer de knop 'links' wordt ingedrukt
    return redirect("/")

@app.route("/Rechts")
def rechts():
    #Hierin komt de GPIO, HIGH voor wanneer de knop 'rechts' wordt ingedrukt
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
