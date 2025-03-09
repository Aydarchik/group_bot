import sqlite3


class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = sqlite3.connect(self.db_url)
        self.cursor = self.conn.cursor()

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

        # insert #

    def add_user(self, tg_id: str):
        self.cursor.execute("INSERT INTO users (tg_id) VALUES (?)", (tg_id,))
        self.conn.commit()

    def add_max_call(self, tg_id: str, max_call: int):
        self.cursor.execute("UPDATE users SET max_call = ? WHERE tg_id = ?", (max_call, tg_id))
        self.conn.commit()

    def add_min_call(self, tg_id: str, min_call: int):
        self.cursor.execute("UPDATE users SET min_call = ? WHERE tg_id = ?", (min_call, tg_id))
        self.conn.commit()

    def add_day_call(self, tg_id: str, day_call: int):
        self.cursor.execute("UPDATE users SET day_call = ? WHERE tg_id = ?", (day_call, tg_id))
        self.conn.commit()

    def add_food(self, tg_id: str, food: str, food_call: int, protein: int, fat: int, carbohydrates: int):
        self.cursor.execute(
            "INSERT INTO foods (user_tg_id, food, food_call, protein, fat, carbohydrates) VALUES (?, ?, ?, ?, ?, ?)",
            (tg_id, food, food_call, protein, fat, carbohydrates))
        self.conn.commit()

        # select #

    def select_user(self, tg_id: str):
        self.cursor.execute('''
            SELECT max_call, min_call, day_call FROM users
            WHERE tg_id = ?
        ''', (tg_id,))
        user = self.cursor.fetchone()

        if user:
            return {
                'max_call': user[0],
                'min_call': user[1],
                'day_call': user[2],
            }

        return None


db_manager = DatabaseManager('database.db')

if __name__ == "__main__":
    pass
