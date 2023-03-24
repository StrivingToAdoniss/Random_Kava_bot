from Model.Database import database


class UserAnswer:
    def __init__(self):
        self.database = database

    def get_data(self):
        """
        Gets all data from User_Answer database
        :return: data from User_Answer database
        """
        self.database.cursor.execute("SELECT * FROM User_Answer")
        return self.database.cursor.fetchall()

    def insert_data(self, *data):
        """
        Inserts data in User_Answer database
        :param data: data in the format id, id_question, id_user
        """
        self.database.cursor.execute(f"INSERT INTO User_Answer VALUES({data[0]}, {data[1]}, {data[2]})")
        self.database.connection.commit()

    def updateQuestion(self, *data):
        """
        Updates id_question in User_Answer database
        :param data: data in the format id, id_question
        """
        self.database.cursor.execute(f"UPDATE User_Answer SET id_question = '{data[1]}' WHERE id = {data[0]}")

    def updateUser(self, *data):
        """
        Updates id_user in User_Answer database
        :param data: data in the format id, id_user
        """
        self.database.cursor.execute(f"UPDATE User_Answer SET id_user = '{data[1]}' WHERE id = {data[0]}")
        self.database.connection.commit()


# user_answer = UserAnswer()
# user_answer.insert_data(1, 2, 3)
# print(user_answer.get_data())
