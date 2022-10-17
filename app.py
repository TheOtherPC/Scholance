from flask import (Flask, render_template, request, redirect, session)
import random
import models

app = Flask(__name__)
app.secret_key = "SECRET"

user = {"username": "user", "password": "123"}
team_lead = {"username": "team lead", "password": "123"}
admin = {"username": "admin", "password": "123"}
dolphin = {"username": "dolphin", "password": "123"}


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if checkUser(username, password):
            session['user'] = username
            return redirect('/dashboard')
        return "<h1>Incorrect Login</h1>"
    return render_template("login.html")

@app.route('/profile', methods=["POST", "GET"])
def profile():
    return render_template("profile.html")

def checkUser(username, password):
    if (username == user['username'] and password == user['password']) or (
            username == team_lead['username'] and password == team_lead['password']) or (
            username == admin['username'] and password == admin['password']) or (
            username == dolphin['username'] and password == dolphin['password']):
        return True
    return False


def checkDashBoard():
    if 'user' in session and (session['user'] == user['username'] or session['user'] == team_lead['username'] or session['user'] == admin['username'] or session['user'] == dolphin['username']):
        return True
    return False


@app.route('/dashboard')
def dashboard():
    if checkDashBoard():
   # if 'user' in session and session['user'] == user['username']:
        return "<h1>Dashboard</h1>"
    return "<h1>Not Logged In</h1>"


@app.route('/logout')
def logout():
    session.pop("user")
    return redirect("/login")


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        new_user = models.User(random.randint(0, 999999), request.form.get("email"), request.form.get("username"),
                               request.form.get("password"), request.form.get("school"), "NULL")
        if new_user.username != user['username']:
            print("put new_user in mongo")
            return redirect('/login')
        return "<h1>Username Taken</h1>"
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(port=6969, debug=True)
