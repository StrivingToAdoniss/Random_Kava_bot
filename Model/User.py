from Database import database


class User:
    def __init__(self):
        self.database = database

    def get_data(self):
        """
        Gets all data from User database
        :return: data from User database
        """
        self.database.cursor.execute("SELECT * FROM User")
        return self.database.cursor.fetchall()

    def insert_data(self, *data):
        """
        Inserts data in User database
        :param data: data in the format id, id_category
        """
        if len(data) == 1:
            self.database.cursor.execute(f"INSERT INTO User VALUES({data[0]}, NULL)")
        else:
            self.database.cursor.execute(f"INSERT INTO User VALUES({data[0]}, {data[1]})")
        self.database.connection.commit()

    def updateCategory(self, *data):
        """
        Updates id_category in User database
        :param data: data in the format id, id_category
        """
        self.database.cursor.execute(f"UPDATE User SET id_category = '{data[1]}' WHERE id = {data[0]}")
        self.database.connection.commit()

    def getUsersByCategoryId(self, id):
        self.database.cursor.execute(f"SELECT * FROM User WHERE id_category = {id}")
        return self.database.cursor.fetchall()


user = User()
# user.insert_data(1, 2)
# user.insert_data(22)
# user.updateCategory()
# print(user.get_data())