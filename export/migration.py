import psycopg2, os, sys, csv, glob
from random import randint

def main():
    connect()
    users()
    facilities()
    assets()
    transfers()

def users():
    with open('users.csv', 'w', newline='\n') as csvfile:
        mywriter = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
        mywriter.writerow(['username', 'password', 'role', 'active'])
        cursor.execute("SELECT * FROM users;")
        response = cursor.fetchall()
        for entry in response:
            username = entry[2]
            password = entry[3]
            active="TRUE"
            cursor.execute("SELECT * FROM roles WHERE role_pk=" + str(entry[1]) + ";")
            role = cursor.fetchone()[1]
            mywriter.writerow([username] + [password] + [role] + [active])

def facilities():
    with open('facilities.csv', 'w', newline='\n') as csvfile:
        mywriter = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
        mywriter.writerow(['fcode', 'common_name'])
        cursor.execute("SELECT * FROM facilities;")
        response = cursor.fetchall()
        for entry in response:
            fcode = entry[1]
            common_name = entry[2]
            mywriter.writerow([fcode] + [common_name])

def assets():
    with open('assets.csv', 'w', newline='\n') as csvfile:
        mywriter = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
        mywriter.writerow(['asset_tag', 'description', 'facility', 'acquired', 'disposed'])
        cursor.execute("SELECT * FROM assets;")
        response = cursor.fetchall()
        for entry in response:
            asset_tag = entry[1]
            description = entry[2]
            cursor.execute("SELECT * FROM asset_at WHERE asset_fk=" + str(entry[0]) + ";")
            asset_at = cursor.fetchone()
            facility_fk = str(asset_at[0])
            cursor.execute("SELECT * FROM facilities WHERE facility_pk=" + facility_fk + ";")
            facility = cursor.fetchone()[2]
            acquired = str(asset_at[2].strftime('%Y-%m-%d'))
            disposed = "NULL"
            if asset_at[3] != None:
                disposed = str(asset_at[3].strftime('%Y-%m-%d'))
            mywriter.writerow([asset_tag] + [description] + [facility] + [acquired] + [disposed])

def transfers():
    with open('facilities.csv', 'w', newline='\n') as csvfile:
        mywriter = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
        mywriter.writerow(['fcode', 'common_name'])
        cursor.execute("SELECT * FROM facilities;")
        response = cursor.fetchall()
        for entry in response:
            fcode = entry[1]
            common_name = entry[2]
            mywriter.writerow([fcode] + [common_name])

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
