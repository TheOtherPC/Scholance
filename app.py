import json
from xml.dom.pulldom import SAX2DOM
from random import randint
from flask import (Flask, render_template, request,
                   redirect, session, flash, url_for)
import random

import dynamo
import models
from datetime import datetime

app = Flask(__name__)
app.secret_key = "SECRET"

user = None
customer = None


@app.route('/')
def index():
    if user is None:
        exit
    else:
        if 'user' in session and session['user'] == user.username:
            return redirect(url_for("dashboard"))
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

            return redirect(url_for("dashboard"))
        print("Incorrect Login")
        return "<h1>Incorrect Login</h1>"
    return render_template("login.html")


@app.route("/projects_check")
def projects_check():
    table = dynamo.get_projects_table()
    items = table.scan()['Items']
    from pprint import pprint
    pprint(items)
    return f"Projects: {items}"


@app.route('/dashboard')
def dashboard():
    if user is None:
        exit
    else:
        if 'user' in session and session['user'] == user.username:
            statement = ""
            customer_projects = False
            user_projects = False
            try:  # (i created an account to test btw, i didn't use "something" or wtv)
                customer.projects
            except Exception as e:  # 'NoneType' object has no attribute 'projects'
                print("EXCEPTION")
                print(e)
                statement += "Activate Customer Account "
            else:
                if not customer.projects:
                    statement += "No Owned Projects "
                else:
                    customer_projects = True
            try:
                user.projects
            except Exception as e:  # 'User' object has no attribute 'projects'
                print("EXCEPTION")
                print(e)
                statement += "Activate Employee Account "
            else:
                if not user.projects:
                    statement += "No projects"
                else:
                    user_projects = True

            if customer_projects and user_projects:
                projects_urls = [x.lower().replace(" ", "-") for x in user.projects]
                projects_dict = dict(zip(user.projects, projects_urls))
                print(str(user.projects) + "user projects")
                cprojects_urls = [x.lower().replace(" ", "-") for x in customer.projects]
                cprojects_dict = dict(zip(customer.projects, cprojects_urls))
                return render_template("dashboard/dashboard.html", projects=user.projects, cprojects=cprojects_dict)
            elif customer_projects:
                print(str(user.projects) + "user projects")
                cprojects_urls = [x.lower().replace(" ", "-") for x in customer.projects]
                cprojects_dict = dict(zip(customer.projects, cprojects_urls))
                return render_template("dashboard/dashboard.html", cprojects=cprojects_dict)
            elif user_projects:
                projects_urls = [x.lower().replace(" ", "-") for x in user.projects]
                projects_dict = dict(zip(user.projects, projects_urls))
                print(str(user.projects) + "user projects")
                return render_template("dashboard/dashboard.html", projects=user.projects)
            else:
                return render_template("dashboard/dashboard.html", statement=statement)

    flash("You are not logged in!", "error")
    return redirect(url_for("login"))


@app.route("/dashboard/<project>")
def dashboard_project_page(project):
    table = dynamo.get_projects_table()
    data = table.scan()['Items']
    for project_data in data:
        if project_data["info"]["project_url"] == project:
            return render_template("/dashboard/dashboard-project.html", project_data=project_data)


@app.route("/dashboard/<project>/<username>/accept")
def accept_project_user(project, username):
    table = dynamo.get_projects_table()
    data = table.scan()['Items']
    for project_data in data:
        if project_data["info"]["project_url"] == project:
            dynamo.update_user(username, "employee.projects", project_data["project_name"])
            flash("New employee recruited!", "info")
            return redirect("/dashboard")
    flash("Error in adding employee", "error")
    return redirect("/dashboard")


@app.route("/projects/post", methods=["POST", "GET"])
def postjob():
    if customer is None:
        flash("Need to Active Account", "error")
        exit
    else:
        if 'user' in session and session['user'] == customer.username:
            if request.method == "POST":
                project_url = request.form.get("project_name").lower()
                project_url = project_url.replace(" ", "-")
                description = request.form.get("description")

                if request.form.get("payment"):
                    payment = "$" + request.form.get("payment")
                else:
                    payment = request.form.get("volunteer_hours") + " hrs"

                project = models.Project(request.form.get("project_name"), request.form.get("size"), description[0:425],
                                         description, customer,
                                         payment, False, False, project_url)
                print("about to put project into dynamo")
                dynamo.put_project(project)
                print("project into dynamo")
                cust = dynamo.get_user(customer.username)['customer']['projects']
                cust.append(request.form.get("project_name"))
                dynamo.update_user(customer.username, "customer.projects", cust)
                print(cust)
                print("<-- Cust")
                flash("project posted successfully!", "info")
                return redirect(request.url)
            else:
                print("not a post method")
        else:
            flash("Not logged in!")
            return redirect(url_for("login"))
    return render_template("projects/post-project.html")


@app.route('/logout')
def logout():
    session.pop("user")
    return redirect(url_for("index"))


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
            return redirect(url_for("login"))
        return "<h1>Username Taken</h1>"
    return render_template("signup.html")


@app.route('/profile/user', methods=["POST", "GET"])
def user_profile():
    school = ""
    if request.method == "POST":
        dynamo.update_user(user.username, "info.email", request.form.get("email"))
        dynamo.update_user(user.username, "employee.school", request.form.get("school"))
        flash("Updated user profile!", "info")
        return redirect(request.url)
    try:
        user.school
    except Exception as e:
        print(e)
    else:
        school = user.school
    return render_template("profile/user-profile.html", username=user.username, email=user.email, school=user.school)


@app.route('/profile/business')
def business_profile():
    business = ""
    phone= ""
    if request.method == "POST":
        dynamo.update_user(user.username, "customer.business", request.form.get("business"))
        dynamo.update_user(user.username, "customer.phone", request.form.get("phone"))
        flash("Updated business profile!", "info")
        return redirect(request.url)
    if customer is None:
        exit
    else:
        business = customer.business
        phone = customer.phone_number
    return render_template("profile/business-profile.html", business=business, phone=phone)


@app.route('/profile/password')
def password():
    return render_template("profile/password.html")


@app.route("/projects")
def projects():
    table = dynamo.get_projects_table()
    data = table.scan()['Items']
    return render_template("projects/projects.html", data=data, data_length=len(data))


@app.route("/projects/logout")
def bs_function():
    return redirect(url_for("logout"))


@app.route("/projects/<project>")
def project_page(project):
    table = dynamo.get_projects_table()
    data = table.scan()['Items']
    print(data)
    for project_data in data:
        if project_data["info"]["project_url"] == project:
            return render_template("/projects/project-page.html", project_data=project_data)
    return "<h1>Project Not Found!</h1>"


@app.route("/projects/<project>/apply", methods=["POST", "GET"])
def apply_for_project(project):
    projects = dynamo.scan_projects("project_url")
    print("Projects:")
    for i, p in enumerate(projects):
        p_url = projects[i]["info"]["project_url"]
        if p_url == project:
            pn = projects[i]["project_name"]
            p = dynamo.get_project(pn)
            print(p)
            pa = p["info"]['applications']
            pa.append(user.username)
            dynamo.update_project(pn, "applications",
                                  pa)  # should be under info and then applications but don't change for now
        else:
            print("p_url != project")
    return "<h1>Applied</h1>"


if __name__ == '__main__':
    app.run(debug=True, port=6969)
