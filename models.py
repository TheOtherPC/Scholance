class Team:
    def __init__(self, team_name, team_lead, team_members, customer):
        self.team_name = team_name
        self.team_lead = team_lead
        self.team_members = team_members
        self.customer = customer


class User:
    def __init__(self, uid, email, username, password, school, team):
        self.uid = uid
        self.email = email
        self.username = username
        self.password = password
        self.school = school
        self.team = team


class TeamLead(User):
    def __init__(self, is_temp):
        self.is_temp = is_temp

    def kickTeam(self, uid):
        # kick another user off team
        print("Filler")

    def joinTeam(self, uid):
        # join another user to team
        print("Filler")


class Admin(TeamLead):
    def demoteTeamLead(self, uid):
        # demote another user from TeamLead to User
        print("Filler")

    def upgradeUser(self, uid):
        # upgrade another user from User to TeamLead
        print("Filler")

    def fireUser(self, uid):
        # fire/delete user
        print("Filler")

    def createTeam(self, team_name, team_lead, team_members, customer):
        new_team = Team(team_name, team_lead, team_members, customer)
        # creates new team with assigned values
class Dolphin(Admin):
    def demoteAdmin(self, uid):
        # demote another admin to Team Lead or User
        print("Filler")

    def upgradeUser(self, uid):
        # upgrade Team Lead  or User to Admin
        print("Filler")

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
