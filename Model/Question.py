from Model.Database import database


class Question:
    def __init__(self):
        self.database = database

    def get_data(self):
        self.database.cursor.execute("SELECT * FROM Question")
        return self.database.cursor.fetchall()

    def get_by_id(self, question_number):
        self.database.cursor.execute(f'SELECT title FROM Answer WHERE id_question={question_number}')
        answers = [item[0] for item in self.database.cursor.fetchall()]
        self.database.cursor.execute(f'SELECT id, title FROM Question WHERE id={question_number}')
        question = list(self.database.cursor.fetchone())
        for answer in answers:
            question.append(answer)
        return question

    def get_one(self, question_id):
        self.database.cursor.execute(f'SELECT id FROM Question WHERE id > {question_id} ORDER BY id ASC LIMIT 1')
        return self.database.cursor.fetchone()

questions = Question()
# print(questions.get_data())
