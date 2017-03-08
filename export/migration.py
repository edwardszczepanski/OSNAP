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
    with open('transfers.csv', 'w', newline='\n') as csvfile:
        mywriter = csv.writer(csvfile, quotechar="'", quoting=csv.QUOTE_MINIMAL)
        mywriter.writerow(['asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt'])
        cursor.execute("SELECT * FROM requests;")
        response = cursor.fetchall()
        for entry in response:
            cursor.execute("SELECT * FROM assets WHERE asset_pk=" + str(entry[1]) + ";")
            asset_tag = cursor.fetchone()[1]
            cursor.execute("SELECT * FROM users WHERE user_pk=" + str(entry[2]) + ";")
            request_by = cursor.fetchone()[2]
            request_dt = str(entry[5].strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute("SELECT * FROM facilities WHERE facility_pk=" + str(entry[3]) + ";")
            source = cursor.fetchone()[2]
            cursor.execute("SELECT * FROM facilities WHERE facility_pk=" + str(entry[4]) + ";")
            destination = cursor.fetchone()[2]
            # Below are the approved ones
            approve_dt = "NULL"
            if entry[6] != None:
                approve_dt = str(entry[6].strftime('%Y-%m-%d %H:%M:%S'))
            approve_by = "NULL"
            if entry[8] != None:
                cursor.execute("SELECT * FROM users WHERE user_pk=" + str(entry[8]) + ";")
                approve_by = cursor.fetchone()[2]
            # These two queries are passed back and may not be complete
            load_dt = "NULL"
            unload_dt = "NULL"
            cursor.execute("SELECT * FROM in_transit WHERE request_fk=" + str(entry[0]) + ";")
            if len(cursor.fetchall()) > 0:
                cursor.execute("SELECT * FROM in_transit WHERE request_fk=" + str(entry[0]) + ";")
                load_dt = str(cursor.fetchone()[2].strftime('%Y-%m-%d %H:%M:%S'))
                cursor.execute("SELECT * FROM in_transit WHERE request_fk=" + str(entry[0]) + ";")
                unload_dt = str(cursor.fetchone()[3].strftime('%Y-%m-%d %H:%M:%S'))
            mywriter.writerow([asset_tag] + [request_by] + [request_dt] + [approve_by] + [approve_dt] + [source] + [destination] + [load_dt] + [unload_dt])

def connect():
    global cursor
    global conn
    connection_string = "host='localhost' port='" + "5432" + "' dbname='" + db_name + "' user='osnapdev' password='secret'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    work_mem = 2048
    cursor.execute('SET work_mem TO ' + str(work_mem))

if __name__ == '__main__':
    global db_name
    global port
    if len(sys.argv) == 2:
        db_name = sys.argv[1]
    else:
        db_name = "lost"
    main()
