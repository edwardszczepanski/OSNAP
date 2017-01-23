
create_tables.sql - This is the SQL file that creates the LOST postgres tables.
You can use it by running "psql $db_name -f create_tables.sql"

import_data.sh - This is a shell script that downloads all the legacy data. 
It deletes some hidden files, runs a python script and cleans up after itself.
Use: "./import_data.sh $db_name $port_number"

migration.py - Here is where the main migration happens. It uses psycopg2 to go 
through and pull in asset information into the Postgres database. It takes in 
two arguments that are passed in from the import_data script which are the db 
name and the port number.


