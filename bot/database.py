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

    def add_tg_id(self, user_tg_id: str, ):
        self.cursor.execute("INSERT INTO foods (user_tg_id,) VALUES (?, ?)", (user_tg_id))
        self.conn.commit()
        self.conn.close()
        
    def add_food(self, food:str):
        self.cursor.execute("INSERT INTO foods (food) VALUES (?)", (food,))
        self.conn.commit()
        self.conn.close()
        
    def add_food_call(self, food_call: str):
        self.cursor.execute("INSERT INTO foods (food_call) VALUES (?)", (food_call,))
        self.conn.commit()
        self.conn.close()
        
    def add_protein(self, protein: str):
        self.cursor.execute("INSERT INTO foods (protein) VALUES (?)", (protein,))
        self.conn.commit()
        self.conn.close()
        
    def add_fat(self, fat: str):
        self.cursor.execute("INSERT INTO foods (fat) VALUES (?)", (fat,))
        self.conn.commit()
        self.conn.close()
        
    def add_carbohydrates(self, carbohydrates: str):
        self.cursor.execute("INSERT INTO foods (carbohydrates) VALUES (?)", (carbohydrates,))
        self.conn.commit()
        self.conn.close()
        
db_manager = DatabaseManager('database.db')

if __name__ == "__main__":
    pass
