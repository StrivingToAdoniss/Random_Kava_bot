from Model.Database import database


class Question:
    def __init__(self):
        self.database = database

    def get_data(self):
        self.database.cursor.execute("SELECT * FROM Question")
        return self.database.cursor.fetchall()


questions = Question()
# print(questions.get_data())
