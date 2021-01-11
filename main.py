from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from celery import Celery
from datetime import timedelta
import config
import functions
import control_management
from multiprocessing import Process

app = Flask(__name__)

app.secret_key = "TeamTechnoManTeam"
app.permanent_session_lifetime = timedelta(seconds=5)
app.config['MYSQL_HOST'] = config.db_host
app.config['MYSQL_USER'] = config.db_user
app.config['MYSQL_PASSWORD'] = config.db_password
app.config['MYSQL_DB'] = config.db_database
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

mysql = MySQL(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def game_start(username):
    config.controls_inactive = False
    game_score = 0

    control_management.find_controller()
    controller = control_management.MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller_process = Process(target=controller.listen(), name="Listen_to_controller")
    distance_check_process = Process(target=control_management.check_distance(), name="Check_car_distance")
    time_limit_reached_process = Process(target=functions.countdown(config.game_time_length_sec))

    controller_process.daemon = True
    time_limit_reached_process.daemon = True
    distance_check_process.daemon = True

    controller_process.start()
    controller_process.join()
    time_limit_reached_process.start()
    time_limit_reached_process.join()
    distance_check_process.start()
    distance_check_process.join()

    while True:
        if config.game_stop:
            cursor = mysql.cursor()
            sql = "INSERT INTO Fys (name, score) VALUES (%s, %s)"
            val = (username, game_score)

            cursor.execute(sql, val)
            mysql.commit()

            if controller_process.is_alive():
                controller_process.close()
            if time_limit_reached_process.is_alive():
                time_limit_reached_process.close()
            if distance_check_process.is_alive():
                distance_check_process.close()
            break

        functions.blue_send_msg(config.client_one_mac, config.client_one_port, config.is_inactive)
        functions.blue_send_msg(config.client_two_mac, config.client_two_port, config.is_active)

        game_score += functions.blue_receive_msg(config.client_two_mac, config.robot_port)

        functions.blue_send_msg(config.client_one_mac, config.client_one_port, config.is_active)
        functions.blue_send_msg(config.client_two_mac, config.client_two_port, config.is_inactive)

        game_score += functions.blue_receive_msg(config.client_one_mac, config.robot_port)


@app.route("/")
def index():
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
        game_start.delay(user)
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
    app.run(debug=True, host='0.0.0.0')
