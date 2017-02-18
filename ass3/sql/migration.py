import psycopg2, os, sys, csv, glob
from random import randint

def main():
    connect()
    dir = os.getcwd() + "/osnap_legacy/"
    for filename in glob.iglob(dir + "*.csv"):
        if "inventory" in filename:
            name = filename.split('/')[-1].split('_')[0]
            insert("facilities", ["fcode", "common_name", "location"], [name, name, name])
            cursor.execute("SELECT facility_pk FROM facilities WHERE fcode = '" + name + "';")
            facility_pk = cursor.fetchone()[0]
            inventory(filename, facility_pk)
    conn.commit()

def inventory(filename, facility_fk):
    reader = read(filename)
    head = next(reader)
    for row in reader:
        insert("assets", ["asset_tag", "description"], [row[0], row[2]])
        cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag = '" + row[0] + "';")
        asset_fk = cursor.fetchone()[0]
        insert("asset_at", ["asset_fk", "facility_fk"], [asset_fk, facility_fk])

def read(filename):
    return csv.reader(open(filename, newline=''), delimiter=',', quotechar='|')

def insert(table, columns, values):
    column_string = ','.join(columns)
    value_string = ""
    for i in range(len(values)):
        if type(values[i]) is str:
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
