For my testing I am not using WSGI and instead am running the application by directly running the app.py file
Please go to 0.0.0.0:8080 to test the application!!!

app.py - Run this file to start execution. It takes in an argument which is the database name, but will default to 'lost' if no argument is provided. This file has all my business logic, builds SQL queries, and provides the correct .html files for the user. 

static/* - I use bootstrap for my application so I have many bootstrap files here. I also have a styles.css file which does not seem to be actually affecting my web app... I'll find to debug that.

templates/* - I have a layout.html file which is based off the one provided in the Flaskr tutorial. This was great as I didn't have to copy all the details to my child pages and it made it super modular. Login and Logout are pretty self explanatory. Report_filter users input boxes of different types to get dates and specific facilities and sends them to the backend. Originally I had two different reports pages but I consolidated them into one and my reports.html simply takes in the session input and creates table entries for me.

../sql/ass3_create_tables.sql - My custom, simple DB schema for this assignment

../sql/ass3_inserts.sql - My script that puts these files into the db.

../sql/ass3manualdata.csv - Data I compiled manually from looking at the input csv files and what was needed

../sql/ass3_migration.csv - My overcomplicated script that took way too long that takes the manual data csv and generated the ass3_inserts.sql file

../preflight.sh - Simple shell script that just runs the sql scripts. It requires 1 argument which is the DB name


