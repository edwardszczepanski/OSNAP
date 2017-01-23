import psycopg2, os, sys, csv, glob
from random import randint

def main():
    connect()
    dir = os.getcwd() + "/osnap_legacy/"
    for filename in glob.iglob(dir + "*.csv"):
        if "product_list" in filename:
            product_list(filename)
        elif "inventory" in filename:
            inventory(filename)
    conn.commit()


def inventory(filename):
    reader = read(filename)
    head = next(reader)
    for row in reader:
        # Search products for the row[1]. Use that primary key as the product_key, if generate 1.
        insert("assets", ["asset_pk", "asset_tag", "description"], [gen_pk(), row[0], row[2]])

def product_list(filename):
    reader = read(filename)
    head = next(reader)
    for row in reader:
        insert("products", ["product_pk", "vendor", "description", "alt_description"], [gen_pk(), row[3], row[2], row[1]])

def read(filename):
    return csv.reader(open(filename, newline=''), delimiter=',', quotechar='|')


def gen_pk():
    range_start = 10**(8-1)
    range_end = (10**8)-1
    return randint(range_start, range_end)
    #return abs(hash(string)) % (10 ** 8)

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


def demo():
    cursor.execute("SELECT * FROM products")
    records = cursor.fetchall()
    print(records)

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
