from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_tables, Student
import csv

students = list()
with open('period_12.csv', mode ='r')as file:
  csvFile = csv.DictReader(file)
  for row in csvFile:
        students.append(
            Student(
                name=row["first_name"],
                preferential_seating=row["preferential_seating"].strip().lower()=='yes'
            )
        )

tables = make_tables(students, 7)
svg = make_slides(
    tables, 
    announcements=["test"],
    agenda_items = ["item1", "item2"])
xml_string = ET.tostring(svg, encoding='unicode')

# Save the string to a file
with open('hello.svg', 'w') as f:
    f.write(xml_string)
    print(f"File '{f.name}' has been created.")