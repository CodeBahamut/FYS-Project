from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from celery import Celery
from datetime import timedelta
import config
import functions
import control_management
import  main
from multiprocessing import Process

app = Flask(__name__)

app.secret_key = "TeamTechnoManTeam"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['MYSQL_HOST'] = config.db_host
app.config['MYSQL_USER'] = config.db_user
app.config['MYSQL_PASSWORD'] = config.db_password
app.config['MYSQL_DB'] = config.db_database
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

mysql = MySQL(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route("/")
def index():
    functions.MySocket.connect(config.robot_ip, config.robot_port)
    return redirect('login')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        game_start_process = Process(target=main.game_start, args=user)
        return render_template("user.html", user=user)
    else:
        flash("Uw tijd is afgelopen!")
        return redirect(url_for('login'))


@app.route("/score")
def score():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM `Fys`")

    data = cursor.fetchall()
    return render_template("score.html", data=data)


@app.route("/test")
def test():
    return render_template("index.html")


@app.route("/logout")
def logout():
    flash("Uw tijd is afgelopen!")
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
