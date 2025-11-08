import streamlit as st
import json

def get_contact_title(contact):
    if contact["title"] is None:
        return "Mr" if contact["relation"] == "father" else "Mrs"
    else:
        return contact["title"]
    
def get_formal_contact_names(contacts):
    if len(contacts) == 0:
        raise ValueError("No contacts provided")
    if len(contacts) == 1:
        title = get_contact_title(contacts[0])
        return f"{title}  {contacts[0]["lastname"]}"
    if contacts[0]["lastname"] == contacts[1]["lastname"]:
        title1 = get_contact_title(contacts[0])
        title2 = get_contact_title(contacts[1])
        return f"{title1} and {title2} {contacts[0]['lastname']}"
    title1 = get_contact_title(contacts[0])
    title2 = get_contact_title(contacts[1])
    return f"{title1} {contacts[0]['lastname']} and {title2} {contacts[1]['lastname']}"


with open("students.json", "r") as f:
    students = json.load(f)

st.title("Student Contact Information and Email Generator")
selected_names = st.multiselect(
    "Select students to generate emails for:",
    options=[f"{s['firstname']} {s['lastname']}" for s in students],
)
selected_students = [s for s in students if f"{s['firstname']} {s['lastname']}" in selected_names]

st.header("Contact information for selected students")
if len(selected_students) > 0:
    for student in selected_students:
        st.subheader(f"{student['firstname']} {student['lastname']}")
        st.write(f"**Email:** {student.get('email', 'N/A')}")
        st.write(f"**Course:** {student.get('course', 'N/A')}")
        emails = [student["email"]]
        for g in student["contacts"]:
            emails.append(g["contact_email"])
        st.write("**Contacts Emails:**")
        st.code( ";".join(emails))


st.header("Generate email bodies")

default_template = """Hello Guardians,
  I posted the grades for the unit 2 test on Tuesday and Johnny scored a 1.  I would strongly encourage him to retake the test, as I have seen him do better work in class. The test was on proportional relationships (e.g. the relationship between time and distance for a car travelling 10 miles per hour).  Study material can be found on Google classroom.  The relvant postings are from October 3 to October 30.
    Would Johnny be able to retake the test on Thursday?"""

st.write("## Email body generator")
template = st.text_area("Email Template",value=default_template, height=200, key="template")
if st.button("Generate Emails"):
    if not template:
        st.error("Please enter an email template.")
    else:
        for student in selected_students:
            email_body = template
            email_body = email_body.replace("Guardians", get_formal_contact_names(student["contacts"]))
            email_body = email_body.replace("Johnny", student["firstname"])
            email_body = email_body.replace("him", "him" if student["gender"] == "M" else "her")
            email_body = email_body.replace("his", "his" if student["gender"] == "M" else "her")
            email_body = email_body.replace(" he ", " he " if student["gender"] == "M" else " she ") #TODO: handle non-binary (they/them/their)
            
            st.subheader(f"Email for {student['firstname']} {student['lastname']}") 
            st.write("**Contacts Emails:**")
            emails = [g["contact_email"] for g in student["contacts"]] + [student.get("email", "")]
            st.code( ";".join(emails))
            st.write("**Email Body:**") 
            st.code(email_body, language="text", wrap_lines=True)