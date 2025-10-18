from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_tables, Student
import csv
import json
from typing import Dict
from collections import defaultdict
from datetime import datetime
from hashlib import sha256


periods = [
    "period_12",
    "period_45",
    "period_78",
    "period_910"
]

def to_default_dict(d: Dict):
    output = defaultdict(lambda : d["default"])
    for k, v, in d.items():
         output[k] = v
    return output

with open("announcements.json", "r") as f:
    announcements = to_default_dict(json.load(f))

with open("agenda.json", "r") as f:
    agenda = to_default_dict(json.load(f))

with open("do_now.json", "r") as f:
    do_now = to_default_dict(json.load(f))


for period in periods:
    students = list()
    with open(f'rosters/{period}.csv', mode ='r')as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
                students.append(
                    Student(
                        name=row["first_name"],
                        preferential_seating=row["preferential_seating"].strip().lower()=='yes',
                        avoids=row["avoids"]
                    )
                )
    print(f"there are {len(students)} in {period}")
    doy = datetime.now().strftime("%b%d_%Y")
    tables = make_tables(students, 3, seed=doy)
    svg = make_slides(
        tables, 
        announcements=announcements[period],
        agenda = agenda[period],
        donows = do_now[period]
    )
    xml_string = ET.tostring(svg, encoding='unicode')

    # Save the string to a file
    with open(f'welcome_slide_{doy}_{period}.svg', 'w') as f:
        f.write(xml_string)
        print(f"File '{f.name}' has been created.")