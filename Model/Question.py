from Database import database


class Question:
    def __init__(self):
        self.database = database

    def get_data(self):
        self.database.cursor.execute("SELECT * FROM Question")
        questions = self.database.cursor.fetchall()
        return questions


questions = Question()
print(questions.get_data())
