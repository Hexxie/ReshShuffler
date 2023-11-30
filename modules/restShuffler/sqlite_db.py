import sqlite3
from pathlib import Path


class SqliteDatabaseWrapper:
    def __init__(self, path_to_db, path_to_sql = Path(__file__).parent / "../../data/restEvents.sql"):
        #connect to db
        self.con = sqlite3.connect(path_to_db)

        #get coursor
        self.cur = self.con.cursor()

        #execute script tp fill db
        sql_file = open(path_to_sql)
        sql_script = sql_file.read()
        self.cur.executescript(sql_script)

    def get_cursor(self):
        return self.cur
    
    def get_connection(self):
        return self.con
    
db = SqliteDatabaseWrapper(Path(__file__).parent / "../../data/restEvents.db")