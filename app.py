import json

from flask import (Flask, render_template, request, redirect, session)
import random

import dynamo
import models

app = Flask(__name__)
app.secret_key = "SECRET"

user = None

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        result = dynamo.query_employees(username)[0]
        print(result)
        global user
        if password == result['info']['password']:
            if result['info']['level'] == "base_user":
                user = models.User(result['username'], result['info']['email'], result['info']['password'],
                                   result['info']['first_name'], result['info']['last_name'], result['info']['school'],
                                   result['info']['team'], result['info']['level'])
            elif result['info']['level'] == "team_lead":
                user = models.TeamLead(result['username'], result['info']['email'], result['info']['password'],
                                       result['info']['first_name'], result['info']['last_name'],
                                       result['info']['school'],
                                       result['info']['team'], result['info']['level'])
            elif result['info']['level'] == "admin":
                user = models.Admin(result['username'], result['info']['email'], result['info']['password'],
                                    result['info']['first_name'], result['info']['last_name'], result['info']['school'],
                                    result['info']['team'], result['info']['level'])
            else:
                user = models.Dolphin(result['username'], result['info']['email'], result['info']['password'],
                                      result['info']['first_name'], result['info']['last_name'],
                                      result['info']['school'],
                                      result['info']['team'], result['info']['level'])

            session['user'] = user.username
            return redirect('/dashboard')
        return "<h1>Incorrect Login</h1>"
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if user is None:
        exit
    else:
        if 'user' in session and session['user'] == user.username:
            return "<h1>Dashboard</h1>"
    return "<h1>Not Logged In</h1>"


@app.route('/logout')
def logout():
    session.pop("user")
    return redirect("/login")


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        new_user = models.User(request.form.get("username"), "NULL", request.form.get("password"),
                               request.form.get("first_name"), request.form.get("last_name"), request.form.get("school")
                               , "NULL", "base_user")
        if not dynamo.query_employees(new_user.username):
            print(dynamo.put_employee(new_user))
            return redirect('/login')
        return "<h1>Username Taken</h1>"
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)
