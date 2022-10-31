import dynamo
import datetime
from multipledispatch import dispatch
from datetime import datetime


class Team:
    def __init__(self, team_name, team_lead, team_members, project):
        self.team_name = team_name
        self.team_lead = team_lead
        self.team_members = team_members
        self.project = project


class User:
    def __init__(self, username, email, password, first_name, last_name):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class Employee(User):
    def __init__(self, username, email, password, first_name, last_name, level, school, teams, interests, skills,
                 projects):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.school = school
        self.teams = teams
        self.level = level
        self.projects = projects
        self.skills = skills
        self.interests = interests

    def changePassword(self, new_password):
        dynamo.update_user(self.username, "password", new_password)


class TeamLead(Employee):
    def kickTeam(self, other_user, team_name):
        user = dynamo.get_user(other_user)
        temp = user.teams
        temp = temp.remove(team_name)
        dynamo.update_user(other_user, "teams", temp)
        team = dynamo.get_team(team_name)
        temp = team.members
        temp = temp.remove(other_user)
        dynamo.update_team(team_name, "members", temp)

    def joinTeam(self, other_user, team_name):
        user = dynamo.get_user(other_user)
        temp = user.teams
        temp = temp.append(team_name)
        dynamo.update_user(other_user, "teams", temp)
        team = dynamo.get_team(team_name)
        temp = team.members
        temp = temp.append(other_user)
        dynamo.update_team(team_name, "members", temp)

    def getTeamsLead(self):
        response = dynamo.scan_teams("team_lead")


class Admin(TeamLead):
    def demoteTeamLead(self, other_user):
        dynamo.update_user(other_user, "level", "base_user")

    def upgradeTeamLead(self, other_user):
        dynamo.update_user(other_user, "level", "team_lead")

    def fireUser(self, other_user):
        dynamo.delete_user(other_user)

    def createTeam(self, team):
        dynamo.put_team(team)
        # creates new team with assigned values


class Dolphin(Admin):
    def demoteAdmin(self, other_user, new_level):
        dynamo.update_user(other_user, "level", new_level)

    def upgradeAdmin(self, other_user):
        dynamo.update_user(other_user, "level", "admin")


class Customer(User):
    def __init__(self, username, email, password, first_name, last_name, business, projects, phone_number):
        self.username = username
        self.email = email
        self.password = password
        self.business = business
        self.projects = projects
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def create_project(self, project):
        dynamo.put_project(project)


@dispatch(str, Team, str, str, str, str, str, Customer, str, bool, bool, str, list)
class Project:
   def __init__(self, project_name, team, size, preview, description, project_start, project_end, customer, payment,
                active,
                finished, project_url, applications):
       self.project_name = project_name
       self.workers = team
       self.project_start = project_start
       self.project_end = project_end
       self.customer = customer
       self.size = size
       self.description = description
       self.payment = payment
       self.active = active
       self.finished = finished
       self.preview = preview
       self.project_url = project_url
       self.applications = applications


@dispatch(str, Employee, str, str, str, str, str, Customer, str, bool, bool, bool, str, list)
class Project:
   def __init__(self, project_name, employee, size, preview, description, project_start, project_end, customer,
                payment, active,
                finished, project_url, applications):
       self.project_name = project_name
       self.workers = employee
       self.project_start = project_start
       self.project_end = project_end
       self.customer = customer
       self.size = size
       self.description = description
       self.payment = payment
       self.active = active
       self.finished = finished
       self.preview = preview
       self.project_url = project_url
       self.applications = applications


@dispatch(str, str, str, str, Customer, str, bool, bool, str)
class Project:
   def __init__(self, project_name, size, preview, description, customer, payment,
                active,
                finished, project_url):
       self.project_name = project_name
       self.workers = None
       self.project_start = datetime.now().strftime("%m%d%Y")
       self.project_end = None
       self.customer = customer
       self.size = size
       self.description = description
       self.payment = payment
       self.active = active
       self.finished = finished
       self.preview = preview
       self.project_url = project_url
       self.applications = ["hello"]

