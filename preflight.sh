#! /bin/bash
psql $1 -f ./sql/ass3_create_tables.sql
psql $1 -f ./sql/ass3inserts.sql
