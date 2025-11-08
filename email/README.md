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
 - [x] Get student emails in csv with names
 - [x] Put email data in the json structure
 
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


 Example email template
```
Hello Guardians,
  I posted the grades for the unit 2 test on Tuesday and Johnny scored a 1.  I would strongly encourage him to retake the test, as I have seen him do better work in class. The test was on proportional relationships (e.g. the relationship between time and distance for a car travelling 10 miles per hour).  Study material can be found on Google classroom.  The relvant postings are from October 3 to October 30.
    Would Johnny be able to retake the test on Thursday?
```
The words `Guardians`, `Johnny`, `him` would be replaced for each student.