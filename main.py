import RPi.GPIO as GPIO
from flask import Flask, render_template, redirect
import time

app = Flask(__name__)

@app.route("/")
def index():
    #Hierin kan je de setups van de GPIO pinnen zetten
    return render_template('index.html')

@app.route("/Vooruit")
def vooruit():
    #Hierin komt dus de GPIO, HIGH voor wanneer de knop 'vooruit' wordt ingedrukt
    return redirect("/StatusVooruit")

@app.route("/Achteruit")
def achteruit():
    #Hierin komt de GPIO, HIGH voor wanneer de knop 'achteruit' wordt ingedrukt
    return redirect("/StatusAchteruit")

@app.route("/Links")
def links():
    #Hierin komt de GPIO, HIGH voor wanneer de knop 'links' wordt ingedrukt
    return redirect("/StatusLinks")

@app.route("/Rechts")
def rechts():
    #Hierin komt de GPIO, HIGH voor wanneer de knop 'rechts' wordt ingedrukt
    return redirect("/")

@app.route("/StatusVooruit")
def statusvrt():
    #De html pagina waarin de geupdate status staat
    return render_template("statusvrt.html")

@app.route("/StatusAchteruit")
def statusact():
    #De html pagina waarin de geupdate status staat
    return render_template("statusact.html")

@app.route("/StatusLinks")
def statuslnk():
    #De html pagina waarin de geupdate status staat
    return render_template("statuslnk.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
