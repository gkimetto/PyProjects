import sqlite3

class UtilCreateDB:
    
    print("Connecting to Database....")
    db = sqlite3.connect('db-api.db')
    cur = db.cursor()
    print('Creating Lotto Database: ')
    curr.execute('DROP TABLE IF EXISTS lotto')
    curr.execute("""CREATE TABLE lotto (id INTEGER PRIMARY KEY, LottoNo Varchar, NoOfWins Int, NoOfNoWins Int, Prob float """)