from Model.Database import database


class User:
    def __init__(self):
        self.database = database

    def get_data(self):
        """
        Gets all data from User database
        :return: data from User database
        """
        self.database.cursor.execute("SELECT * FROM User")
        return list(self.database.cursor.fetchall())

    def insert_user(self, user_id, username):
        """
        Inserts data in User database
        """
        if not self.isUsersById(user_id):
            self.database.cursor.execute \
                (f"INSERT INTO User(id, username, id_category) VALUES('{user_id}', '{username}', NULL)")
            self.database.connection.commit()

    def updateCategory(self, users_id, categories_id):
        """
        Updates id_category in User database
        :param data: data in the format id, id_category
        """
        if len(users_id) == len(categories_id):
            for user_id, category_id in zip(users_id, categories_id):
                # print(category_id)
                # print(user_id)
                if self.isUsersById(user_id):
                    self.database.cursor.execute(
                        f"UPDATE User SET id_category = {int(category_id)} WHERE id = '{user_id}'")
                    self.database.connection.commit()
                    # print()

    def getUsersByCategoryId(self, id):
        self.database.cursor.execute(f"SELECT * FROM User WHERE id_category = {id}")
        return self.database.cursor.fetchall()

    def getUsersId(self):
        self.database.cursor.execute(f"SELECT id FROM User")
        users = self.database.cursor.fetchall()
        return [i[0] for i in users]

    def getUsernameId(self, user_id):
        self.database.cursor.execute(f"SELECT username FROM User WHERE id = '{user_id}'")
        username = self.database.cursor.fetchone()
        if username is not None:
            return username[0]
        else:
            return None
    def isUsersById(self, user_id):
        self.database.cursor.execute(f"SELECT * FROM User WHERE id = '{user_id}'")
        res = len(self.database.cursor.fetchall()) > 0
        # print(res)
        return res

    def updateUsernameNumber(self, user_id, phone_number):
        """
        Updates id_category in User database
        :param data: data in the format id, id_category
        """

        if self.isUsersById(user_id):
            self.database.cursor.execute(f"UPDATE User SET username = '{phone_number}' WHERE id = '{user_id}'")
            self.database.connection.commit()
            # print()
        else:
            self.insert_user(user_id, phone_number)

    def get_usernames_by_category_id(self, category_id):
        """
        Gets all categories from Category database
        :return: list of categories
        """
        self.database.cursor.execute(f"SELECT username FROM User WHERE id_category = {category_id}")
        return [item[0] for item in self.database.cursor.fetchall()]

    def get_users_all_questions(self):
        self.database.cursor.execute(f"SELECT id_user FROM User_Answer GROUP BY id_user "
                                     f"HAVING COUNT(DISTINCT id_question) = (SELECT COUNT(*) FROM Question)")
        res = [item[0] for item in self.database.cursor.fetchall()]
        return res

    def is_screen_valid(self, user_id):
        self.database.cursor.execute(f"SELECT is_screen FROM User WHERE id = '{user_id}'")
        res = self.database.cursor.fetchone()
        # print(res)
        return res[0]

    def set_screen_valid(self, user_id):
        if self.isUsersById(user_id):
            self.database.cursor.execute(f"UPDATE User SET is_screen = 1 WHERE id = '{user_id}'")
            self.database.connection.commit()

    def get_users_id_with_valid_screen(self):
        self.database.cursor.execute(f"SELECT id FROM User where is_screen = 1")
        users = self.database.cursor.fetchall()
        return [i[0] for i in users]

    def get_users_id_without_discount_sent(self):
        self.database.cursor.execute(f"SELECT id FROM User where is_discount = 0 and is_screen = 1")
        users = self.database.cursor.fetchall()
        return [i[0] for i in users]

    def is_discount_set(self, user_id):
        self.database.cursor.execute(f"SELECT is_discount FROM User WHERE id = '{user_id}'")
        res = self.database.cursor.fetchone()
        # print(res)
        return res[0]

    def set_discount_sent(self, user_id):
        if self.isUsersById(user_id):
            self.database.cursor.execute(f"UPDATE User SET is_discount = 1 WHERE id = '{user_id}'")
            self.database.connection.commit()

user = User()
# print(user.isUsersById("795526685"))
# user.insert_data(1, 2)
# user.insert_data(22)
# user.updateCategory()
# print(user.get_data())
