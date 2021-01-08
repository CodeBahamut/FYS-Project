from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import config
import functions
import control_management
import time

app = Flask(__name__)


app.secret_key = "TeamTechnoManTeam"
app.permanent_session_lifetime = timedelta(seconds=5)


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



def game_start():
    NotImplemented


functions.find_controller()

controller = control_management.MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
game_start()
controller.listen()


