from Database import database

class Category:
    def __init__(self):
        self.database = database

    def get_categories(self):
        """
        Gets all categories from Category database
        :return: list of categories
        """
        self.database.cursor.execute("SELECT * FROM Category")
        return self.database.cursor.fetchall()

    def get_users_with_categories(self):
        """
        Gets all users with their categories from User database
        :return: list of tuples containing user id and category id
        """
        self.database.cursor.execute("SELECT * FROM User")
        user_data = self.database.cursor.fetchall()

        users_with_categories = []
        for user in user_data:
            users_with_categories.append((user[0], user[1]))

        return users_with_categories
