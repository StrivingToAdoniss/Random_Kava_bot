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

    def insert_data(self, id_question, id_user, id_answer):
        """
        Inserts data in User_Answer database
        :param data: data in the format id, id_question, id_user
        """
        self.database.cursor.execute(f"SELECT * FROM User_Answer WHERE id_question = {id_question} and id_user = '{id_user}'")
        id_user_answer = self.database.cursor.fetchone()
        if id_user_answer is None:
            print("INSERT INTO User_Answer(id_question, id_user, id_answer) "
                                         f"VALUES({id_question}, '{id_user}', {id_answer})")
            self.database.cursor.execute("INSERT INTO User_Answer (id_question, id_user, id_answer)"
                                         f"VALUES({id_question}, '{id_user}', {id_answer})")
        else:
            print(f"UPDATE User_Answer SET id_answer = {id_answer} WHERE id = {id_user_answer[0]}")
            self.database.cursor.execute(f"UPDATE User_Answer SET id_answer = {id_answer} WHERE id = {id_user_answer[0]}")

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


user_answer = UserAnswer()
# user_answer.insert_data(1, 2, 3)
# print(user_answer.get_data())
