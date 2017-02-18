import psycopg2, os, sys, csv, glob
from random import randint
from datetime import datetime

def main():
    connect()
    dir = os.getcwd()
    reader = read(dir + "/ass3manualdata.csv")
    add_to_db(reader)
    conn.commit()

def add_to_db(reader):
    head = next(reader)
    for row in reader:
        columns = ["fcode", "asset_tag", "src_facility", "dest_facility", "arrive_date", "depart_date", "expunge_date"]
        rCols = []
        rVals = []
        for i in range(len(columns)):
            if  row[i]!= None and row[i] != "":
                rCols.append(columns[i])
                if i >= 4:
                    rVals.append(convert(row[i]))
                else:
                    rVals.append(row[i])
        insert("assets", rCols, rVals)

def convert(string):
    return datetime.strptime(string, '%m/%d/%Y')

def read(filename):
    return csv.reader(open(filename, newline=''), delimiter=',', quotechar='|')

def insert(table, columns, values):
    column_string = ','.join(columns)
    value_string = ""
    for i in range(len(values)):
        if type(values[i]) is str:
            value_string += ("'" + values[i] + "'")
        elif not type(values[i]) is int:
            value_string += "('" + str(values[i]) + "')"
        else:
            if values[i] != None:
                value_string += (str(values[i]))
        if i != (len(values) - 1):
            value_string += ","
    string = "INSERT INTO {}({}) VALUES ({});".format(table, column_string, value_string)
    print(string)
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
