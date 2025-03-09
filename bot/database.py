import sqlite3


class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = sqlite3.connect(self.db_url)
        self.cursor = self.connection.cursor()

    def init_db(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER NOT NULL,
        max_call INTEGER,
        min_call INTEGER,
        day_call INTEGER
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_tg_id INTEGER NOT NULL,
        food INTEGER NOT NULL,
        food_call INTEGER NOT NULL,
        protein INTEGER NOT NULL,
        fat INTEGER NOT NULL,
        carbohydrates INTEGER NOT NULL,
        FOREIGN KEY (user_tg_id) REFERENCES users(tg_id) ON DELETE CASCADE
        )
        ''')

db_manager = DatabaseManager('database.db')


if __name__ == "__main__":
    pass