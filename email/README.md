# Description
An app for sending mass emails to my class

Desired Features:
 - Toggle for including parents
 - Email templates to insert student name, parent name, section, in appropriate places
 - Automatically default to BCC when multiple families are involved.
 - Select students by section and then individually
 - Select all students in section toggle
 - Prohibit sending one-off emails
 - Review emails before sending


 TODO:
 - [ ] Get student emails in csv with names
 - [ ] Put email data in the json structure
 ```json
{
    "lastname": "Ochoa",
    "firstname": "Alex",
    "email": "27abcdefg@district44.com",
    "section": "34",
    "pronouns": "she/her"
    "guardians": [
        {
            "title":"Mr.",
            "firstname": "Allan",
            "lastname": "Ochoa",
            "relation": "Father",
            "email": "adfads@gmail.com"
        },
        {
            "title":"Mrs.",
            "firstname": "Mallory",
            "lastname": "Ochoa",
            "relation": "Mother",
            "email": "asdfasdf@yahoo.com"
        }
    ]
}
 ```


 ## Notes
 The file `students.json` is generated from `process_email_files.py`.  However, there are a few errors (check Alina's record + records for students with the same last name + for null genders)