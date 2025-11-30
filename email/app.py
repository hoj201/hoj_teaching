import streamlit as st
import json

with open("students.json", "r") as f:
    students = json.load(f)

st.title("Student Email Directory")
search = st.text_input("Search by last name:", key="search")
if search:
    for student in students:
        if search.lower() in student["lastname"].lower():
            st.subheader(f"{student['firstname']} {student['lastname']}")
            st.write(f"**Email:** {student.get('email', 'N/A')}")
            st.write(f"**Course:** {student.get('course', 'N/A')}")
            emails = [student["email"]]
            for g in student["contacts"]:
                emails.append(g["contact_email"])
            st.write("**Contacts Emails:**")
            st.code( ";".join(emails))
