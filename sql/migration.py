import psycopg2, os, sys

db_name = "lost"
port = 2222

def main():
    #connection_string = "host='127.0.0.1' port='" + port + "' dbname='" + db_name + "' user='osnapdev' password='CIS322image'"
    connection_string = "host='localhost' port='5432' dbname='" + db_name + "' user='osnapdev' password='secret'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    print("Connected!")
    cursor.execute("SELECT * FROM products")
    records = cursor.fetchall()
    print(records)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        db_name = sys.argv[1]
        port = sys.argv[2]
    main()
