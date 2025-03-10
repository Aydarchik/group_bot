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

    def add_user(self, username: str):
        self.cursor.execute("INSERT INTO users (tg_id) VALUES (?)", (username,))
        self.conn.commit()
        self.conn.close()

    def add_max_call(self, username: str, max_call: float):
        self.cursor.execute("UPDATE users SET max_call = ? WHERE tg_id = ?", (max_call, username))
        self.conn.commit()
        self.conn.close()

    def add_min_call(self, username: str, min_call: float):
        self.cursor.execute("UPDATE users SET min_call = ? WHERE tg_id = ?", (min_call, username))
        self.conn.commit()
        self.conn.close()

    def add_day_call(self, username: str, day_call: float):
        self.cursor.execute("UPDATE users SET day_call = ? WHERE tg_id = ?", (day_call, username))
        self.conn.commit()
        self.conn.close()

    def add_food(self, username: str, food: str, food_call: float, protein: float, fat: float, carbohydrates: float):
        self.cursor.execute("INSERT INTO foods (user_tg_id, food, food_call, protein, fat, carbohydrates) VALUES (?, ?, ?, ?, ?, ?)",
                             (username, food, food_call, protein, fat, carbohydrates))
        self.conn.commit()
        self.conn.close()
        
db_manager = DatabaseManager('database.db')

if __name__ == "__main__":
    pass
