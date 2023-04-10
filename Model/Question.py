from Model.Database import database


class Question:
    def __init__(self):
        self.database = database

    def get_data(self):
        data = []
        self.database.cursor.execute("SELECT * FROM Question")
        questions = self.database.cursor.fetchall()

        for question in questions:
            self.database.cursor.execute(f"SELECT * FROM Answer WHERE id_question ={question[0]}")
            answers = self.database.cursor.fetchall()
            data.append({'id_question': question[0], 'title': question[1], 'answers':
                [{'id': answer[0], 'title': answer[1]} for answer in answers]})
        return data

    def get_by_id(self, question_number):
        self.database.cursor.execute(f'SELECT title FROM Answer WHERE id_question={question_number}')
        answers = [item[0] for item in self.database.cursor.fetchall()]
        self.database.cursor.execute(f'SELECT id, title FROM Question WHERE id={question_number}')
        question = list(self.database.cursor.fetchone())
        for answer in answers:
            question.append(answer)
        return question

    def get_one(self, question_id):
        self.database.cursor.execute(f'SELECT id FROM Question ORDER BY id ASC LIMIT 1 OFFSET {question_id}')
        return self.database.cursor.fetchone()


questions = Question()
# print(questions.get_data())
