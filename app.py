import json

from flask import (Flask, render_template, request, redirect, session, flash)
import random

#import dynamo
#import models

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
        '''result = dynamo.query_employees(username)[0]
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
        return "<h1>Incorrect Login</h1>"'''
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user")
    return redirect("/login")

@app.route('/profile/user')
def user_profile():
    return render_template("profile/user-profile.html")

@app.route('/profile/business')
def business_profile():
    return render_template("profile/business-profile.html")

@app.route('/profile/password')
def password():
    return render_template("profile/password.html")

@app.route("/projects")
def projects():
    return render_template("projects/projects.html")

@app.route("/projects/post", methods=["POST", "GET"])
def postjob():
    if request.method == "POST":
        flash("Project posted successfully!", "info")
        return redirect(request.url)
    return render_template("projects/post-project.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/dashboard.html")


@app.route('/signup', methods=["POST", "GET"])
def signup():
    return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True, port=6969)
