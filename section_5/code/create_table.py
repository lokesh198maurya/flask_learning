import sqlite3

conection = sqlite3.connect('data.db')
cursor = conection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users('id' INTEGER PRIMARY KEY, 'username' text, 'password' text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items('item' text, 'price' real)"
cursor.execute(create_table)

conection.commit()
conection.close()
