from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_tables, Student

with open("rosters.json", "r") as f:
    import json
    rosters = json.load(f)

tables = make_tables([Student(x) for x in rosters["period_12"]], 6)
svg = make_slides(tables)
xml_string = ET.tostring(svg, encoding='unicode')

# Save the string to a file
with open('hello.svg', 'w') as f:
    f.write(xml_string)
    print(f"File '{f.name}' has been created.")