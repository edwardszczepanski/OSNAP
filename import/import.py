import psycopg2, os, sys, csv, glob
from datetime import datetime

def main():
    connect()
    """
    for filename in glob.iglob(input + "*"):
        if "facilities" in filename:
            facilities(filename)
    for filename in glob.iglob(input + "*"):
        if "users" in filename:
            users(filename)
    for filename in glob.iglob(input + "*"):
        if "assets" in filename:
            assets(filename)
    """
    for filename in glob.iglob(input + "*"):
        if "transfers" in filename:
            transfers(filename)

            
def facilities(filename):
    reader = read(filename)
    head = next(reader)
    for row in reader:
        insert("facilities", ["fcode", "common_name", "location"], [row[0], row[1], row[0]])
    conn.commit()


def assets(filename):
    reader = read(filename)
    head = next(reader)
    for row in reader:
        insert("assets", ["asset_tag", "description"], [row[0], row[1]])
        cursor.execute("SELECT * FROM assets WHERE asset_tag = '" + row[0] + "';")
        asset_fk = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM facilities WHERE fcode = '" + row[2] + "';")
        facility_fk = cursor.fetchone()[0]
        arrive_dt = "NULL"
        depart_dt = "NULL"
        if row[3] != 'NULL':
            arrive_dt = str(datetime.strptime(row[3], '%Y-%m-%d'))
        if row[4] != 'NULL':
            depart_dt = str(datetime.strptime(row[4], '%Y-%m-%d'))
        insert("asset_at", ["asset_fk", "facility_fk", "arrive_dt", "depart_dt"], [asset_fk, facility_fk, arrive_dt, depart_dt])
    conn.commit()
        
def users(filename):
    reader = read(filename)
    head = next(reader)
    for row in reader:
        cursor.execute("SELECT * FROM roles WHERE title = '" + row[2] + "';")
        role_fk = cursor.fetchone()[0]
        insert("users", ["role_fk", "username", "password"], [role_fk, row[0], row[1]])
    conn.commit()


def transfers(filename):
    reader = read(filename)
    head = next(reader)
    for row in reader:
        cursor.execute("SELECT * FROM assets WHERE asset_tag = '" + row[0] + "';")
        asset_fk = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM users WHERE username = '" + row[1] + "';")
        user_fk = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM facilities WHERE fcode = '" + row[5] + "';")
        src_fk = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM facilities WHERE fcode = '" + row[6] + "';")
        dest_fk = cursor.fetchone()[0]
        request_dt = str(datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'))
        approve_dt = "NULL"
        approved = "FALSE"
        approve_user_fk = "NULL"
        if row[4] != 'NULL':
            approve_dt = str(datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'))
            cursor.execute("SELECT * FROM users WHERE username = '" + row[3] + "';")
            approve_user_fk = cursor.fetchone()[0]
            approved = "TRUE"
        insert("requests", ["asset_fk", "user_fk", "src_fk", "dest_fk", "request_dt", "approve_dt", "approve_user_fk", "approved"], [asset_fk, user_fk, src_fk, dest_fk, request_dt, approve_dt, approve_user_fk, approved])
        if row[4] != 'NULL':
            cursor.execute("SELECT * FROM requests WHERE asset_fk = " + str(asset_fk) + " AND user_fk=" + str(user_fk) + " AND src_fk=" + str(src_fk) + " AND dest_fk=" + str(dest_fk) + " AND request_dt='" + request_dt + "' AND approve_dt='" + approve_dt + "' AND approve_user_fk=" + str(approve_user_fk) + " AND approved='" + approved + "';")
            request_fk = cursor.fetchone()[0]
            load_dt = str(datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S'))
            unload_dt = str(datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S'))
            insert("in_transit", ["request_fk", "load_dt", "unload_dt"], [request_fk, load_dt, unload_dt])
    conn.commit()
            
            
def read(filename):
    return csv.reader(open(filename, newline=''), delimiter=',', quotechar='|')

def insert(table, columns, values):
    column_string = ','.join(columns)
    value_string = ""
    for i in range(len(values)):
        if type(values[i]) is str and values[i] != 'NULL':
            value_string += ("'" + values[i] + "'")
        else:
            value_string += (str(values[i]))
        if i != (len(values) - 1):
            value_string += ","
    string = "INSERT INTO {}({}) VALUES ({});".format(table, column_string, value_string)
    cursor.execute(string)

        #insert("requests", ["asset_fk", "user_fk", "src_fk", "dest_fk", "request_dt", "approve_dt", "approve_user_fk"], [asset_fk, ])
        #insert("in_transit", ["request_fk", "load_dt", "unload_dt"], [role_fk, row[0], row[1]])
            
            
def read(filename):
    return csv.reader(open(filename, newline=''), delimiter=',', quotechar='|')

def insert(table, columns, values):
    column_string = ','.join(columns)
    value_string = ""
    for i in range(len(values)):
        if type(values[i]) is str and values[i] != 'NULL':
            value_string += ("'" + values[i] + "'")
        else:
            value_string += (str(values[i]))
        if i != (len(values) - 1):
            value_string += ","
    string = "INSERT INTO {}({}) VALUES ({});".format(table, column_string, value_string)
    cursor.execute(string)

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
    global input
    if len(sys.argv) == 3:
        db_name = sys.argv[1]
        input = sys.argv[2]
    else:
        db_name = "lost"
        input = "./"
    main()
