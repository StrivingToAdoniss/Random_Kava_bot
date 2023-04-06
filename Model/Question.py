from Model.Database import database


class Question:
    def __init__(self):
        self.database = database

    def get_data(self):
        self.database.cursor.execute("SELECT * FROM Question")
        return self.database.cursor.fetchall()

    def get_by_id(self, question_number):
        self.database.cursor.execute('SELECT id, question, answer1, answer2 FROM questions WHERE id=%s',
                                     (question_number,))
        return self.database.cursor.fetchone()

    def get_one(self, question_id):
        self.database.cursor.execute('SELECT id FROM questions WHERE id > %s ORDER BY id ASC LIMIT 1', (question_id,))
        return self.database.cursor.fetchone()

questions = Question()
# print(questions.get_data())
