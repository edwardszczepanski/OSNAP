import psycopg2, os, sys, csv, glob
from random import randint

def main():
    connect()
    users()
    facilities()
    assets()
    transfers()

def users():
    cursor.execute("SELECT * FROM users;")
    response = cursor.fetchall()

    with open('eggs.csv', 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    return

def facilities():
    return

def assets():
    return

def transfers():
    return

def connect():
    global cursor
    global conn
    connection_string = "host='localhost' port='" + port + "' dbname='" + db_name + "' user='osnapdev' password='secret'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    work_mem = 2048
    cursor.execute('SET work_mem TO ' + str(work_mem))

if __name__ == '__main__':
    global db_name
    global port
    if len(sys.argv) == 3:
        db_name = sys.argv[1]
        port = sys.argv[2]
    else:
        db_name = "lost"
        port = "5432"
    main()
