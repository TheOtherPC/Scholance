import dynamo


class Team:
    def __init__(self, team_id, team_name, team_lead, team_members, customer):
        self.team_id = team_id
        self.team_name = team_name
        self.team_lead = team_lead
        self.team_members = team_members
        self.customer = customer


class User:
    def __init__(self, username, email, password, first_name, last_name, school, team, level):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.school = school
        self.team = team
        self.level = level

    def changePassword(self, new_password):
        dynamo.update_employee(self.username, "password", new_password)


class TeamLead(User):
    def kickTeam(self, other_user):
        dynamo.update_employee(other_user, "team", "NULL")

    def joinTeam(self, other_user, new_team):
        dynamo.update_employee(other_user, "team", new_team)


class Admin(TeamLead):
    def demoteTeamLead(self, other_user):
        dynamo.update_employee(other_user, "level", "base_user")

    def upgradeTeamLead(self, other_user):
        dynamo.update_employee(other_user, "level", "team_lead")

    def fireUser(self, other_user):
        dynamo.delete_user(other_user)

    def createTeam(self, team_name, team_lead, team_members, customer):
        new_team = Team(team_name, team_lead, team_members, customer)
        # creates new team with assigned values


class Dolphin(Admin):
    def demoteAdmin(self, other_user, new_level):
        dynamo.update_employee(other_user, "level", new_level)

    def upgradeAdmin(self, other_user):
        dynamo.update_employee(other_user, "level", "admin")


class Customer:
    def __init__(self, cid, email, username, password, project_start, project_end):
        self.cid = cid
        self.email = email
        self.username = username
        self.password = password
        self.project_start = project_start
        self.project_end = project_end

    def getStart(self):
        return self.project_start

    def getEnd(self):
        return self.project_end

