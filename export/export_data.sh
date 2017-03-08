#! /bin/bash
db_name=$1
output=$2

python3 migration.py $db_name
mkdir --parents $2; mv *.csv $_

