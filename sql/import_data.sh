#! /bin/bash
db_name = $1
port = $2

curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xvf osnap_legacy.tar.gz
rm ./osnap_legacy/.*.csv
# Do some cool stuff here
python3 migration.py $db_name $port > migration.sql
# echo "psql -f $db_name -f migration.sql"
rm -rf osnap_legacy
rm migration.sql
rm osnap_legacy.tar.gz
