import sqlite3


class DataBase:
    def __init__(self):
        databaseName = '../RandomCofeeBot.db'
        try:
            self.sqliteConnection = sqlite3.connect(databaseName)
            self.cursor = self.sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def __del__(self):
        self.cursor.close()
        self.sqliteConnection.close()
        print("Closed")


database = DataBase()