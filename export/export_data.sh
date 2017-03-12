#! /bin/bash
db_name=$1
port=$2

python3 migration.py $db_name $port
