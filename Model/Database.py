import sqlite3


class DataBase:
    def __init__(self):
        databaseName = '../RandomCofeeBot.db'
        try:
            self.connection = sqlite3.connect(databaseName)
            self.cursor = self.connection.cursor()
            print("Database created and Successfully Connected to SQLite")
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        print("Closed")

    def getTableInfo(self, name):
        """Return a string representing the table's CREATE"""
        self.cursor.execute("SELECT sql FROM sqlite_master WHERE name=?;", [name])
        return self.cursor.fetchone()[0]


database = DataBase()
