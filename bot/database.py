import sqlite3

conn = sqlite3.connect("food_nutrition.db")

cur = conn.cursor()

create_table_query = """
CREATE TABLE food_nutrition (
    id SERIAL PRIMARY KEY,  
    food_name VARCHAR(255) NOT NULL,  
    calories_per_100g DECIMAL(10, 2) NOT NULL,  
    fats DECIMAL(10, 2) NOT NULL,  
    proteins DECIMAL(10, 2) NOT NULL,  
    carbohydrates DECIMAL(10, 2) NOT NULL  
);"""

cur.execute(create_table_query)


conn.commit()


cur.close()
conn.close()