import sqlite3

# 1. Connect to a database (it creates the file if it doesn't exist)
connection = sqlite3.connect('contacts.db')

# 2. Create a "cursor" (this is what executes the SQL commands)
cursor = connection.cursor()

# 3. Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        nickname TEXT,
        pronouns TEXT,
        course TEXT,
        email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS guardians (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT,
        lastname TEXT NOT NULL,
        title TEXT,
        email TEXT
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        guardian_id INTEGER,
        type TEXT,
        foreign key(student_id) REFERENCES students(id) ON DELETE CASCADE,
        foreign key(guardian_id) REFERENCES guardians(id) ON DELETE CASCADE
    )'''
)

# 4. Add recoreds
with open("students.json", "r") as f:
    import json
    students = json.load(f)
    for student in students:
        cursor.execute('''
            INSERT INTO students (firstname, lastname, nickname, pronouns, course, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            student.get("firstname"),
            student.get("lastname"),
            student.get("nickname"),
            student.get("pronouns"),
            student.get("course"),
            student.get("email")
        ))
        student_id = cursor.lastrowid
        for guardian in student.get("contacts", []):
            print(guardian)
            cursor.execute('''
                INSERT INTO guardians (firstname, lastname, title, email)
                VALUES (?, ?, ?, ?)
            ''', (
                guardian.get("firstname"),
                guardian.get("lastname"),
                guardian.get("title"),
                guardian.get("contact_email")
            ))
            guardian_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO relationships (student_id, guardian_id, type)
                VALUES (?, ?, ?)
            ''', (
                student_id,
                guardian_id,
                guardian.get("relationship")
            ))  

# 5. Save (commit) your changes
connection.commit()

# 6. Close the connection
connection.close()
print("Database created and records added!")