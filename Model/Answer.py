from Model.Database import database


class Answer:
    def __init__(self):
        self.database = database

    def get_data(self):
        self.database.cursor.execute("SELECT * FROM Answer")
        answers = self.database.cursor.fetchall()
        return answers

    def get_data_title_question(self, title, id_question):
        print(f"SELECT id FROM Answer WHERE title like '{title}' and id_question = {id_question}")
        self.database.cursor.execute(f"SELECT id FROM Answer WHERE title like '{title}' and id_question = {id_question}")

        answer_id = self.database.cursor.fetchone()
        print(answer_id)
        return answer_id[0]

    def get_data_by_user_id(self, user_id):
        self.database.cursor.execute(f"SELECT * FROM Answer WHERE id_user = {user_id}")
        answers_by_user_id = self.database.cursor.fetchall()
        return answers_by_user_id


answer = Answer()
print(answer.get_data())
