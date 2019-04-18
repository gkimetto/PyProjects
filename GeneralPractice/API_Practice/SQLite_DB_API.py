import sqlite3

print("Connecting to the database: ")
db = sqlite3.connect('db-api.db')
cur = db.cursor()   
 
def add_decor(func):
    print("*-*"*20+"\n")
    func()
    print("=^="*20)
    
@add_decor
def create_table_in_db():
    print('Create table in the database: ')
    cur.execute("DROP TABLE IF EXISTS test")
    cur.execute("""
        CREATE TABLE test(
           id INTEGER PRIMARY KEY, string  TEXT, number INTEGER
           )
           """)
    print('Committing Data to the database. ')
    db.commit()

@add_decor    
def add_data_to_db_table():
    print("Inserting data into the database ") 
    cur.execute("""
        INSERT INTO test (string, number) VALUES ('one', 1)""")
    cur.execute("""
        INSERT INTO test (string, number) VALUES ('two', 2)""")
    cur.execute("""INSERT INTO test (string, number) VALUES ('three', 3)""")
    print('Committing Data to the database. ')
    db.commit()
    
@add_decor    
def count_no_of_rows():
    print("Counting the number of rows....")
    
    cur.execute("SELECT COUNT(*) from test")
    count = cur.fetchone()[0]
    print("There are {} rows in the table.".format(count) )
    print('Reading the table. ')
    for row in cur.execute("SELECT * from test"):
        print(row)
@add_decor
def dropping_the_table():
    #Add code to drop the table
    print("Dropping the table.....")
    cur.execute("""
        DROP TABLE test
        """)
    print("Table Dropped. ")
@add_decor
def close_db_connection():
    print("Close the database connection: ")
    db.close()
    

def main():
    print("SQLite DB API.")
    create_table_in_db()
    add_data_to_db_table()
    count_no_of_rows()
    print_data_in_table()
    dropping_the_table()
    close_db_connection()
    
    
    
if __name__ == "__main__":
    main()
    
        