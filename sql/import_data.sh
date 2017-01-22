#! /bin/bash
db_name = $1
port = $2

curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xvf osnap_legacy.tar.gz
rm ./osnap_legacy/.*.csv
# Do some cool stuff here
python3 migration.py $db_name $port
rm -rf osnap_legacy
rm osnap_legacy.tar.gz
