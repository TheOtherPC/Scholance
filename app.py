import json
from xml.dom.pulldom import SAX2DOM
from random import randint
from flask import (Flask, render_template, request, redirect, session, flash)
import random
import projects_update

import dynamo
import models
from datetime import datetime

app = Flask(__name__)
app.secret_key = "SECRET"

user = None
customer = None


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    print("Logging In")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            flash("Username or password field empty", "error")
            return redirect(request.url)
        try:
            dynamo.query_users(username)[0]
        except IndexError:
            flash("Invalid username or password", "error")
            return redirect(request.url)
        else:
            result = dynamo.query_users(username)[0]
            print(result)
        global user
        global customer
        if password == result['info']['password']:
            if result['employee']['level'] == "base_user":
                user = models.Employee(result['username'], result['info']['email'], result['info']['password'],
                                       result['info']['first_name'], result['info']['last_name'],
                                       result['employee']['level'], result['employee']['school'],
                                       result['employee']['teams'], result['employee']['interests'],
                                       result['employee']['skills'], result['employee']['projects'])
            elif result['employee']['level'] == "team_lead":
                user = models.TeamLead(result['username'], result['info']['email'], result['info']['password'],
                                       result['info']['first_name'], result['info']['last_name'],
                                       result['employee']['level'], result['employee']['school'],
                                       result['employee']['teams'], result['employee']['interests'],
                                       result['employee']['skills'], result['employee']['projects'])
            elif result['employee']['level'] == "admin":
                user = models.Admin(result['username'], result['info']['email'], result['info']['password'],
                                    result['info']['first_name'], result['info']['last_name'],
                                    result['employee']['level'], result['employee']['school'],
                                    result['employee']['teams'], result['employee']['interests'],
                                    result['employee']['skills'], result['employee']['projects'])
            elif result['employee']['level'] == "dolphin":
                user = models.Dolphin(result['username'], result['info']['email'], result['info']['password'],
                                      result['info']['first_name'], result['info']['last_name'],
                                      result['employee']['level'], result['employee']['school'],
                                      result['employee']['teams'], result['employee']['interests'],
                                      result['employee']['skills'], result['employee']['projects'])
            else:
                user = models.User(result['username'], result['info']['email'], result['info']['password'],
                                   result['info']['first_name'], result['info']['last_name'])

            if result['customer']['business']:
                customer = models.Customer(result['username'], result['info']['email'], result['info']['password'],
                                           result['info']['first_name'], result['info']['last_name'],
                                           result['customer']['business'], result['customer']['projects'],
                                           result['customer']['phone_number'])

            session['user'] = user.username

            return redirect('/dashboard')
        print("Incorrect Login")
        return "<h1>Incorrect Login</h1>"
    return render_template("login.html")

@app.route("/projects_check")
def projects_check():
    table = dynamo.get_projects_table()
    items = table.scan()['Items']
    from pprint import pprint
    pprint(items)
    projects_update.update()
    return f"Projects: {items}"

@app.route('/dashboard')
def dashboard():
    if user is None:
        exit
    else:
        if 'user' in session and session['user'] == user.username:
            render_template("dashboard.html")
            temp = dynamo.scan_projects("skills")
            pproject = None
            if not temp:
                pproject = "No Potential Projects"
            else:
                pproject = []
                for i in temp:
                    result = len(set(temp[i]) & set(user.skills)) / float(len(set(temp[i]) | set(user.skills))) * 100
                    pproject.append(result)
                    pproject.sort()

            try:
                user.projects
            except Exception as e:
                print(e)
                return render_template("dashboard.html", projects="Need To Activate Account", pprojects=pproject)
            else:
                if not user.projects:
                    print(pproject)
                    return render_template("dashboard.html", projects="No Current Projects", pprojects=pproject)
                else:
                    return render_template("dashboard.html", projects=user.projects, pprojects=pproject)

    return "<h1>Not Logged In</h1>"


@app.route('/projects/post', methods=["POST", "GET"])
def projectPost():
    if request.method == "POST":
        #if customer is None:
        #    flash("Error: Not a verified customer", "info")
        #else:
        now = datetime.now()
        #interests = request.form.get("interests").split(",")
        #skills = request.form.get("skills").split(",")
        
        project = models.Project(f"project name {random.randint(0, 10)}", "Worker", "today",
                                    "TBD",  "n/a", "n/a", "n/a", "n/a", "n/a")
        dynamo.put_project(project)
        flash("Project posted successfully!", "info")
        projects_update.update()
        return redirect(request.url)
    return render_template("projects/post-project.html")

@app.route('/logout')
def logout():
    session.pop("user")
    return redirect("/login")


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        first_name = full_name.split(" ")[0]
        last_name = full_name.split(" ")[1]
        new_user = {'username': request.form.get("username"),
                    'info': {'email': request.form.get("email"), 'password': request.form.get("password"),
                             'first_name': first_name, 'last_name': last_name},
                    'employee': {'level': None, 'school': None, 'teams': [], 'interests': [], 'skills': [],
                                 'projects': []}, 'customer': {'business': None, 'projects': [], 'phone_number': None}}
        if not dynamo.query_users(new_user['username']):
            print(dynamo.put_user(new_user))
            return redirect('/login')
        return "<h1>Username Taken</h1>"
    return render_template("signup.html")

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
    # table = dynamo.get_projects_table()
    # data = table.scan()['Items']
    with open('projectsdata.json') as f:
        data = json.load(f)
    return render_template("projects/projects.html", data=data, data_length=len(data))

@app.route("/projects/post", methods=["post", "get"])
def postjob():
    if request.method == "post":
        flash("project posted successfully!", "info")
        return redirect(request.url)
    return render_template("projects/post-project.html")

@app.route("/projects/<project>")
def project_page(project):
    with open('projectsdata.json') as f:
        data = json.load(f)
    for project_data in data:
        if project_data["info"]["interests"] == project:
            return render_template("/projects/project-page.html", project_data=project_data)
    return "<h1>Project Not Found!</h1>"


if __name__ == '__main__':
    app.run(debug=True, port=6969)
