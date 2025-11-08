from csv import DictReader
import re
#raise Exception("I do not want this script to be run accidentally")
with open("./fixtures/studentEmails.txt", "r") as f:
    doc = f.read()

student_email_addresses = [x.strip() for x in doc.split(";")]
name2gender = {}
with open("./fixtures/studentGender.csv", "r") as f:
    reader = DictReader(f, fieldnames=["Name", "Gender"])
    for row in reader:
        name2gender[row["Name"].lower()] = row["Gender"]

students = []
with open("./fixtures/parentEmails.csv", "r") as f:
    reader = DictReader(f, fieldnames=["Name", "Contact Name", "Contact Email", "Course"], quotechar='"', delimiter=";")
    for row in reader:
        if row["Name"] != "":
            try:
                lastname, firstname = row["Name"].split(",")
            except ValueError:
                print("Could not parse name:", row["Name"])
                continue
            student = {
                "firstname": firstname.strip().replace('"', ''),
                "lastname": lastname.strip().replace('"', ''),
                "contacts": [],
                "course": row["Course"],
                "gender": name2gender.get(row["Name"].lower(), None)
            }
            students.append(student)
        else:
            lastname = re.search(r"([^,]+),", row["Contact Name"]).group(1).strip()
            title = re.search(r"^([^\s]+)\.", lastname)
            if title is not None:
                title = title.group(1)
                lastname = lastname.removeprefix(title).strip().removeprefix(".").strip()
            contact = {
                "relation" : re.search(r"\(([^)]*)\)", row["Contact Name"]).group(1).lower(),
                "title": title,
                "firstname": re.search(r", (.*?) \(", row["Contact Name"]).group(1),
                "lastname": lastname,
                "contact_name": row["Contact Name"],
                "contact_email": row["Contact Email"].removesuffix(" (Current - Primary)").strip().lower()
            }
            student["contacts"].append(contact)



for student in students:
    lastname = student["lastname"].lower().strip()
    student_email = [x for x in student_email_addresses if lastname in x]
    if student_email:
        student_email = student_email[0]
    else:
        student_email = None
    student["email"] = student_email
    print(student_email)

with open("students.json", "w") as f:
    import json
    json.dump(students, f, indent=4)