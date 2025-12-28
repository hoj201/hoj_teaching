import streamlit as st
from crypt import get_database, upload_database
import sqlite3
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name='us-east-2'
)

# 1. Connect to a database (it creates the file if it doesn't exist)
#load_dotenv()
#key = os.getenv("SECRET_KEY").encode()
st.session_state.dbkey = st.text_input("Enter the encryption key:", type="password").encode("utf-8")
if "dbkey" in st.session_state and st.session_state.dbkey == st.secrets["DB_KEY"].encode("utf-8"):
    get_database(st.session_state.dbkey, s3_client=s3)
else:
    st.warning("Please enter the encryption key to access the database.")
    st.stop()

connection = sqlite3.connect('contacts.db')

st.title("Student Email Directory")
search_term = st.text_input("Search by student name:", key="search")
search_term = f"%{search_term}%"
if search_term and search_term != "%%":
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, firstname, lastname, nickname, email FROM students WHERE firstname LIKE ? OR lastname LIKE ?", 
        (search_term, search_term)
    )
    rows = cursor.fetchall()
    for row in rows:
        first, last, nick, email = row[1], row[2], row[3], row[4]
        st.write(f"{first} {last} ({nick}) - {email}")
        st.write("Student ID:", row[0])
        st.write("---")
        cursor.execute(
            """SELECT firstname, lastname, email, relationships.type, title
            FROM guardians JOIN relationships 
            ON guardians.id = relationships.guardian_id 
            WHERE student_id = ?""", 
            (row[0],)
        )
        g_rows = cursor.fetchall()
        guardian_emails = []
        full_guardian_names = []
        guardian_last_names = []
        for g_row in g_rows:
            g_first, g_last, g_email, type, title = g_row[0], g_row[1], g_row[2], g_row[3], g_row[4]
            st.write(f"Guardian: {title} {g_first} {g_last} ({type}) - {g_email}")
            st.write("---")
            full_guardian_names.append(f"{title} {g_last}")
            guardian_last_names.append(g_last)
            guardian_emails.append(g_email)

        st.code(",".join(guardian_emails+ [email]))
        if all(ln == guardian_last_names[0] for ln in guardian_last_names) and len(guardian_last_names) > 1:
            st.code("Hello " + guardian_last_names[0] + " family,")
        else:
            st.code("Hello " + " and ".join(full_guardian_names) + ",")

st.title("Add New Student")
with st.form("add_student_form"):
    firstname = st.text_input("First Name")
    lastname = st.text_input("Last Name")
    nickname = st.text_input("Nickname")
    pronouns = st.text_input("Pronouns")
    course = st.text_input("Course")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Add Student")
    if submitted:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO students (firstname, lastname, nickname, pronouns, course, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (firstname, lastname, nickname, pronouns, course, email))
        connection.commit()
        st.success(f"Added student {firstname} {lastname}.")

        upload_database("contacts.db", st.session_state.dbkey, s3_client=s3)
        st.info("Database uploaded and encrypted.")
    
st.title("Add Guardian Relationship")
with st.form("add_relationship_form"):
    student_id = st.number_input("Student ID", min_value=1, step=1)
    guardian_firstname = st.text_input("Guardian First Name")
    guardian_lastname = st.text_input("Guardian Last Name")
    guardian_title = st.text_input("Guardian Title (e.g., Mr., Ms., Dr.)")
    guardian_email = st.text_input("Guardian Email")
    relationship_type = st.text_input("Relationship Type (e.g., Parent, Guardian)")
    rel_submitted = st.form_submit_button("Add Relationship")
    if rel_submitted:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO guardians (firstname, lastname, title, email)
            VALUES (?, ?, ?, ?)
        ''', (guardian_firstname, guardian_lastname, guardian_title, guardian_email))
        guardian_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO relationships (student_id, guardian_id, type)
            VALUES (?, ?, ?)
        ''', (student_id, guardian_id, relationship_type))
        connection.commit()
        st.success(f"Added relationship for student ID {student_id}.")

        upload_database("contacts.db", st.session_state.dbkey)
        st.info("Database uploaded and encrypted.")

st.title("Delete Student")
with st.form("delete_student_form"):
    student_id = st.number_input("Student ID", min_value=0, step=1, value=9999)
    del_submitted = st.form_submit_button("Delete Student")
    if del_submitted:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        connection.commit()
        st.success(f"Deleted student with ID {student_id}.")

        upload_database("contacts.db", st.session_state.dbkey, s3_client=s3)
        st.info("Database uploaded and encrypted.")