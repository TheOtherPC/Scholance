import dynamo
import json

def update():
    table = dynamo.get_projects_table()
    data = table.scan()['Items']
    json_data = json.dumps(data)

    with open("projectsdata.json", "w") as f:
        f.write(json_data)