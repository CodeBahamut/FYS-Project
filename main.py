from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import config
import functions
import control_management
import threading

app = Flask(__name__)


app.secret_key = "TeamTechnoManTeam"
app.permanent_session_lifetime = timedelta(seconds=5)


def game_start(user):
    control_management.find_controller()
    controller = control_management.MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller_thread = threading.Thread(target=controller.listen(), name="Listen_to_controller", args="")
    controller_thread.start()

    functions.blue_send_msg(config.client_one_mac, config.client_one_port, "t")
    functions.blue_send_msg(config.client_two_mac, config.client_two_port, "f")

    time_limit_reached = functions.countdown(config.game_time_length_sec)


    while True:
        if time_limit_reached:
            controller.stop
            break


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
        game_thread = threading.Thread(target=game_start(user), name="game", args="")

        if not game_thread.is_alive():
            game_thread.start()

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
