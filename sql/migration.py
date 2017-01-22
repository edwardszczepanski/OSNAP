import psycopg2, os, sys, csv, glob

db_name = "lost"
port = "5432"
cursor = None

def main():
    connect()
    dir = os.getcwd() + "/osnap_legacy/"
    for filename in glob.iglob(dir + "*.csv"):
        if "product_list" in filename:
            product_list(filename)

def product_list(filename):
    print("In product list")
    reader = csv.reader(open(filename, newline=''), delimiter=' ', quotechar='|')
    first = True
    for row in reader:
        if first: first = False
        else:
            insert("products", ["product_pk", "vendor", "description", "alt_description"], [gen_pk(row[0]), row[3], row[2], row[1]])
    cursor.execute("INSERT INTO {}({}) VALUES ({})".format(table, ', '.join(columns), ', '.join(values)))

def gen_pk(string):
    return abs(hash(string)) % (10 ** 8)

def insert(table, columns, values):
    print(table)
    print(columns)
    print(values)
    cursor.execute("INSERT INTO {}({}) VALUES ({})".format(table, ', '.join(columns), ', '.join(values)))

def connect():
    global cursor
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
    main()
