from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import config
import functions
import control_management
import multiprocessing

app = Flask(__name__)

app.secret_key = "TeamTechnoManTeam"
app.permanent_session_lifetime = timedelta(seconds=5)


def game_start(username):
    config.controls_inactive = False
    score = 0

    control_management.find_controller()
    controller = control_management.MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller_process = multiprocessing.Process(target=controller.listen(), name="Listen_to_controller")
    distance_check_process = \
        multiprocessing.Process(target=control_management.check_distance(), name="Check_car_distance")
    time_limit_reached_process = multiprocessing.Process(target=functions.countdown(config.game_time_length_sec))

    controller_process.start()
    time_limit_reached_process.start()
    distance_check_process.start()

    while True:
        if config.game_stop:
            functions.save_data(username, score)
            break

        functions.blue_send_msg(config.client_one_mac, config.client_one_port, config.is_inactive)
        functions.blue_send_msg(config.client_two_mac, config.client_two_port, config.is_active)



        functions.blue_send_msg(config.client_one_mac, config.client_one_port, config.is_active)
        functions.blue_send_msg(config.client_two_mac, config.client_two_port, config.is_inactive)


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
        game_process = multiprocessing.Process(target=game_start(user), name="game")

        if not game_process.is_alive():
            game_process.start()

        return render_template("user.html", user=user)
    else:
        flash("Uw tijd is afgelopen!")
        return redirect(url_for('login'))


@app.route("/score")
def score():
    return render_template("score.html")


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
