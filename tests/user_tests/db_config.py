import sqlite3


class DBConnect:
    URL = '../../user/instance/database/user.db'

    def __init__(self):
        db = sqlite3.connect(self.URL)
        self.cur = db.cursor()

    def select_user_info_by_id(self, user_id):
        result = self.cur.execute(f"SELECT * from user WHERE id = {user_id}").fetchall()
        return result
